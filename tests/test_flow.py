"""End-to-End Integration Tests for Ayni Cacao Backend."""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.config import settings


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_01_health_and_root():
    """Verify application boots and health check returns expected status."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert data["exchange_rate_bob"] == settings.EXCHANGE_RATE_USDC_BOB
        assert data["vaquita_pool_id"] == settings.VAQUITA_POOL_ID

        root_resp = await client.get("/")
        assert root_resp.status_code == 200
        assert root_resp.json()["status"] == "ONLINE"


@pytest.mark.anyio
async def test_02_producers_seed_data():
    """Verify initial database seeding of Alto Beni cooperative cacao farmers."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/producers")
        assert resp.status_code == 200
        producers = resp.json()
        assert len(producers) >= 3

        names = [p["name"] for p in producers]
        assert "Mateo Mamani Ticona" in names
        assert "Elena Quispe Condori" in names
        assert "Carlos Condori Mamani" in names

        # Check detailed profile with EUDR plot and historical deliveries
        detail_resp = await client.get("/api/v1/producers/1")
        assert detail_resp.status_code == 200
        mateo = detail_resp.json()
        assert mateo["id"] == 1
        assert "El Ceibo" in mateo["cooperative"]
        assert mateo["eudr_latitude"] == -15.5412
        assert mateo["eudr_longitude"] == -67.3298
        assert len(mateo["deliveries"]) >= 2
        assert mateo["total_delivered_kg"] > 0


@pytest.mark.anyio
async def test_03_module_1_cacao_baba_delivery():
    """Test Module 1: Cacao BABA delivery with 0.33 conversion factor and Stellar notarization."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "producer_id": 1,
            "cacao_type": "BABA",
            "gross_weight_kg": 1000.0,
            "moisture_percentage": 56.0,
            "quality_grade": "A",
            "base_price_per_kg_usdc": 4.80,
        }
        resp = await client.post("/api/v1/deliveries", json=payload)
        assert resp.status_code == 201
        data = resp.json()

        # Business rule: 1000 kg BABA * 0.33 = 330 kg dry
        assert data["net_dry_weight_kg"] == 330.0
        # Grade A multiplier = 1.0x -> $4.80 / kg
        assert data["final_price_per_kg_usdc"] == 4.80
        # Total USDC = 330 * 4.80 = 1584.00
        assert data["total_amount_usdc"] == 1584.00
        # Total BOB = 1584 * 6.96 = 11024.64
        assert data["total_amount_bob"] == round(1584.00 * settings.EXCHANGE_RATE_USDC_BOB, 2)
        # EUDR Coords present
        assert "PLOT:" in data["eudr_coords"]
        # SHA-256 hash generated
        assert len(data["payload_hash"]) == 64
        # Stellar on-chain notarization mock hash present
        assert data["stellar_tx_hash"] is not None
        assert data["status"] == "NOTARIZED"


@pytest.mark.anyio
async def test_04_module_1_cacao_seco_moisture_penalty():
    """Test Module 1: Cacao SECO delivery with excess moisture (>7.5%) and Grade B (0.90x)."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "producer_id": 2,
            "cacao_type": "SECO",
            "gross_weight_kg": 500.0,
            "moisture_percentage": 9.5,  # excess: 2.0% -> penalty: 10 kg -> net: 490 kg
            "quality_grade": "B",        # multiplier: 0.90x -> price: 4.80 * 0.90 = 4.32
            "base_price_per_kg_usdc": 4.80,
        }
        resp = await client.post("/api/v1/deliveries", json=payload)
        assert resp.status_code == 201
        data = resp.json()

        assert data["net_dry_weight_kg"] == 490.0
        assert data["final_price_per_kg_usdc"] == 4.32
        assert data["total_amount_usdc"] == 2116.80
        assert data["total_amount_bob"] == round(2116.80 * settings.EXCHANGE_RATE_USDC_BOB, 2)
        assert data["status"] == "NOTARIZED"


@pytest.mark.anyio
async def test_05_module_2_factoring_simulation():
    """Test Module 2: ML-powered Factoring Simulation with climate inputs."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "producer_id": 1,
            "expected_harvest_kg": 1500.0,
            "rainfall_mm": 160.0,  # Optimal rainfall for Alto Beni
            "humidity_pct": 75.0,  # Good humidity
        }
        resp = await client.post("/api/v1/factoring/simulate", json=payload)
        assert resp.status_code == 200
        sim = resp.json()

        assert sim["producer_id"] == 1
        assert 0.0 <= sim["risk_score"] <= 100.0
        assert sim["risk_level"] in ["BAJO", "MEDIO", "ALTO"]
        assert 15.0 <= sim["approved_advance_pct"] <= 60.0
        assert sim["max_advance_usdc"] > 0
        assert sim["max_advance_bob"] == round(sim["max_advance_usdc"] * settings.EXCHANGE_RATE_USDC_BOB, 2)
        assert len(sim["risk_factors"]) >= 2
        # Check Spanish agronomic explanation
        factors_text = " ".join(sim["risk_factors"])
        assert "Precipitación" in factors_text


@pytest.mark.anyio
async def test_06_module_2_factoring_execute_and_escrow():
    """Test Module 2: Factoring execution -> Vaquita Reserve -> Trustless Escrow -> Pollar QR."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "producer_id": 1,
            "requested_amount_usdc": 800.00,
            "expected_harvest_kg": 1500.0,
            "rainfall_mm": 160.0,
            "humidity_pct": 75.0,
        }
        resp = await client.post("/api/v1/factoring/execute", json=payload)
        assert resp.status_code == 201
        loan = resp.json()

        assert loan["loan_id"] > 0
        assert loan["loan_code"].startswith("LOAN-AB-1-")
        assert loan["approved_amount_usdc"] == 800.00
        assert loan["amount_bob"] == round(800.00 * settings.EXCHANGE_RATE_USDC_BOB, 2)
        assert loan["status"] == "ACTIVE_ESCROW"
        assert loan["vaquita_reservation_id"].startswith("vaq_res_")
        assert loan["trustless_escrow_id"].startswith("escrow_tw_")
        assert loan["pollar_payout_id"].startswith("pol_out_")
        assert "bo.gob.asfi.qr" in loan["pollar_qr_payload"]
        assert "https://qr.pollar.io/pay/" in loan["qr_deep_link"]


@pytest.mark.anyio
async def test_07_credit_limit_validation():
    """Verify that requesting an amount above the approved credit limit is rejected."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "producer_id": 3,  # Carlos (high risk)
            "requested_amount_usdc": 99999.00,
            "expected_harvest_kg": 300.0,
            "rainfall_mm": 270.0,  # Extreme rain
            "humidity_pct": 92.0,   # High humidity / fungal risk
        }
        resp = await client.post("/api/v1/factoring/execute", json=payload)
        assert resp.status_code == 422
        err = resp.json()
        assert err["success"] is False
        assert err["error"]["code"] == "FACTORING_VALIDATION_ERROR"


@pytest.mark.anyio
async def test_08_dashboard_metrics():
    """Verify real-time dashboard aggregation and Vaquita pool status."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/dashboard")
        assert resp.status_code == 200
        dash = resp.json()

        # Check Vaquita Pool
        pool = dash["vaquita_pool"]
        assert pool["total_liquidity_usdc"] == 25000.00
        assert pool["reserved_liquidity_usdc"] >= 800.00
        assert pool["available_liquidity_usdc"] <= 24200.00

        # Check Loans
        assert dash["active_loans_count"] >= 1
        assert dash["total_advanced_usdc"] >= 800.00
        assert dash["total_advanced_bob"] > 0
        assert len(dash["active_loans"]) >= 1

        # Check Deliveries
        assert dash["total_deliveries_count"] >= 5
        assert len(dash["recent_deliveries"]) > 0


@pytest.mark.anyio
async def test_09_module_2_factoring_settlement():
    """Test Module 2: Loan settlement with 2.5% fee (2% Vaquita Pool, 0.5% Ayni Cacao)."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # First check active loans from dashboard
        dash_resp = await client.get("/api/v1/dashboard")
        active_loans = dash_resp.json()["active_loans"]
        assert len(active_loans) > 0
        target_loan_id = active_loans[0]["id"]
        principal = active_loans[0]["approved_amount_usdc"]

        # Settle loan
        settle_resp = await client.post(f"/api/v1/factoring/{target_loan_id}/settle")
        assert settle_resp.status_code == 200
        settle_data = settle_resp.json()

        assert settle_data["status"] == "SETTLED"
        expected_vaquita_fee = round(principal * 0.02, 2)
        expected_ayni_fee = round(principal * 0.005, 2)
        expected_total = round(principal + expected_vaquita_fee + expected_ayni_fee, 2)

        assert settle_data["fee_vaquita_usdc"] == expected_vaquita_fee
        assert settle_data["fee_ayni_usdc"] == expected_ayni_fee
        assert settle_data["total_settled_usdc"] == expected_total
        assert settle_data["trustless_settlement_tx"] is not None

        # Verify pool liquidity after settlement: reserved capital restored, 2% yield credited
        dash_after = (await client.get("/api/v1/dashboard")).json()
        assert dash_after["vaquita_pool"]["reserved_liquidity_usdc"] == 0.0
        assert dash_after["vaquita_pool"]["total_liquidity_usdc"] == 25000.00 + expected_vaquita_fee

        # Attempting to settle again should return 400 InvalidOperationException
        double_settle = await client.post(f"/api/v1/factoring/{target_loan_id}/settle")
        assert double_settle.status_code == 400
        assert double_settle.json()["error"]["code"] == "INVALID_OPERATION"
