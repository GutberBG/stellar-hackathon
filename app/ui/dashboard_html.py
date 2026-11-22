"""Embedded Interactive Web Application UI for Ayni Cacao."""

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ayni Cacao 🍫🌱 | Plataforma de Acopio & Factoring Agrícola</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #0f172a; color: #f8fafc; }
    .glass-card { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.08); }
    .badge-stellar { background: linear-gradient(135deg, #0284c7, #2563eb); }
    .badge-cacao { background: linear-gradient(135deg, #b45309, #78350f); }
  </style>
</head>
<body class="min-h-screen flex flex-col">

  <!-- Top Navbar -->
  <header class="border-b border-slate-800 bg-slate-900/80 sticky top-0 z-50 backdrop-blur-md">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <span class="text-3xl">🍫🌱</span>
        <div>
          <span class="text-xl font-extrabold tracking-tight bg-gradient-to-r from-amber-400 to-emerald-400 bg-clip-text text-transparent">
            Ayni Cacao
          </span>
          <span class="text-xs text-slate-400 block -mt-1 font-medium">Alto Beni & Palos Blancos · Bolivia</span>
        </div>
      </div>
      
      <!-- Nav Tabs -->
      <nav class="hidden md:flex space-x-1" id="nav-tabs">
        <button onclick="switchTab('dashboard')" class="tab-btn px-4 py-2 rounded-lg text-sm font-semibold transition-all text-amber-400 bg-slate-800/80" data-tab="dashboard">
          <i class="fa-solid fa-chart-line mr-2"></i>Dashboard
        </button>
        <button onclick="switchTab('producers')" class="tab-btn px-4 py-2 rounded-lg text-sm font-semibold transition-all text-slate-300 hover:text-white hover:bg-slate-800" data-tab="producers">
          <i class="fa-solid fa-users mr-2"></i>Productores EUDR
        </button>
        <button onclick="switchTab('deliveries')" class="tab-btn px-4 py-2 rounded-lg text-sm font-semibold transition-all text-slate-300 hover:text-white hover:bg-slate-800" data-tab="deliveries">
          <i class="fa-solid fa-scale-balanced mr-2"></i>Boleta Acopio
        </button>
        <button onclick="switchTab('factoring')" class="tab-btn px-4 py-2 rounded-lg text-sm font-semibold transition-all text-slate-300 hover:text-white hover:bg-slate-800" data-tab="factoring">
          <i class="fa-solid fa-brain mr-2"></i>Factoring ML
        </button>
        <button onclick="switchTab('ml-forecast')" class="tab-btn px-4 py-2 rounded-lg text-sm font-semibold transition-all text-slate-300 hover:text-white hover:bg-slate-800" data-tab="ml-forecast">
          <i class="fa-solid fa-wand-magic-sparkles mr-2"></i>Pronóstico ML Two-Stage
        </button>
      </nav>

      <div class="flex items-center space-x-3">
        <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 mr-1.5 animate-pulse"></span>Stellar Testnet
        </span>
        <a href="/docs" target="_blank" class="px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition">
          <i class="fa-solid fa-code mr-1"></i>Swagger Docs
        </a>
      </div>
    </div>
  </header>

  <!-- Main Content Container -->
  <main class="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full">

    <!-- TAB 1: DASHBOARD -->
    <div id="tab-dashboard" class="tab-content space-y-6">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-800">
        <div>
          <h1 class="text-2xl font-bold text-white">Métricas de Operación en Tiempo Real</h1>
          <p class="text-sm text-slate-400">Supervisión de liquidez de Vaquita Pool, boletas notarizadas y factoring activo.</p>
        </div>
        <button onclick="loadDashboardData()" class="self-start px-3 py-1.5 bg-slate-800 hover:bg-slate-700 rounded-lg text-xs text-slate-200 border border-slate-700 transition">
          <i class="fa-solid fa-rotate mr-1.5"></i>Actualizar
        </button>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="glass-card p-5 rounded-xl border border-slate-700/60 shadow-lg">
          <div class="flex items-center justify-between text-slate-400 text-xs font-medium">
            <span>POOL VAQUITA DISPONIBLE</span>
            <span class="p-2 bg-emerald-500/10 text-emerald-400 rounded-lg"><i class="fa-solid fa-coins"></i></span>
          </div>
          <div class="mt-2 flex items-baseline">
            <span id="stat-pool-avail" class="text-2xl font-extrabold text-emerald-400">$25,000.00</span>
            <span class="ml-1 text-xs text-slate-400">USDC</span>
          </div>
          <div class="mt-2 text-xs text-slate-400 flex justify-between">
            <span>Total Pool: <strong id="stat-pool-total">$25,000.00</strong></span>
            <span>Res.: <strong id="stat-pool-res" class="text-amber-400">$0.00</strong></span>
          </div>
        </div>

        <div class="glass-card p-5 rounded-xl border border-slate-700/60 shadow-lg">
          <div class="flex items-center justify-between text-slate-400 text-xs font-medium">
            <span>TOTAL ADELANTADO (FACTORING)</span>
            <span class="p-2 bg-amber-500/10 text-amber-400 rounded-lg"><i class="fa-solid fa-hand-holding-dollar"></i></span>
          </div>
          <div class="mt-2 flex items-baseline">
            <span id="stat-total-usdc" class="text-2xl font-extrabold text-amber-400">$0.00</span>
            <span class="ml-1 text-xs text-slate-400">USDC</span>
          </div>
          <div class="mt-2 text-xs text-slate-400">
            <span>Equivalente en Bolivianos: <strong id="stat-total-bob" class="text-slate-200">Bs. 0.00</strong></span>
          </div>
        </div>

        <div class="glass-card p-5 rounded-xl border border-slate-700/60 shadow-lg">
          <div class="flex items-center justify-between text-slate-400 text-xs font-medium">
            <span>BOLETAS NOTARIZADAS</span>
            <span class="p-2 bg-blue-500/10 text-blue-400 rounded-lg"><i class="fa-solid fa-file-shield"></i></span>
          </div>
          <div class="mt-2 flex items-baseline">
            <span id="stat-deliveries-count" class="text-2xl font-extrabold text-blue-400">5</span>
            <span class="ml-1 text-xs text-slate-400">tickets</span>
          </div>
          <div class="mt-2 text-xs text-slate-400">
            <span>Inmutabilidad SHA-256 en Stellar</span>
          </div>
        </div>

        <div class="glass-card p-5 rounded-xl border border-slate-700/60 shadow-lg">
          <div class="flex items-center justify-between text-slate-400 text-xs font-medium">
            <span>PRÉSTAMOS EN ESCROW</span>
            <span class="p-2 bg-purple-500/10 text-purple-400 rounded-lg"><i class="fa-solid fa-lock"></i></span>
          </div>
          <div class="mt-2 flex items-baseline">
            <span id="stat-active-loans" class="text-2xl font-extrabold text-purple-400">0</span>
            <span class="ml-1 text-xs text-slate-400">activos</span>
          </div>
          <div class="mt-2 text-xs text-slate-400">
            <span>Trustless Work Smart Contracts</span>
          </div>
        </div>
      </div>

      <!-- Recent Deliveries Table -->
      <div class="glass-card rounded-xl border border-slate-800 p-6 shadow-xl">
        <h3 class="text-lg font-bold text-white mb-4 flex items-center">
          <i class="fa-solid fa-receipt text-amber-400 mr-2"></i>Últimas Boletas de Acopio Notarizadas
        </h3>
        <div class="overflow-x-auto">
          <table class="w-full text-left text-sm text-slate-300">
            <thead class="text-xs uppercase bg-slate-800/80 text-slate-400">
              <tr>
                <th class="px-4 py-3">Código</th>
                <th class="px-4 py-3">Productor</th>
                <th class="px-4 py-3">Tipo / Calidad</th>
                <th class="px-4 py-3">Peso Bruto / Neto</th>
                <th class="px-4 py-3">Total USDC / BOB</th>
                <th class="px-4 py-3">Hash Notarizado Stellar</th>
                <th class="px-4 py-3">Estado</th>
              </tr>
            </thead>
            <tbody id="recent-deliveries-body" class="divide-y divide-slate-800">
              <tr><td colspan="7" class="text-center py-6 text-slate-500">Cargando boletas históricas...</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 2: PRODUCTORES -->
    <div id="tab-producers" class="tab-content hidden space-y-6">
      <div class="flex items-center justify-between pb-2 border-b border-slate-800">
        <div>
          <h1 class="text-2xl font-bold text-white">Socios Cacaoteros Registrados</h1>
          <p class="text-sm text-slate-400">Trazabilidad EUDR, cumplimiento y georreferenciación de parcelas.</p>
        </div>
      </div>

      <div id="producers-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Rendered by JS -->
      </div>
    </div>

    <!-- TAB 3: REGISTRO DE ACOPIO -->
    <div id="tab-deliveries" class="tab-content hidden space-y-6">
      <div class="max-w-2xl mx-auto glass-card rounded-xl border border-slate-800 p-6 md:p-8 shadow-2xl">
        <div class="border-b border-slate-800 pb-4 mb-6">
          <h1 class="text-xl font-bold text-white flex items-center">
            <i class="fa-solid fa-scale-balanced text-emerald-400 mr-2"></i>Registrar Nueva Boleta de Acopio
          </h1>
          <p class="text-xs text-slate-400 mt-1">
            Aplica factores agronómicos automáticos (Baba 0.33, penalización humedad >7.5%) y notariza en Stellar.
          </p>
        </div>

        <form id="delivery-form" onsubmit="submitDelivery(event)" class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-slate-300 uppercase mb-1">Socio Productor</label>
            <select id="del-producer-id" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-amber-400" required>
              <option value="1">Mateo Mamani Ticona - Central El Ceibo (Sapecho)</option>
              <option value="2">Elena Quispe Condori - Coop. Palos Blancos</option>
              <option value="3">Carlos Condori Mamani - Asoc. Bella Vista</option>
            </select>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-semibold text-slate-300 uppercase mb-1">Tipo de Cacao</label>
              <select id="del-cacao-type" onchange="calculatePreview()" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-amber-400">
                <option value="BABA">Cacao en Baba (Húmedo)</option>
                <option value="SECO">Cacao Seco / Fermentado</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-semibold text-slate-300 uppercase mb-1">Grado de Calidad</label>
              <select id="del-quality" onchange="calculatePreview()" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-amber-400">
                <option value="A">Grado A (100% Precio Base)</option>
                <option value="B">Grado B (90% Precio Base)</option>
                <option value="C">Grado C (75% Precio Base)</option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-semibold text-slate-300 uppercase mb-1">Peso Bruto Balanza (kg)</label>
              <input type="number" id="del-gross-weight" step="0.1" value="1000" oninput="calculatePreview()" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-amber-400" required>
            </div>
            <div>
              <label class="block text-xs font-semibold text-slate-300 uppercase mb-1">Humedad Medida (%)</label>
              <input type="number" id="del-moisture" step="0.1" value="55.0" oninput="calculatePreview()" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-amber-400" required>
            </div>
          </div>

          <!-- Preview calculation box -->
          <div class="bg-slate-950/60 border border-slate-800 rounded-lg p-4 space-y-2 text-xs">
            <div class="text-slate-400 font-medium uppercase text-[10px] tracking-wider">Cálculo Agronómico en Vivo</div>
            <div class="flex justify-between">
              <span class="text-slate-400">Peso Neto Seco Estimado:</span>
              <span id="preview-net-weight" class="font-bold text-emerald-400">330.00 kg</span>
            </div>
            <div class="flex justify-between">
              <span class="text-slate-400">Precio Final por kg:</span>
              <span id="preview-price-kg" class="font-bold text-white">$4.80 USDC</span>
            </div>
            <div class="flex justify-between pt-1 border-t border-slate-800 text-sm">
              <span class="font-semibold text-amber-400">Liquidación Estimada:</span>
              <span class="font-extrabold text-amber-400" id="preview-total">$1,584.00 USDC <span class="text-xs text-slate-300">(Bs. 11,024.64)</span></span>
            </div>
          </div>

          <button type="submit" id="btn-submit-delivery" class="w-full py-3 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold rounded-lg shadow-lg transition">
            <i class="fa-solid fa-stamp mr-2"></i>Emitir Boleta & Notarizar en Stellar
          </button>
        </form>

        <!-- Result Box -->
        <div id="delivery-result-box" class="hidden mt-6 bg-emerald-950/40 border border-emerald-600/40 rounded-xl p-4 space-y-2">
          <div class="flex items-center text-emerald-400 font-bold text-sm">
            <i class="fa-solid fa-circle-check mr-2"></i>Boleta Emitida y Notarizada Exitosamente
          </div>
          <div id="delivery-result-content" class="text-xs text-slate-300 font-mono space-y-1"></div>
        </div>
      </div>
    </div>

    <!-- TAB 4: FACTORING ML & ORÁCULO -->
    <div id="tab-factoring" class="tab-content hidden space-y-6">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        <!-- Left: Simulator Controls -->
        <div class="glass-card rounded-xl border border-slate-800 p-6 md:p-8 shadow-2xl space-y-5">
          <div class="border-b border-slate-800 pb-3">
            <h2 class="text-xl font-bold text-white flex items-center">
              <i class="fa-solid fa-brain text-purple-400 mr-2"></i>Oráculo de Riesgo Agronómico ML
            </h2>
            <p class="text-xs text-slate-400 mt-1">
              RandomForest entrenado con microclima de Alto Beni (lluvia, humedad) e historial del productor.
            </p>
          </div>

          <div class="space-y-4 text-sm">
            <div>
              <label class="block text-xs font-semibold text-slate-300 uppercase mb-1">Productor Solicitante</label>
              <select id="fac-producer-id" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white">
                <option value="1">Mateo Mamani (Central El Ceibo - Historial 96%)</option>
                <option value="2">Elena Quispe (Palos Blancos - Historial 78%)</option>
                <option value="3">Carlos Condori (Bella Vista - Nuevo Productor 55%)</option>
              </select>
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-300 uppercase mb-1">Cosecha Proyectada (kg secos)</label>
              <input type="number" id="fac-expected-kg" value="1500" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white">
            </div>

            <!-- Rainfall Slider -->
            <div>
              <div class="flex justify-between items-center mb-1">
                <label class="text-xs font-semibold text-slate-300 uppercase">Precipitación Mensual Alto Beni</label>
                <span id="label-rainfall" class="text-xs font-bold text-emerald-400">160 mm (Óptimo)</span>
              </div>
              <input type="range" id="fac-rainfall" min="40" max="320" value="160" step="5" oninput="updateWeatherLabels()" class="w-full accent-emerald-500">
              <div class="flex justify-between text-[10px] text-slate-500 mt-0.5">
                <span>&lt;80mm (Sequía)</span>
                <span>140-180mm (Óptimo)</span>
                <span>&gt;240mm (Moniliasis)</span>
              </div>
            </div>

            <!-- Humidity Slider -->
            <div>
              <div class="flex justify-between items-center mb-1">
                <label class="text-xs font-semibold text-slate-300 uppercase">Humedad Relativa</label>
                <span id="label-humidity" class="text-xs font-bold text-emerald-400">75% (Seguro)</span>
              </div>
              <input type="range" id="fac-humidity" min="50" max="98" value="75" step="1" oninput="updateWeatherLabels()" class="w-full accent-emerald-500">
              <div class="flex justify-between text-[10px] text-slate-500 mt-0.5">
                <span>50%</span>
                <span>&gt;85% (Alerta Mazorca Negra)</span>
                <span>98%</span>
              </div>
            </div>

            <button onclick="runSimulation()" id="btn-simulate" class="w-full py-2.5 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-bold rounded-lg shadow transition">
              <i class="fa-solid fa-calculator mr-2"></i>Calcular Capacidad de Factoring
            </button>
          </div>
        </div>

        <!-- Right: Simulation Results & Instant QR Payout -->
        <div class="glass-card rounded-xl border border-slate-800 p-6 md:p-8 shadow-2xl flex flex-col justify-between">
          <div>
            <h3 class="text-lg font-bold text-white pb-3 border-b border-slate-800 flex items-center">
              <i class="fa-solid fa-qrcode text-amber-400 mr-2"></i>Propuesta de Adelanto & Desembolso
            </h3>

            <div id="sim-empty-state" class="py-12 text-center text-slate-500">
              <i class="fa-solid fa-seedling text-4xl mb-3 text-slate-600"></i>
              <p>Presiona "Calcular Capacidad de Factoring" para consultar al oráculo ML.</p>
            </div>

            <div id="sim-result-box" class="hidden space-y-4 mt-4">
              <div class="flex items-center justify-between p-3 bg-slate-900 rounded-lg border border-slate-800">
                <div>
                  <div class="text-[10px] uppercase text-slate-400 font-bold">Nivel de Riesgo Evaluado</div>
                  <div id="res-risk-tier" class="text-lg font-extrabold text-emerald-400">RIESGO BAJO</div>
                </div>
                <div class="text-right">
                  <div class="text-[10px] uppercase text-slate-400 font-bold">Score de Riesgo</div>
                  <div id="res-risk-score" class="text-lg font-extrabold text-white">24.5 / 100</div>
                </div>
              </div>

              <div class="grid grid-cols-2 gap-3">
                <div class="p-3 bg-slate-900 rounded-lg border border-slate-800">
                  <div class="text-[10px] text-slate-400 uppercase font-semibold">% Adelanto Pre-aprobado</div>
                  <div id="res-advance-pct" class="text-xl font-extrabold text-amber-400">53.0%</div>
                </div>
                <div class="p-3 bg-slate-900 rounded-lg border border-slate-800">
                  <div class="text-[10px] text-slate-400 uppercase font-semibold">Monto Máximo Aprobado</div>
                  <div id="res-advance-amount" class="text-xl font-extrabold text-emerald-400">$3,816.00 <span class="text-xs text-slate-300 font-normal">USDC</span></div>
                </div>
              </div>

              <!-- Risk explanations list -->
              <div class="p-3 bg-slate-900/60 rounded-lg border border-slate-800">
                <div class="text-[11px] font-bold text-slate-300 uppercase mb-2">Diagnóstico Agronómico del Oráculo:</div>
                <ul id="res-factors-list" class="space-y-1 text-xs text-slate-400 list-disc list-inside"></ul>
              </div>

              <!-- Execution Form -->
              <div class="pt-3 border-t border-slate-800 space-y-3">
                <div class="flex items-center justify-between text-xs">
                  <span class="text-slate-300 font-semibold">Monto a Desembolsar (USDC):</span>
                  <input type="number" id="exec-requested-amount" class="w-32 bg-slate-900 border border-slate-700 rounded px-2 py-1 text-right text-white font-bold" value="800">
                </div>
                <button onclick="executeLoan()" id="btn-exec-loan" class="w-full py-3 bg-gradient-to-r from-amber-500 to-emerald-600 hover:from-amber-400 hover:to-emerald-500 text-slate-950 font-black rounded-lg shadow-xl transition">
                  <i class="fa-solid fa-bolt mr-2"></i>Desembolsar Ahora (QR Simple BOB)
                </button>
              </div>
            </div>
          </div>

          <!-- Pollar QR Output Modal / View -->
          <div id="qr-modal-view" class="hidden mt-4 p-4 bg-slate-900 border border-amber-500/40 rounded-xl space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-amber-400 uppercase flex items-center">
                <i class="fa-solid fa-qrcode mr-2"></i>Pollar · Simple QR en Bolivianos
              </span>
              <span class="text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-mono">ACTIVE_ESCROW</span>
            </div>
            <div class="bg-white p-3 rounded-lg flex flex-col items-center justify-center text-slate-900">
              <!-- Dummy visual QR pattern -->
              <div class="w-36 h-36 bg-slate-100 flex items-center justify-center border-2 border-dashed border-slate-300 rounded text-center p-2">
                <i class="fa-solid fa-qrcode text-6xl text-slate-800"></i>
              </div>
              <div class="mt-2 text-center">
                <div class="text-xs font-black" id="qr-amount-bob">Bs. 5,568.00</div>
                <div class="text-[10px] text-slate-500 font-mono" id="qr-payout-id">pol_out_...</div>
              </div>
            </div>
            <div class="text-[10px] text-slate-400 space-y-1">
              <div>• <strong>Vaquita Pool:</strong> <span id="qr-vaquita-res" class="font-mono text-slate-300">vaq_res_...</span></div>
              <div>• <strong>Trustless Work Escrow:</strong> <span id="qr-escrow-id" class="font-mono text-slate-300">escrow_tw_...</span></div>
            </div>
            <a id="qr-deep-link" href="#" target="_blank" class="block text-center py-1.5 bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold rounded text-xs">
              Abrir en Pollar Wallet App
            </a>
          </div>

        </div>
      </div>
    </div>

    <!-- TAB 5: TWO-STAGE ML FORECAST -->
    <div id="tab-ml-forecast" class="tab-content hidden space-y-6">
      <div class="border-b border-slate-800 pb-3">
        <h1 class="text-2xl font-bold text-white flex items-center">
          <i class="fa-solid fa-wand-magic-sparkles text-amber-400 mr-2"></i>Modelo Two-Stage (LightGBM) & Pronóstico de Precios
        </h1>
        <p class="text-sm text-slate-400 mt-1">
          Etapa 1: Clasificación de árboles con/sin fruto P(y &gt; 0) + Etapa 2: Regresión logarítmica de rendimiento + Modelo estocástico de precios ICCO.
        </p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Panel 1: Estimación de Rendimiento por Biometría -->
        <div class="glass-card rounded-xl border border-slate-800 p-6 shadow-xl space-y-4">
          <h2 class="text-lg font-bold text-white flex items-center">
            <i class="fa-solid fa-tree text-emerald-400 mr-2"></i>Predicción de Rendimiento de Cacao
          </h2>
          <div class="grid grid-cols-2 gap-3 text-xs">
            <div>
              <label class="block text-slate-400 mb-1">Altura Árbol (cm)</label>
              <input type="number" id="ml-height" value="170" class="w-full bg-slate-900 border border-slate-700 rounded px-2.5 py-1.5 text-white">
            </div>
            <div>
              <label class="block text-slate-400 mb-1">Diámetro Tronco (cm)</label>
              <input type="number" id="ml-diam" value="8.0" step="0.1" class="w-full bg-slate-900 border border-slate-700 rounded px-2.5 py-1.5 text-white">
            </div>
            <div>
              <label class="block text-slate-400 mb-1">Conteo de Hojas</label>
              <input type="number" id="ml-leaves" value="260" class="w-full bg-slate-900 border border-slate-700 rounded px-2.5 py-1.5 text-white">
            </div>
            <div>
              <label class="block text-slate-400 mb-1">Cherelles por Árbol</label>
              <input type="number" id="ml-cherelle" value="0.3" step="0.1" class="w-full bg-slate-900 border border-slate-700 rounded px-2.5 py-1.5 text-white">
            </div>
            <div>
              <label class="block text-slate-400 mb-1">Árboles por Hectárea</label>
              <input type="number" id="ml-density" value="1111" class="w-full bg-slate-900 border border-slate-700 rounded px-2.5 py-1.5 text-white">
            </div>
            <div>
              <label class="block text-slate-400 mb-1">Variedad</label>
              <select id="ml-variety" class="w-full bg-slate-900 border border-slate-700 rounded px-2.5 py-1.5 text-white">
                <option value="Nacional">Nacional (Alto Beni)</option>
                <option value="Criollo">Criollo Silvestre</option>
                <option value="CCN-51">CCN-51</option>
              </select>
            </div>
          </div>
          <button onclick="estimateYield()" id="btn-ml-yield" class="w-full py-2.5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold rounded-lg shadow text-xs transition">
            <i class="fa-solid fa-microchip mr-2"></i>Inferir Rendimiento (Two-Stage)
          </button>

          <!-- Yield Result Box -->
          <div id="ml-yield-result" class="hidden p-4 bg-slate-900/80 rounded-lg border border-emerald-500/30 space-y-2 text-xs">
            <div class="text-[10px] uppercase text-slate-400 font-bold">Resultado Two-Stage LightGBM</div>
            <div class="flex justify-between items-baseline">
              <span class="text-slate-300">Rendimiento por Árbol:</span>
              <span id="res-yield-g" class="text-base font-extrabold text-emerald-400">0.00 g/árbol</span>
            </div>
            <div class="flex justify-between items-baseline">
              <span class="text-slate-300">Rendimiento por Hectárea:</span>
              <span id="res-yield-ha" class="text-base font-extrabold text-amber-400">0.00 kg/ha</span>
            </div>
            <div class="flex justify-between text-[11px] text-slate-400 pt-1 border-t border-slate-800">
              <span>Probabilidad Cosecha Positiva P(y&gt;0):</span>
              <span id="res-yield-prob" class="font-bold text-white">0%</span>
            </div>
          </div>
        </div>

        <!-- Panel 2: Pronóstico de Precios -->
        <div class="glass-card rounded-xl border border-slate-800 p-6 shadow-xl space-y-4">
          <h2 class="text-lg font-bold text-white flex items-center">
            <i class="fa-solid fa-chart-line text-blue-400 mr-2"></i>Pronóstico de Precios de Cacao (ICCO)
          </h2>
          <div class="grid grid-cols-2 gap-3 text-xs">
            <div>
              <label class="block text-slate-400 mb-1">Horizonte Temporal</label>
              <select id="ml-horizon" class="w-full bg-slate-900 border border-slate-700 rounded px-2.5 py-1.5 text-white">
                <option value="15">15 Días</option>
                <option value="30" selected>30 Días (1 Mes)</option>
                <option value="60">60 Días (2 Meses)</option>
                <option value="90">90 Días (Cosecha)</option>
              </select>
            </div>
            <div>
              <label class="block text-slate-400 mb-1">Precio Actual ($/kg USDC)</label>
              <input type="number" id="ml-current-price" value="4.80" step="0.05" class="w-full bg-slate-900 border border-slate-700 rounded px-2.5 py-1.5 text-white">
            </div>
          </div>
          <button onclick="forecastPrice()" id="btn-ml-price" class="w-full py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold rounded-lg shadow text-xs transition">
            <i class="fa-solid fa-arrow-trend-up mr-2"></i>Simular Trayectoria de Precios
          </button>

          <!-- Price Result Box -->
          <div id="ml-price-result" class="hidden p-4 bg-slate-900/80 rounded-lg border border-blue-500/30 space-y-2 text-xs">
            <div class="flex items-center justify-between">
              <span class="text-[10px] uppercase text-slate-400 font-bold">Proyección a <span id="res-price-days">30</span> días</span>
              <span id="res-price-trend" class="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-500/20 text-blue-300">NEUTRAL</span>
            </div>
            <div class="flex justify-between items-baseline">
              <span class="text-slate-300">Precio Esperado:</span>
              <span id="res-price-val" class="text-lg font-extrabold text-blue-400">$4.80 USDC/kg</span>
            </div>
            <div class="flex justify-between text-[11px] text-slate-400 pt-1 border-t border-slate-800">
              <span>Intervalo de Confianza (95%):</span>
              <span id="res-price-ci" class="font-bold text-white">[$4.41 - $5.22]</span>
            </div>
          </div>
        </div>
      </div>
    </div>

  </main>

  <!-- Footer -->
  <footer class="border-t border-slate-800 py-6 text-center text-xs text-slate-500">
    <p>Ayni Cacao · Hackathon Stellar 2026 · Desarrollado con Clean Architecture, Soroban & Machine Learning</p>
  </footer>

  <script>
    // Tab switching logic
    function switchTab(tabName) {
      document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('text-amber-400', 'bg-slate-800/80');
        btn.classList.add('text-slate-300');
      });

      const target = document.getElementById('tab-' + tabName);
      if (target) target.classList.remove('hidden');

      const activeBtn = document.querySelector(`[data-tab="${tabName}"]`);
      if (activeBtn) {
        activeBtn.classList.remove('text-slate-300');
        activeBtn.classList.add('text-amber-400', 'bg-slate-800/80');
      }

      if (tabName === 'dashboard') loadDashboardData();
      if (tabName === 'producers') loadProducersData();
    }

    // Weather label updater
    function updateWeatherLabels() {
      const rainfall = parseInt(document.getElementById('fac-rainfall').value);
      const humidity = parseInt(document.getElementById('fac-humidity').value);

      const rLabel = document.getElementById('label-rainfall');
      if (rainfall < 80) {
        rLabel.textContent = `${rainfall} mm (Sequía)`;
        rLabel.className = 'text-xs font-bold text-red-400';
      } else if (rainfall > 240) {
        rLabel.textContent = `${rainfall} mm (Alerta Plagas)`;
        rLabel.className = 'text-xs font-bold text-amber-400';
      } else {
        rLabel.textContent = `${rainfall} mm (Óptimo)`;
        rLabel.className = 'text-xs font-bold text-emerald-400';
      }

      const hLabel = document.getElementById('label-humidity');
      if (humidity > 85) {
        hLabel.textContent = `${humidity}% (Riesgo Fungoso)`;
        hLabel.className = 'text-xs font-bold text-amber-400';
      } else {
        hLabel.textContent = `${humidity}% (Seguro)`;
        hLabel.className = 'text-xs font-bold text-emerald-400';
      }
    }

    // Delivery calculation preview
    function calculatePreview() {
      const type = document.getElementById('del-cacao-type').value;
      const gross = parseFloat(document.getElementById('del-gross-weight').value) || 0;
      const moisture = parseFloat(document.getElementById('del-moisture').value) || 0;
      const grade = document.getElementById('del-quality').value;
      const basePrice = 4.80;

      let netWeight = gross;
      if (type === 'BABA') {
        netWeight = gross * 0.33;
      } else if (type === 'SECO' && moisture > 7.5) {
        const excess = (moisture - 7.5) / 100.0;
        netWeight = gross * (1.0 - excess);
      }

      let gradeMult = 1.0;
      if (grade === 'B') gradeMult = 0.90;
      if (grade === 'C') gradeMult = 0.75;

      const finalPrice = basePrice * gradeMult;
      const totalUSDC = netWeight * finalPrice;
      const totalBOB = totalUSDC * 6.96;

      document.getElementById('preview-net-weight').textContent = netWeight.toFixed(2) + ' kg';
      document.getElementById('preview-price-kg').textContent = '$' + finalPrice.toFixed(2) + ' USDC';
      document.getElementById('preview-total').innerHTML = `$${totalUSDC.toFixed(2)} USDC <span class="text-xs text-slate-300">(Bs. ${totalBOB.toFixed(2)})</span>`;
    }

    // Load Dashboard Metrics
    async function loadDashboardData() {
      try {
        const res = await fetch('/api/v1/dashboard');
        if (!res.ok) return;
        const data = await res.json();

        // Update Pool stats
        document.getElementById('stat-pool-avail').textContent = '$' + data.pool_status.available_liquidity_usdc.toLocaleString('en-US', {minimumFractionDigits: 2});
        document.getElementById('stat-pool-total').textContent = '$' + data.pool_status.total_liquidity_usdc.toLocaleString('en-US', {minimumFractionDigits: 2});
        document.getElementById('stat-pool-res').textContent = '$' + data.pool_status.reserved_liquidity_usdc.toLocaleString('en-US', {minimumFractionDigits: 2});

        // Total advanced
        document.getElementById('stat-total-usdc').textContent = '$' + data.total_advanced_usdc.toLocaleString('en-US', {minimumFractionDigits: 2});
        document.getElementById('stat-total-bob').textContent = 'Bs. ' + data.total_advanced_bob.toLocaleString('en-US', {minimumFractionDigits: 2});
        document.getElementById('stat-deliveries-count').textContent = data.total_deliveries_count;
        document.getElementById('stat-active-loans').textContent = data.active_loans_count;

        // Populate table
        const tbody = document.getElementById('recent-deliveries-body');
        if (data.recent_deliveries && data.recent_deliveries.length > 0) {
          tbody.innerHTML = data.recent_deliveries.map(d => `
            <tr class="hover:bg-slate-800/40">
              <td class="px-4 py-3 font-mono font-bold text-amber-400 text-xs">${d.delivery_code}</td>
              <td class="px-4 py-3 font-medium text-white">${d.producer_name || 'Socio #' + d.producer_id}</td>
              <td class="px-4 py-3">
                <span class="px-2 py-0.5 rounded text-xs ${d.cacao_type === 'BABA' ? 'bg-amber-500/20 text-amber-300' : 'bg-emerald-500/20 text-emerald-300'}">
                  ${d.cacao_type} - Grado ${d.quality_grade}
                </span>
              </td>
              <td class="px-4 py-3 text-xs">
                ${d.gross_weight_kg} kg &rarr; <strong class="text-white">${d.net_dry_weight_kg} kg seco</strong>
              </td>
              <td class="px-4 py-3 text-xs">
                <strong class="text-emerald-400">$${d.total_amount_usdc.toFixed(2)}</strong>
                <span class="text-slate-400 block text-[10px]">Bs. ${d.total_amount_bob.toFixed(2)}</span>
              </td>
              <td class="px-4 py-3 text-[11px] font-mono text-slate-400 truncate max-w-xs" title="${d.stellar_tx_hash}">
                <i class="fa-solid fa-link text-blue-400 mr-1"></i>${d.stellar_tx_hash.substring(0, 16)}...
              </td>
              <td class="px-4 py-3">
                <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-blue-500/20 text-blue-400 border border-blue-500/30">
                  ${d.status}
                </span>
              </td>
            </tr>
          `).join('');
        }
      } catch (err) {
        console.error('Error fetching dashboard:', err);
      }
    }

    // Load Producers
    async function loadProducersData() {
      try {
        const res = await fetch('/api/v1/producers');
        if (!res.ok) return;
        const producers = await res.json();

        const grid = document.getElementById('producers-grid');
        grid.innerHTML = producers.map(p => `
          <div class="glass-card rounded-xl border border-slate-800 p-5 shadow-lg space-y-4">
            <div class="flex items-start justify-between">
              <div>
                <h3 class="font-bold text-white text-base">${p.name}</h3>
                <p class="text-xs text-amber-400 font-medium">${p.cooperative}</p>
                <p class="text-xs text-slate-400">${p.community}</p>
              </div>
              <span class="px-2 py-0.5 rounded text-[10px] font-black ${
                p.risk_tier === 'BAJO' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' :
                p.risk_tier === 'MEDIO' ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' :
                'bg-red-500/20 text-red-400 border border-red-500/30'
              }">
                RIESGO ${p.risk_tier}
              </span>
            </div>

            <div class="bg-slate-900/80 rounded-lg p-3 text-xs space-y-1.5 border border-slate-800 font-mono">
              <div class="flex justify-between text-slate-400">
                <span>Parcela EUDR:</span>
                <span class="text-slate-200 font-bold">${p.eudr_plot_code}</span>
              </div>
              <div class="flex justify-between text-slate-400">
                <span>Superficie:</span>
                <span class="text-slate-200">${p.parcel_hectares} ha</span>
              </div>
              <div class="flex justify-between text-slate-400">
                <span>Coordenadas GPS:</span>
                <span class="text-emerald-400 text-[11px]">${p.eudr_latitude}, ${p.eudr_longitude}</span>
              </div>
              <div class="flex justify-between text-slate-400">
                <span>Certificación Cero Deforestación:</span>
                <span class="${p.eudr_certified ? 'text-emerald-400 font-bold' : 'text-slate-500'}">
                  ${p.eudr_certified ? '✓ EUDR VÁLIDO' : 'En proceso'}
                </span>
              </div>
            </div>

            <div class="flex items-center justify-between text-xs pt-1 border-t border-slate-800 text-slate-400">
              <span>Score Cumplimiento:</span>
              <span class="font-bold text-white">${(p.compliance_score * 100).toFixed(0)}%</span>
            </div>
          </div>
        `).join('');
      } catch (err) {
        console.error('Error fetching producers:', err);
      }
    }

    // Submit Delivery Ticket
    async function submitDelivery(e) {
      e.preventDefault();
      const btn = document.getElementById('btn-submit-delivery');
      btn.disabled = true;
      btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-2"></i>Notarizando en Stellar...';

      const payload = {
        producer_id: parseInt(document.getElementById('del-producer-id').value),
        cacao_type: document.getElementById('del-cacao-type').value,
        gross_weight_kg: parseFloat(document.getElementById('del-gross-weight').value),
        moisture_percentage: parseFloat(document.getElementById('del-moisture').value),
        quality_grade: document.getElementById('del-quality').value,
        base_price_per_kg_usdc: 4.80
      };

      try {
        const res = await fetch('/api/v1/deliveries', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();

        if (res.ok) {
          const resBox = document.getElementById('delivery-result-box');
          const resContent = document.getElementById('delivery-result-content');
          resBox.classList.remove('hidden');
          resContent.innerHTML = `
            <div>• <strong>Código Boleta:</strong> ${data.delivery_code}</div>
            <div>• <strong>Peso Neto Seco:</strong> ${data.net_dry_weight_kg} kg (Penalización: ${data.penalty_discount_kg} kg)</div>
            <div>• <strong>Total Liquidado:</strong> $${data.total_amount_usdc} USDC (Bs. ${data.total_amount_bob})</div>
            <div>• <strong>Payload SHA-256:</strong> ${data.payload_hash}</div>
            <div>• <strong>Stellar TX Hash:</strong> <span class="text-emerald-400 font-bold">${data.stellar_tx_hash}</span></div>
          `;
          loadDashboardData();
        } else {
          alert('Error al registrar boleta: ' + (data.detail || 'Error desconocido'));
        }
      } catch (err) {
        alert('Error de conexión: ' + err.message);
      } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-stamp mr-2"></i>Emitir Boleta & Notarizar en Stellar';
      }
    }

    // Run ML Factoring Simulation
    let currentSimulation = null;
    async function runSimulation() {
      const btn = document.getElementById('btn-simulate');
      btn.disabled = true;
      btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-2"></i>Consultando Oráculo ML...';

      const payload = {
        producer_id: parseInt(document.getElementById('fac-producer-id').value),
        expected_harvest_kg: parseFloat(document.getElementById('fac-expected-kg').value),
        rainfall_mm: parseFloat(document.getElementById('fac-rainfall').value),
        humidity_pct: parseFloat(document.getElementById('fac-humidity').value)
      };

      try {
        const res = await fetch('/api/v1/factoring/simulate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();

        if (res.ok) {
          currentSimulation = data;
          document.getElementById('sim-empty-state').classList.add('hidden');
          const resultBox = document.getElementById('sim-result-box');
          resultBox.classList.remove('hidden');

          document.getElementById('res-risk-tier').textContent = 'RIESGO ' + data.risk_level;
          document.getElementById('res-risk-tier').className = 'text-lg font-extrabold ' + (
            data.risk_level === 'BAJO' ? 'text-emerald-400' :
            data.risk_level === 'MEDIO' ? 'text-amber-400' : 'text-red-400'
          );
          document.getElementById('res-risk-score').textContent = data.risk_score + ' / 100';
          document.getElementById('res-advance-pct').textContent = data.approved_advance_pct + '%';
          document.getElementById('res-advance-amount').innerHTML = '$' + data.max_advance_usdc.toFixed(2) + ' <span class="text-xs text-slate-300 font-normal">USDC (Bs. ' + data.max_advance_bob.toFixed(2) + ')</span>';

          document.getElementById('exec-requested-amount').value = Math.min(800, data.max_advance_usdc);

          // List factors
          const list = document.getElementById('res-factors-list');
          list.innerHTML = data.risk_factors.map(f => `<li>${f}</li>`).join('');
        }
      } catch (err) {
        alert('Error en simulación: ' + err.message);
      } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-calculator mr-2"></i>Calcular Capacidad de Factoring';
      }
    }

    // Execute Loan & Pollar QR Simple
    async function executeLoan() {
      const btn = document.getElementById('btn-exec-loan');
      btn.disabled = true;
      btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-2"></i>Reservando Vaquita & Generando QR...';

      const payload = {
        producer_id: parseInt(document.getElementById('fac-producer-id').value),
        requested_amount_usdc: parseFloat(document.getElementById('exec-requested-amount').value),
        expected_harvest_kg: parseFloat(document.getElementById('fac-expected-kg').value),
        rainfall_mm: parseFloat(document.getElementById('fac-rainfall').value),
        humidity_pct: parseFloat(document.getElementById('fac-humidity').value)
      };

      try {
        const res = await fetch('/api/v1/factoring/execute', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();

        if (res.ok) {
          const qrView = document.getElementById('qr-modal-view');
          qrView.classList.remove('hidden');

          document.getElementById('qr-amount-bob').textContent = 'Bs. ' + data.amount_bob.toFixed(2);
          document.getElementById('qr-payout-id').textContent = data.pollar_payout_id;
          document.getElementById('qr-vaquita-res').textContent = data.vaquita_reservation_id;
          document.getElementById('qr-escrow-id').textContent = data.trustless_escrow_id;
          document.getElementById('qr-deep-link').href = data.qr_deep_link;

          loadDashboardData();
        } else {
          alert('Error al ejecutar factoring: ' + (data.detail || 'Error desconocido'));
        }
      } catch (err) {
        alert('Error de conexión: ' + err.message);
      } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-bolt mr-2"></i>Desembolsar Ahora (QR Simple BOB)';
      }
    }

    // Yield Estimation with Two-Stage LightGBM
    async function estimateYield() {
      const btn = document.getElementById('btn-ml-yield');
      btn.disabled = true;
      btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-2"></i>Calculando con LightGBM...';

      const payload = {
        tree_height: parseFloat(document.getElementById('ml-height').value) || 170.0,
        diameter: parseFloat(document.getElementById('ml-diam').value) || 8.0,
        leaf_count: parseFloat(document.getElementById('ml-leaves').value) || 260.0,
        cherelle: parseFloat(document.getElementById('ml-cherelle').value) || 0.3,
        n_trees: parseInt(document.getElementById('ml-density').value) || 1111,
        variedad: document.getElementById('ml-variety').value
      };

      try {
        const res = await fetch('/api/v1/ml/yield/estimate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (res.ok) {
          document.getElementById('ml-yield-result').classList.remove('hidden');
          document.getElementById('res-yield-g').textContent = data.predicted_yield_g_per_tree.toFixed(2) + ' g/árbol';
          document.getElementById('res-yield-ha').textContent = data.predicted_yield_kg_per_ha.toFixed(2) + ' kg/ha';
          document.getElementById('res-yield-prob').textContent = (data.prob_positive_yield * 100).toFixed(1) + '%';
        } else {
          alert('Error en estimación: ' + (data.detail || 'Error'));
        }
      } catch (err) {
        alert('Error de conexión: ' + err.message);
      } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-microchip mr-2"></i>Inferir Rendimiento (Two-Stage)';
      }
    }

    // Cacao Price Forecast
    async function forecastPrice() {
      const btn = document.getElementById('btn-ml-price');
      btn.disabled = true;
      btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-2"></i>Simulando precios...';

      const horizon = parseInt(document.getElementById('ml-horizon').value) || 30;
      const currentPrice = parseFloat(document.getElementById('ml-current-price').value) || 4.80;

      try {
        const res = await fetch('/api/v1/ml/prices/forecast', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ horizon_days: horizon, current_price_usdc: currentPrice })
        });
        const data = await res.json();
        if (res.ok) {
          document.getElementById('ml-price-result').classList.remove('hidden');
          document.getElementById('res-price-days').textContent = data.horizon_days;
          document.getElementById('res-price-val').textContent = '$' + data.forecast_price_usdc_per_kg.toFixed(2) + ' USDC/kg';
          document.getElementById('res-price-ci').textContent = `[$${data.confidence_lower.toFixed(2)} - $${data.confidence_upper.toFixed(2)}]`;
          
          const trendSpan = document.getElementById('res-price-trend');
          trendSpan.textContent = data.trend.toUpperCase();
          if (data.trend === 'bullish') {
            trendSpan.className = 'px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-400';
          } else if (data.trend === 'bearish') {
            trendSpan.className = 'px-2 py-0.5 rounded text-[10px] font-bold bg-red-500/20 text-red-400';
          } else {
            trendSpan.className = 'px-2 py-0.5 rounded text-[10px] font-bold bg-blue-500/20 text-blue-300';
          }
        } else {
          alert('Error en pronóstico: ' + (data.detail || 'Error'));
        }
      } catch (err) {
        alert('Error de conexión: ' + err.message);
      } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-arrow-trend-up mr-2"></i>Simular Trayectoria de Precios';
      }
    }

    // Initial boot
    document.addEventListener('DOMContentLoaded', () => {
      calculatePreview();
      loadDashboardData();
    });
  </script>
</body>
</html>
"""
