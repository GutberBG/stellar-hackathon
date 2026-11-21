"""Mock adapter for Pollar invisible account and Bolivian banking QR cash-out."""
import hashlib
import time
from typing import Any, Dict
from app.domain.ports.pollar_port import PollarPort


class MockPollarAdapter(PollarPort):
    """
    Simulated implementation of Pollar rails for invisible on/off-ramp and QR cash-out in Bolivianos (BOB).

    # TODO: Integrar SDK real de Pollar (Pollar Invisible Wallet & QR Cash-out API)
    # Ejemplo de migración futura:
    # import httpx
    # response = await httpx.post(f"{settings.POLLAR_API_BASE_URL}/disbursements/qr", json=...)
    """

    async def disburse_to_qr(
        self,
        producer_id: int,
        producer_phone: str,
        amount_bob: float,
        concept: str,
    ) -> Dict[str, Any]:
        """
        Simulates generation of a Simple QR payload compliant with the Bolivian Interbank System (ASFI/BCP/BNB/Banco Unión).
        Enables the cacao smallholder to receive Bolivianos instantly in their local bank account or cash-point.
        """
        timestamp = int(time.time())
        payout_seed = f"POLLAR_PAYOUT:{producer_id}:{amount_bob}:{timestamp}"
        payout_id = "pol_out_" + hashlib.sha256(payout_seed.encode()).hexdigest()[:16]

        # Bolivian Interbank Simple QR format simulation
        qr_payload = (
            f"00020101021226500014bo.gob.asfi.qr0124AYNICACAO-{producer_id}52044217"
            f"5303068540{len(str(amount_bob)):02d}{amount_bob}5802BO"
            f"5910ALTO_BENI6012PALOS_BLANCOS62200516{payout_id[:16]}6304ABCD"
        )

        return {
            "payout_id": payout_id,
            "producer_id": producer_id,
            "currency": "BOB",
            "amount_bob": amount_bob,
            "status": "PROCESSED",
            "concept": concept,
            "payout_channel": "SIMPLE_QR_BOLIVIA",
            "destination_phone": producer_phone,
            "qr_payload": qr_payload,
            "qr_deep_link": f"https://qr.pollar.io/pay/{payout_id}",
            "expires_at_seconds": 86400,
            "created_at": timestamp,
        }

    async def check_payout_status(self, payout_id: str) -> Dict[str, Any]:
        """
        Simulates query to Pollar webhook/API for cash-out clearance.
        """
        return {
            "payout_id": payout_id,
            "status": "COMPLETED",
            "confirmed_at": int(time.time()),
        }
