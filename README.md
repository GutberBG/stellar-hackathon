# Ayni Cacao - Backend API 🍫🌱

> **Plataforma de Acopio Transparente de Cacao y Factoring Agrícola Predictivo**  
> Enfocada en cooperativas cacaoteras del norte de La Paz, Bolivia (**Alto Beni, Sapecho y Palos Blancos**), cuna del cacao silvestre y agroforestal (ej. Central de Cooperativas El Ceibo).

Este repositorio contiene **exclusivamente el Backend** de Ayni Cacao, diseñado bajo **Clean Architecture** y **Arquitectura Hexagonal (Ports & Adapters)**, con oráculo de riesgo agronómico impulsado por **Machine Learning** (`scikit-learn`), base de datos asíncrona (`SQLAlchemy` + `aiosqlite`) y adaptadores listos para la integración con **Stellar/Soroban**, **Pollar**, **Vaquita** y **Trustless Work**.

---

## 🏛️ Arquitectura del Sistema (Ports & Adapters)

El backend aísla completamente la lógica de negocio y las reglas agronómicas de cualquier proveedor externo o infraestructura de persistencia.

```
                  ┌────────────────────────────────────────┐
                  │           FastAPI Endpoints            │
                  │   (/deliveries, /factoring, etc.)      │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
                        ┌──────────────────────────┐
                        │     Domain Services      │
                        │   (Pricing, Dry Weight,  │
                        │    Settlement & Fees)    │
                        └─────────────┬────────────┘
                                      │
         ┌────────────────────────────┼───────────────────────────┐
         ▼                            ▼                           ▼
┌──────────────────┐        ┌───────────────────┐       ┌──────────────────┐
│   StellarPort    │        │    PollarPort     │       │   VaquitaPort    │
│  (Notarización   │        │ (Invisible Auth   │       │  (Pool Staking   │
│   y Pagos USDC)  │        │  y QR en Bs.)     │       │   y Liquidez)    │
└────────┬─────────┘        └─────────┬─────────┘       └─────────┬────────┘
         │                            │                           │
         ▼                            ▼                           ▼
┌──────────────────┐        ┌───────────────────┐       ┌──────────────────┐
│MockStellarAdapter│        │ MockPollarAdapter │       │MockVaquitaAdapter│
│(Listo para Demo) │        │ (Listo para Demo) │       │(Listo para Demo) │
└──────────────────┘        └───────────────────┘       └──────────────────┘
```

### Interfaces de Dominio (`app/domain/ports/`)
* **`StellarPort`**: Notarización inmutable de boletas de acopio (`payload_hash` + coordenadas EUDR) y transferencias de tokens USDC.
* **`PollarPort`**: Generación de credenciales invisibles y desembolso inmediato a pequeños productores mediante el estándar interbank **Simple QR en Bolivianos (BOB)**.
* **`VaquitaPort`**: Consulta de liquidez disponible, bloqueo/reserva de capital para préstamos y acreditación de rendimientos por factoring.
* **`TrustlessPort`**: Despliegue de contratos de depósito en garantía (escrow) condicionados a hitos de floración y entrega de cosecha.

### ¿Cómo cambiar los Mocks por SDKs reales en Producción?
Gracias a la inyección de dependencias centralizada en [`app/api/v1/dependencies.py`](file:///e:/PROJECTS/stellar-backend/app/api/v1/dependencies.py), no es necesario modificar ningún endpoint ni servicio. Simplemente se crea el nuevo adaptador en `app/infrastructure/adapters/` y se sustituye la clase en `dependencies.py`:

```python
# Ejemplo en app/api/v1/dependencies.py:
def get_stellar_adapter() -> StellarPort:
    # Reemplazar MockStellarAdapter por el adaptador con stellar-sdk
    return RealStellarAdapter(secret_key=settings.STELLAR_SECRET_KEY)
```

---

## 🧠 Oráculo de Riesgo Agronómico y Machine Learning (`app/ml/`)

El oráculo evalúa el riesgo crediticio y proyecta el rendimiento de la cosecha combinando:
1. **Historial del Productor:** Cumplimiento histórico de entregas y porcentaje de calidad Grado A.
2. **Microclima de Alto Beni:**
   * **Precipitación óptima (140 - 180 mm):** Condición climática ideal para floración y llenado de mazorcas.
   * **Alerta de sequía (< 80 mm):** Caída severa de flores y estrés hídrico.
   * **Alerta de plagas (> 240 mm):** Humedad y lluvia excesiva detonan brotes de **Moniliasis** (*Moniliophthora roreri*) y **Mazorca Negra** (*Phytophthora*).
   * **Humedad relativa (> 85%):** Acelera la proliferación fungosa en el bosque tropical húmedo.

### Modelo de rendimiento y proyección de ingresos (roadmap)

El precio internacional y el rendimiento por hectárea se modelan por separado:

```
producción_kg      = hectáreas × rendimiento_kg_ha
ingreso_proyectado = producción_kg × precio_usd_kg × factor_calidad
```

El dataset de trabajo (precios, clima, rendimiento FAO y panel sintético de parcelas) vive en `../ayni-precios/`. La integración reemplazará el `expected_harvest_kg` auto-reportado y el precio fijo de 4.80 USDC/kg por las salidas de ambos modelos.

### Tiers de Factoring Aprobado
* **Riesgo BAJO (Score ≤ 35):** Adelanto pre-aprobado del **50% al 60%** del valor proyectado.
* **Riesgo MEDIO (Score 36 - 65):** Adelanto pre-aprobado del **30% al 49%**.
* **Riesgo ALTO (Score > 65):** Adelanto precautorio del **15% al 29%**.

---

## 📋 Especificación de Endpoints para el Frontend

Base URL: `http://localhost:8000/api/v1`  
Documentación interactiva Swagger: `http://localhost:8000/docs`

### 1. Productores
* `GET /api/v1/producers`: Retorna la lista de socios cacaoteros.
* `GET /api/v1/producers/{id}`: Perfil completo, coordenadas EUDR (Trazabilidad y Cero Deforestación), superficie (`hectares`), edad de plantas (`tree_age_years`), altitud (`altitude_m`), historial de entregas y préstamos activos.

### 2. Módulo 1 · Acopio y Boleta Transparente
* `POST /api/v1/deliveries`:
  * **Input:**
    ```json
    {
      "producer_id": 1,
      "cacao_type": "BABA",
      "gross_weight_kg": 1000.0,
      "moisture_percentage": 55.0,
      "quality_grade": "A",
      "base_price_per_kg_usdc": 4.80
    }
    ```
  * **Reglas de Negocio:**
    * Si `cacao_type == "BABA"`, aplica factor de conversión **0.33** para obtener peso seco equivalente.
    * Si `cacao_type == "SECO"` y `moisture_percentage > 7.5%`, descuenta el exceso porcentual del peso bruto.
    * Multiplicador de calidad: Grado A (**1.0x**), Grado B (**0.90x**), Grado C (**0.75x**).
    * Genera hash SHA-256 del ticket + coordenadas EUDR y lo notariza en Stellar Testnet (`tx_hash`).
    * Retorna desglose en **USDC** y en **Bolivianos (Bs.)** al tipo de cambio oficial de 6.96.
* `GET /api/v1/deliveries`: Listado paginado de boletas registradas.
* `GET /api/v1/deliveries/{id}`: Detalle de una boleta específica.

### 3. Módulo 2 · Factoring y Escrow
* `POST /api/v1/factoring/simulate`:
  * **Input:** `producer_id`, `expected_harvest_kg`, `rainfall_mm`, `humidity_pct`.
  * **Output:** `risk_score` (0-100), `risk_level` (`BAJO`, `MEDIO`, `ALTO`), `approved_advance_pct` (15%-60%), `max_advance_usdc`, `max_advance_bob`, y `risk_factors` (diagnósticos explicativos en español listos para mostrar en el frontend).
* `POST /api/v1/factoring/execute`:
  * Ejecuta la orquestación atómica:
    1. **Vaquita:** Reserva liquidez del pool (`vaquita_reservation_id`).
    2. **Trustless Work:** Abre el escrow de hitos (`trustless_escrow_id`).
    3. **Pollar:** Genera orden de desembolso y **Simple QR en Bolivianos** (`pollar_qr_payload` y `qr_deep_link`).
  * Deja el préstamo en estado `ACTIVE_ESCROW`.
* `POST /api/v1/factoring/{loan_id}/settle`:
  * Simula la entrega final de la cosecha:
    * Cobra el capital original + comisión del **2.5%** (**2% para el Pool de Vaquita**, **0.5% para Ayni Cacao**).
    * Libera el contrato de Trustless Work.
    * Acredita el rendimiento al Vaquita Pool.
    * Pasa el préstamo a estado `SETTLED`.

### 4. Dashboard & Liquidez Vaquita
* `GET /api/v1/dashboard`:
  * Estado en vivo de liquidez del Vaquita Pool (total, reservada y disponible).
  * Monto total adelantado en USDC y Bolivianos.
  * Préstamos activos en garantía y últimas boletas notarizadas.

---

## 👥 Seed Data Automático

Al iniciar la aplicación con una base de datos vacía, se auto-generan:
1. **Mateo Mamani Ticona:** Central El Ceibo (Sapecho), Parcela `BO-LPZ-AB-ELCEIBO-001`, 3.2 ha, plantas de 12 años, 520 msnm, Riesgo BAJO, cumplimiento 96%.
2. **Elena Quispe Condori:** Cooperativa Agroecológica Palos Blancos, Parcela `BO-LPZ-PB-AGROECO-002`, 2.4 ha, plantas de 8 años, 480 msnm, Riesgo MEDIO, cumplimiento 78%.
3. **Carlos Condori Mamani:** Bella Vista, Parcela `BO-LPZ-BV-ASOPROC-003`, 1.5 ha, plantas de 4 años, 430 msnm, Riesgo ALTO (nuevo productor), cumplimiento 55%.
4. **5 Boletas Históricas:** Con ejemplos de cacao baba, cacao seco con penalización y grados A/B.
5. **Vaquita Pool:** Fondos iniciales de **$25,000.00 USDC**.

---

## 🚀 Puesta en Marcha

### 1. Activar entorno virtual
```powershell
# En Windows PowerShell (raíz del proyecto):
.\venv\Scripts\Activate.ps1
```

### 2. Ejecutar la Suite de Pruebas (Test E2E)
```powershell
.\venv\Scripts\pytest.exe -v
```

### 3. Iniciar el Servidor de Desarrollo
```powershell
.\venv\Scripts\uvicorn.exe app.main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en `http://localhost:8000` con Swagger UI en `http://localhost:8000/docs`.
CORS está completamente habilitado (`*`) para conectar el repositorio del frontend de inmediato.
