"""Embedded Interactive Web Application UI for KAIRO 3.0.

Professional AgriTech & FinTech SaaS UI with clean white/black identity,
warm agricultural accents (#C76A32, #3F7D44, #75452D, #D5A332, #A74445),
official transparent mascot integration, and responsive navigation.
"""

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="es" class="h-full">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>KAIRO 3.0 — Acopio Transparente, Trazabilidad EUDR y Factoring Agrícola</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
  
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Plus Jakarta Sans"', 'system-ui', 'sans-serif'],
            mono: ['ui-monospace', 'SFMono-Regular', 'Menlo', 'monospace'],
            display: ['"Space Grotesk"', 'sans-serif'],
          },
          colors: {
            kairo: {
              bg: '#FAFAF8',
              card: '#FFFFFF',
              alt: '#F4F4F0',
              border: '#E5E5E0',
              borderLight: '#EFEFEA',
              text: '#171717',
              muted: '#626262',
              cacao: '#C76A32',
              cacaoHover: '#B25A25',
              cacaoDark: '#75452D',
              green: '#3F7D44',
              greenLight: '#EBF4EC',
              gold: '#D5A332',
              goldLight: '#FEF9EC',
              red: '#A74445',
              redLight: '#FDF2F2',
            }
          },
          boxShadow: {
            'subtle': '0 1px 3px rgba(0, 0, 0, 0.05), 0 1px 2px rgba(0, 0, 0, 0.03)',
            'card': '0 4px 12px -2px rgba(0, 0, 0, 0.05), 0 2px 6px -1px rgba(0, 0, 0, 0.03)',
            'elevated': '0 10px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.03)',
          }
        }
      }
    }
  </script>

  <style>
    body {
      background-color: #FAFAF8;
      color: #171717;
      font-feature-settings: 'cv02', 'cv03', 'cv04', 'cv11';
    }
    .custom-scrollbar::-webkit-scrollbar {
      height: 6px;
      width: 6px;
    }
    .custom-scrollbar::-webkit-scrollbar-track {
      background: #F4F4F0;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
      background: #D5D5CF;
      border-radius: 9999px;
    }
    .nav-tab-active {
      background-color: #171717 !important;
      color: #FFFFFF !important;
      font-weight: 600 !important;
    }
    .mascot-shadow {
      filter: drop-shadow(0 12px 16px rgba(117, 69, 45, 0.15));
    }
  </style>
</head>
<body class="min-h-full flex flex-col antialiased bg-[#FAFAF8] text-[#171717]">

  <!-- Top Global Header / Navigation -->
  <header class="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-[#E5E5E0] shadow-subtle">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        
        <!-- Brand Logo & Identity -->
        <div class="flex items-center space-x-3 cursor-pointer" onclick="switchTab('dashboard')">
          <div class="w-10 h-10 rounded-xl bg-[#C76A32]/10 border border-[#C76A32]/20 flex items-center justify-center p-1 overflow-hidden">
            <img src="/static/kairo-mascot-transparent.png" alt="KAIRO" class="w-full h-full object-contain" onerror="this.src='/kairo-mascot-transparent.png'">
          </div>
          <div>
            <div class="flex items-center space-x-1.5">
              <span class="font-display text-xl font-extrabold tracking-tight text-[#171717]">KAIRO</span>
              <span class="text-[11px] font-bold px-1.5 py-0.5 rounded bg-[#C76A32] text-white">3.0</span>
            </div>
            <p class="text-[11px] text-[#626262] font-medium leading-none">Alto Beni · Palos Blancos · Sapecho</p>
          </div>
        </div>

        <!-- Desktop Navigation Tabs (Ensured zero wrap, zero clipping) -->
        <nav class="hidden lg:flex items-center space-x-1 bg-[#F4F4F0] p-1 rounded-xl border border-[#E5E5E0]" id="nav-tabs-desktop" aria-label="Navegación principal">
          <button onclick="switchTab('dashboard')" class="tab-btn nav-tab-active px-3 py-1.5 rounded-lg text-xs font-medium text-[#626262] hover:text-[#171717] transition-all flex items-center space-x-1.5" data-tab="dashboard">
            <i class="fa-solid fa-chart-pie text-xs"></i>
            <span>Dashboard</span>
          </button>
          <button onclick="switchTab('producers')" class="tab-btn px-3 py-1.5 rounded-lg text-xs font-medium text-[#626262] hover:text-[#171717] transition-all flex items-center space-x-1.5" data-tab="producers">
            <i class="fa-solid fa-leaf text-xs"></i>
            <span>EUDR & Parcelas</span>
          </button>
          <button onclick="switchTab('deliveries')" class="tab-btn px-3 py-1.5 rounded-lg text-xs font-medium text-[#626262] hover:text-[#171717] transition-all flex items-center space-x-1.5" data-tab="deliveries">
            <i class="fa-solid fa-scale-balanced text-xs"></i>
            <span>Acopio de Cacao</span>
          </button>
          <button onclick="switchTab('factoring')" class="tab-btn px-3 py-1.5 rounded-lg text-xs font-medium text-[#626262] hover:text-[#171717] transition-all flex items-center space-x-1.5" data-tab="factoring">
            <i class="fa-solid fa-seedling text-xs"></i>
            <span>Factoring ML</span>
          </button>
          <button onclick="switchTab('ml-forecast')" class="tab-btn px-3 py-1.5 rounded-lg text-xs font-medium text-[#626262] hover:text-[#171717] transition-all flex items-center space-x-1.5" data-tab="ml-forecast">
            <i class="fa-solid fa-brain text-xs"></i>
            <span>Two-Stage ML</span>
          </button>
          <button onclick="switchTab('progress')" class="tab-btn px-3 py-1.5 rounded-lg text-xs font-medium text-[#626262] hover:text-[#171717] transition-all flex items-center space-x-1.5" data-tab="progress">
            <i class="fa-solid fa-trophy text-xs text-[#D5A332]"></i>
            <span>Progreso</span>
          </button>
        </nav>

        <!-- Right System Badges & Actions -->
        <div class="flex items-center space-x-2.5">
          <!-- Auto-Demo Action Button -->
          <button onclick="startAutoDemo()" id="btn-auto-demo" class="px-3.5 py-1.5 rounded-xl bg-gradient-to-r from-[#C76A32] to-[#D5A332] hover:brightness-110 text-white text-xs font-extrabold shadow-sm transition flex items-center space-x-1.5 animate-pulse" title="Ejecutar demostración automática paso a paso para grabación de pantalla">
            <i class="fa-solid fa-circle-play text-xs"></i>
            <span class="hidden sm:inline">Auto-Demo (2m 30s)</span>
            <span class="sm:hidden">Auto-Demo</span>
          </button>

          <!-- Stellar Ledger Badge -->
          <div class="hidden sm:flex items-center space-x-1.5 px-2.5 py-1 rounded-full text-[11px] font-semibold bg-[#3F7D44]/10 text-[#3F7D44] border border-[#3F7D44]/20" title="Conectado al libro contable de Stellar Testnet">
            <span class="w-2 h-2 rounded-full bg-[#3F7D44] animate-pulse"></span>
            <span>Stellar Testnet</span>
          </div>

          <!-- Swagger Docs Link -->
          <a href="/docs" target="_blank" rel="noopener" class="hidden md:flex items-center space-x-1 px-2.5 py-1 rounded-lg text-xs font-medium bg-white text-[#626262] hover:text-[#171717] border border-[#E5E5E0] hover:border-[#171717] transition">
            <i class="fa-solid fa-code text-[11px]"></i>
            <span>API Docs</span>
          </a>

          <!-- Mobile Hamburger Toggle -->
          <button type="button" onclick="toggleMobileMenu()" class="lg:hidden p-2 rounded-lg text-[#171717] bg-[#F4F4F0] border border-[#E5E5E0] hover:bg-[#E5E5E0] transition" aria-label="Abrir menú de navegación">
            <i class="fa-solid fa-bars text-sm"></i>
          </button>
        </div>

      </div>

      <!-- Mobile Navigation Drawer -->
      <div id="mobile-menu" class="hidden lg:hidden border-t border-[#E5E5E0] py-3 space-y-1">
        <button onclick="switchTab('dashboard'); toggleMobileMenu()" class="w-full text-left px-3 py-2 rounded-lg text-xs font-semibold text-[#171717] hover:bg-[#F4F4F0] flex items-center space-x-2">
          <i class="fa-solid fa-chart-pie w-5 text-[#C76A32]"></i>
          <span>Dashboard Principal</span>
        </button>
        <button onclick="switchTab('producers'); toggleMobileMenu()" class="w-full text-left px-3 py-2 rounded-lg text-xs font-semibold text-[#171717] hover:bg-[#F4F4F0] flex items-center space-x-2">
          <i class="fa-solid fa-leaf w-5 text-[#3F7D44]"></i>
          <span>EUDR & Trazabilidad de Parcelas</span>
        </button>
        <button onclick="switchTab('deliveries'); toggleMobileMenu()" class="w-full text-left px-3 py-2 rounded-lg text-xs font-semibold text-[#171717] hover:bg-[#F4F4F0] flex items-center space-x-2">
          <i class="fa-solid fa-scale-balanced w-5 text-[#75452D]"></i>
          <span>Acopio de Cacao & Boleta</span>
        </button>
        <button onclick="switchTab('factoring'); toggleMobileMenu()" class="w-full text-left px-3 py-2 rounded-lg text-xs font-semibold text-[#171717] hover:bg-[#F4F4F0] flex items-center space-x-2">
          <i class="fa-solid fa-seedling w-5 text-[#D5A332]"></i>
          <span>Factoring ML & Oráculo</span>
        </button>
        <button onclick="switchTab('ml-forecast'); toggleMobileMenu()" class="w-full text-left px-3 py-2 rounded-lg text-xs font-semibold text-[#171717] hover:bg-[#F4F4F0] flex items-center space-x-2">
          <i class="fa-solid fa-brain w-5 text-indigo-600"></i>
          <span>Two-Stage ML Rendimiento & Precios</span>
        </button>
        <button onclick="switchTab('progress'); toggleMobileMenu()" class="w-full text-left px-3 py-2 rounded-lg text-xs font-semibold text-[#171717] hover:bg-[#F4F4F0] flex items-center space-x-2">
          <i class="fa-solid fa-trophy w-5 text-[#D5A332]"></i>
          <span>Progreso & Puntos KAIRO</span>
        </button>
      </div>
    </div>
  </header>

  <!-- Main Workspace Container -->
  <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">

    <!-- ==================================================================== -->
    <!-- TAB 1: DASHBOARD PRINCIPAL                                           -->
    <!-- ==================================================================== -->
    <div id="tab-dashboard" class="tab-content space-y-6">
      
      <!-- Welcome Hero Banner with Official KAIRO Mascot -->
      <section class="relative bg-gradient-to-br from-white via-[#FAF7F3] to-[#F5ECE1] rounded-2xl border border-[#E5E5E0] p-6 sm:p-8 shadow-card overflow-hidden">
        <div class="grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
          
          <div class="md:col-span-8 space-y-3">
            <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-[#C76A32]/10 border border-[#C76A32]/20 text-[#C76A32] text-xs font-semibold">
              <i class="fa-solid fa-shield-check"></i>
              <span>Plataforma Oficial Cooperativas del Norte de La Paz</span>
            </div>
            <h1 class="text-2xl sm:text-3xl font-display font-extrabold text-[#171717] tracking-tight leading-tight">
              Bienvenido a <span class="text-[#C76A32]">KAIRO</span>.
            </h1>
            <p class="text-sm sm:text-base text-[#626262] max-w-2xl font-normal leading-relaxed">
              Tu producción, tus registros y tus oportunidades en un solo lugar. Conectando la Central de Cooperativas El Ceibo, Palos Blancos y Sapecho con acopio transparente, trazabilidad EUDR y liquidez agrícola en Stellar.
            </p>
            <div class="flex flex-wrap gap-2.5 pt-2">
              <button onclick="startAutoDemo()" class="px-4 py-2 rounded-xl bg-gradient-to-r from-[#C76A32] to-[#D5A332] hover:brightness-110 text-white text-xs font-extrabold shadow-md transition flex items-center space-x-2">
                <i class="fa-solid fa-play"></i>
                <span>▶ Iniciar Demo Guiada Automática (2m 30s)</span>
              </button>
              <button onclick="switchTab('deliveries')" class="px-4 py-2 rounded-xl bg-[#171717] hover:bg-black text-white text-xs font-bold shadow-sm transition flex items-center space-x-2">
                <i class="fa-solid fa-plus"></i>
                <span>Registrar Boleta</span>
              </button>
              <button onclick="switchTab('factoring')" class="px-4 py-2 rounded-xl bg-white hover:bg-[#F4F4F0] text-[#171717] border border-[#E5E5E0] text-xs font-bold transition flex items-center space-x-2">
                <i class="fa-solid fa-calculator text-[#C76A32]"></i>
                <span>Simular Factoring</span>
              </button>
              <button onclick="switchTab('producers')" class="px-4 py-2 rounded-xl bg-white hover:bg-[#F4F4F0] text-[#626262] hover:text-[#171717] border border-[#E5E5E0] text-xs font-semibold transition">
                <span>Ver Parcelas EUDR</span>
              </button>
            </div>
          </div>

          <!-- Kairo Mascot Hero Representation (Section 7.3) -->
          <div class="md:col-span-4 flex justify-center md:justify-end relative">
            <div class="relative w-44 sm:w-52 h-48 sm:h-56 flex items-center justify-center">
              <div class="absolute inset-0 bg-[#C76A32]/10 rounded-full blur-2xl transform scale-90"></div>
              <img src="/static/kairo-mascot-transparent.png" 
                   alt="Kairo la mascota oficial de cacao" 
                   class="relative w-full h-full object-contain mascot-shadow transform hover:scale-105 transition-transform duration-300"
                   onerror="this.src='/kairo-mascot-transparent.png'">
            </div>
          </div>

        </div>
      </section>

      <!-- Financial Metrics & Operation Cards (80% neutral, 15% brand, 5% accent) -->
      <section class="space-y-3">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-base font-bold text-[#171717]">Métricas Financieras & Operativas</h2>
            <p class="text-xs text-[#626262]">Estado en vivo de liquidez, factoring desembolsado y contratos notarizados.</p>
          </div>
          <button onclick="loadDashboardData()" id="btn-refresh-dash" class="px-3 py-1.5 rounded-lg bg-white border border-[#E5E5E0] text-xs font-semibold text-[#171717] hover:bg-[#F4F4F0] transition flex items-center space-x-1.5 shadow-subtle">
            <i class="fa-solid fa-arrows-rotate text-[#C76A32]" id="icon-refresh"></i>
            <span>Actualizar</span>
          </button>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          
          <!-- Pool Vaquita Card -->
          <div class="bg-white rounded-xl border border-[#E5E5E0] p-5 shadow-subtle hover:border-[#C76A32]/40 transition">
            <div class="flex items-center justify-between text-[#626262] text-xs font-semibold uppercase tracking-wider">
              <span>Liquidez Pool Vaquita</span>
              <span class="w-7 h-7 rounded-lg bg-[#3F7D44]/10 text-[#3F7D44] flex items-center justify-center">
                <i class="fa-solid fa-vault text-xs"></i>
              </span>
            </div>
            <div class="mt-3 flex items-baseline">
              <span id="stat-pool-avail" class="text-2xl font-extrabold text-[#171717]">$25,000.00</span>
              <span class="ml-1 text-xs font-semibold text-[#626262]">USDC</span>
            </div>
            <div class="mt-2 text-xs text-[#626262] flex justify-between border-t border-[#EFEFEA] pt-2">
              <span>Total Pool: <strong id="stat-pool-total" class="text-[#171717]">$25,000.00</strong></span>
              <span>Reservado: <strong id="stat-pool-res" class="text-[#C76A32]">$0.00</strong></span>
            </div>
          </div>

          <!-- Factoring Advanced Card -->
          <div class="bg-white rounded-xl border border-[#E5E5E0] p-5 shadow-subtle hover:border-[#C76A32]/40 transition">
            <div class="flex items-center justify-between text-[#626262] text-xs font-semibold uppercase tracking-wider">
              <span>Total Anticipado Factoring</span>
              <span class="w-7 h-7 rounded-lg bg-[#C76A32]/10 text-[#C76A32] flex items-center justify-center">
                <i class="fa-solid fa-hand-holding-dollar text-xs"></i>
              </span>
            </div>
            <div class="mt-3 flex items-baseline">
              <span id="stat-total-usdc" class="text-2xl font-extrabold text-[#171717]">$0.00</span>
              <span class="ml-1 text-xs font-semibold text-[#626262]">USDC</span>
            </div>
            <div class="mt-2 text-xs text-[#626262] border-t border-[#EFEFEA] pt-2 flex items-center justify-between">
              <span>En Bolivianos (6.96):</span>
              <strong id="stat-total-bob" class="text-[#171717]">Bs. 0.00</strong>
            </div>
          </div>

          <!-- Notarized Deliveries Card -->
          <div class="bg-white rounded-xl border border-[#E5E5E0] p-5 shadow-subtle hover:border-[#C76A32]/40 transition">
            <div class="flex items-center justify-between text-[#626262] text-xs font-semibold uppercase tracking-wider">
              <span>Boletas Notarizadas</span>
              <span class="w-7 h-7 rounded-lg bg-[#D5A332]/10 text-[#D5A332] flex items-center justify-center">
                <i class="fa-solid fa-receipt text-xs"></i>
              </span>
            </div>
            <div class="mt-3 flex items-baseline">
              <span id="stat-deliveries-count" class="text-2xl font-extrabold text-[#171717]">0</span>
              <span class="ml-1 text-xs font-semibold text-[#626262]">tickets</span>
            </div>
            <div class="mt-2 text-xs text-[#626262] border-t border-[#EFEFEA] pt-2 flex items-center space-x-1.5">
              <i class="fa-solid fa-link text-[#3F7D44] text-[10px]"></i>
              <span class="truncate">Hashes SHA-256 en Stellar</span>
            </div>
          </div>

          <!-- Active Escrow Loans Card -->
          <div class="bg-white rounded-xl border border-[#E5E5E0] p-5 shadow-subtle hover:border-[#C76A32]/40 transition">
            <div class="flex items-center justify-between text-[#626262] text-xs font-semibold uppercase tracking-wider">
              <span>Préstamos en Garantía</span>
              <span class="w-7 h-7 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center">
                <i class="fa-solid fa-lock text-xs"></i>
              </span>
            </div>
            <div class="mt-3 flex items-baseline">
              <span id="stat-active-loans" class="text-2xl font-extrabold text-[#171717]">0</span>
              <span class="ml-1 text-xs font-semibold text-[#626262]">activos</span>
            </div>
            <div class="mt-2 text-xs text-[#626262] border-t border-[#EFEFEA] pt-2 flex items-center space-x-1.5">
              <i class="fa-solid fa-file-contract text-indigo-600 text-[10px]"></i>
              <span class="truncate">Trustless Work Escrow</span>
            </div>
          </div>

        </div>
      </section>

      <!-- Recent Notarized Deliveries Table (Section 8 Bug Fix: loads perfectly) -->
      <section class="bg-white rounded-xl border border-[#E5E5E0] shadow-subtle overflow-hidden">
        <div class="p-5 border-b border-[#E5E5E0] flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <h3 class="text-base font-bold text-[#171717] flex items-center space-x-2">
              <i class="fa-solid fa-clipboard-check text-[#C76A32]"></i>
              <span>Últimas Boletas de Acopio Notarizadas</span>
            </h3>
            <p class="text-xs text-[#626262]">Registro inmutable de peso neto seco equivalente, coordenadas EUDR y liquidación.</p>
          </div>
          <button onclick="switchTab('deliveries')" class="text-xs font-semibold text-[#C76A32] hover:text-[#B25A25] self-start sm:self-auto flex items-center space-x-1">
            <span>Nueva Boleta</span>
            <i class="fa-solid fa-arrow-right text-[10px]"></i>
          </button>
        </div>

        <!-- Table View -->
        <div class="overflow-x-auto custom-scrollbar">
          <table class="w-full text-left text-xs text-[#171717]" aria-label="Boletas de Acopio Recientes">
            <thead class="bg-[#F4F4F0] text-[#626262] font-semibold uppercase tracking-wider text-[11px] border-b border-[#E5E5E0]">
              <tr>
                <th class="px-4 py-3">Código</th>
                <th class="px-4 py-3">Socio Productor</th>
                <th class="px-4 py-3">Tipo / Grado</th>
                <th class="px-4 py-3">Peso Bruto &rarr; Neto</th>
                <th class="px-4 py-3">Liquidación Total</th>
                <th class="px-4 py-3">Hash Stellar Testnet</th>
                <th class="px-4 py-3 text-right">Estado</th>
              </tr>
            </thead>
            <tbody id="recent-deliveries-body" class="divide-y divide-[#EFEFEA]">
              <tr>
                <td colspan="7" class="text-center py-8 text-[#626262]">
                  <i class="fa-solid fa-spinner fa-spin mr-2 text-[#C76A32]"></i>Cargando boletas de acopio en tiempo real...
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Active Escrow Loans Table -->
      <section class="bg-white rounded-xl border border-[#E5E5E0] shadow-subtle overflow-hidden">
        <div class="p-5 border-b border-[#E5E5E0] flex items-center justify-between">
          <div>
            <h3 class="text-base font-bold text-[#171717] flex items-center space-x-2">
              <i class="fa-solid fa-file-invoice-dollar text-[#3F7D44]"></i>
              <span>Operaciones de Factoring Activas en Escrow</span>
            </h3>
            <p class="text-xs text-[#626262]">Préstamos condicionados a cosecha con fondos reservados en Vaquita Pool.</p>
          </div>
        </div>
        <div class="overflow-x-auto custom-scrollbar">
          <table class="w-full text-left text-xs text-[#171717]" aria-label="Préstamos de Factoring Activos">
            <thead class="bg-[#F4F4F0] text-[#626262] font-semibold uppercase tracking-wider text-[11px] border-b border-[#E5E5E0]">
              <tr>
                <th class="px-4 py-3">Código Préstamo</th>
                <th class="px-4 py-3">Productor</th>
                <th class="px-4 py-3">Monto Aprobado</th>
                <th class="px-4 py-3">Equivalente BOB</th>
                <th class="px-4 py-3">Contrato Trustless Work</th>
                <th class="px-4 py-3 text-right">Acción</th>
              </tr>
            </thead>
            <tbody id="active-loans-body" class="divide-y divide-[#EFEFEA]">
              <tr>
                <td colspan="6" class="text-center py-6 text-[#626262]">No hay préstamos activos en este momento.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

    </div>

    <!-- ==================================================================== -->
    <!-- TAB 2: EUDR & PARCELAS (Trazabilidad y Cero Deforestación)             -->
    <!-- ==================================================================== -->
    <div id="tab-producers" class="tab-content hidden space-y-6">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-2 border-b border-[#E5E5E0]">
        <div>
          <h1 class="text-2xl font-display font-bold text-[#171717]">Socios Cacaoteros & Trazabilidad EUDR</h1>
          <p class="text-xs sm:text-sm text-[#626262]">
            Georreferenciación de parcelas, coordenadas GPS y validación documental contra la deforestación para exportación a la Unión Europea.
          </p>
        </div>
        <span class="self-start sm:self-auto px-3 py-1 rounded-full text-xs font-semibold bg-[#3F7D44]/10 text-[#3F7D44] border border-[#3F7D44]/20 flex items-center space-x-1.5">
          <i class="fa-solid fa-tree"></i>
          <span>Reglamento EUDR 2023/1115</span>
        </span>
      </div>

      <!-- Producers Grid -->
      <div id="producers-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        <div class="col-span-full py-12 text-center text-[#626262]">
          <i class="fa-solid fa-spinner fa-spin mr-2 text-[#C76A32]"></i>Cargando socios cacaoteros...
        </div>
      </div>
    </div>

    <!-- ==================================================================== -->
    <!-- TAB 3: REGISTRO DE ACOPIO (3 Etapas Claras, Section 10)               -->
    <!-- ==================================================================== -->
    <div id="tab-deliveries" class="tab-content hidden space-y-6">
      
      <div class="max-w-3xl mx-auto space-y-6">
        
        <div class="text-center space-y-1">
          <h1 class="text-2xl font-display font-bold text-[#171717]">Módulo de Acopio & Boleta Transparente</h1>
          <p class="text-xs text-[#626262]">
            Digitalización de pesaje en balanza, cálculo agronómico riguroso y notarización criptográfica en Stellar.
          </p>
        </div>

        <!-- 3-Stage Progress Indicator -->
        <div class="grid grid-cols-3 gap-2 p-1.5 bg-[#F4F4F0] rounded-xl border border-[#E5E5E0] text-center text-xs font-semibold text-[#626262]">
          <div id="step-pill-1" class="py-2 rounded-lg bg-white text-[#171717] shadow-subtle border border-[#E5E5E0]">
            <span class="w-5 h-5 rounded-full bg-[#171717] text-white inline-flex items-center justify-center text-[10px] mr-1.5">1</span>
            <span>Datos Entrega</span>
          </div>
          <div id="step-pill-2" class="py-2 rounded-lg text-[#626262]">
            <span class="w-5 h-5 rounded-full bg-[#E5E5E0] text-[#171717] inline-flex items-center justify-center text-[10px] mr-1.5">2</span>
            <span>Vista Previa</span>
          </div>
          <div id="step-pill-3" class="py-2 rounded-lg text-[#626262]">
            <span class="w-5 h-5 rounded-full bg-[#E5E5E0] text-[#171717] inline-flex items-center justify-center text-[10px] mr-1.5">3</span>
            <span>Comprobante</span>
          </div>
        </div>

        <!-- Form Card -->
        <div class="bg-white rounded-2xl border border-[#E5E5E0] p-6 sm:p-8 shadow-card space-y-6">
          
          <form id="delivery-form" onsubmit="submitDelivery(event)" class="space-y-5">
            
            <!-- Etapa 1: Datos de la Entrega -->
            <div class="space-y-4">
              <h2 class="text-sm font-bold text-[#171717] uppercase tracking-wider flex items-center space-x-2 border-b border-[#EFEFEA] pb-2">
                <i class="fa-solid fa-scale-balanced text-[#C76A32]"></i>
                <span>Etapa 1 · Parámetros de Acopio</span>
              </h2>

              <div>
                <label for="del-producer-id" class="block text-xs font-semibold text-[#171717] mb-1.5">Socio Productor Autorizado</label>
                <select id="del-producer-id" class="w-full bg-[#FAFAF8] border border-[#E5E5E0] rounded-xl px-3.5 py-2.5 text-xs text-[#171717] focus:outline-none focus:ring-2 focus:ring-[#C76A32] focus:border-transparent font-medium" required>
                  <option value="1">Mateo Mamani Ticona — Central El Ceibo (Sapecho) · Parcela BO-LPZ-AB-ELCEIBO-001</option>
                  <option value="2">Elena Quispe Condori — Coop. Agroecológica Palos Blancos · Parcela BO-LPZ-PB-AGROECO-002</option>
                  <option value="3">Carlos Condori Mamani — Asoc. Productores Bella Vista · Parcela BO-LPZ-BV-ASOPROC-003</option>
                </select>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label for="del-cacao-type" class="block text-xs font-semibold text-[#171717] mb-1.5">Estado del Cacao</label>
                  <select id="del-cacao-type" onchange="calculatePreview()" class="w-full bg-[#FAFAF8] border border-[#E5E5E0] rounded-xl px-3.5 py-2.5 text-xs text-[#171717] focus:outline-none focus:ring-2 focus:ring-[#C76A32] font-medium">
                    <option value="BABA">Cacao en Baba (Conversión 0.33)</option>
                    <option value="SECO">Cacao Seco (Penalidad si &gt; 7.5% humedad)</option>
                  </select>
                </div>
                <div>
                  <label for="del-quality" class="block text-xs font-semibold text-[#171717] mb-1.5">Grado de Calidad Evaluado</label>
                  <select id="del-quality" onchange="calculatePreview()" class="w-full bg-[#FAFAF8] border border-[#E5E5E0] rounded-xl px-3.5 py-2.5 text-xs text-[#171717] focus:outline-none focus:ring-2 focus:ring-[#C76A32] font-medium">
                    <option value="A">Grado A (1.00x — Cacao de Exportación)</option>
                    <option value="B">Grado B (0.90x — Cacao Convencional)</option>
                    <option value="C">Grado C (0.75x — Cacao con Defectos)</option>
                  </select>
                </div>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label for="del-gross-weight" class="block text-xs font-semibold text-[#171717] mb-1.5">Peso Bruto Balanza (kg)</label>
                  <div class="relative">
                    <input type="number" id="del-gross-weight" step="0.1" min="1" value="1000" oninput="calculatePreview()" class="w-full bg-[#FAFAF8] border border-[#E5E5E0] rounded-xl px-3.5 py-2.5 text-xs text-[#171717] font-bold focus:outline-none focus:ring-2 focus:ring-[#C76A32]" required>
                    <span class="absolute right-3.5 top-2.5 text-xs text-[#626262]">kg</span>
                  </div>
                </div>
                <div>
                  <label for="del-moisture" class="block text-xs font-semibold text-[#171717] mb-1.5">Humedad Medida (%)</label>
                  <div class="relative">
                    <input type="number" id="del-moisture" step="0.1" min="0" max="100" value="55.0" oninput="calculatePreview()" class="w-full bg-[#FAFAF8] border border-[#E5E5E0] rounded-xl px-3.5 py-2.5 text-xs text-[#171717] font-bold focus:outline-none focus:ring-2 focus:ring-[#C76A32]" required>
                    <span class="absolute right-3.5 top-2.5 text-xs text-[#626262]">%</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Etapa 2: Vista Previa de la Liquidación -->
            <div class="space-y-3 bg-[#F4F4F0] rounded-xl p-5 border border-[#E5E5E0]">
              <h2 class="text-xs font-bold text-[#171717] uppercase tracking-wider flex items-center space-x-1.5">
                <i class="fa-solid fa-calculator text-[#C76A32]"></i>
                <span>Etapa 2 · Cálculo Agronómico & Financiero en Vivo</span>
              </h2>

              <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs pt-1">
                <div class="bg-white p-3 rounded-lg border border-[#E5E5E0]">
                  <span class="text-[#626262] block text-[11px]">Peso Neto Seco Eq.:</span>
                  <span id="preview-net-weight" class="text-base font-extrabold text-[#3F7D44]">330.00 kg</span>
                  <span id="preview-penalty" class="text-[10px] text-[#A74445] block">Factor baba 0.33x</span>
                </div>
                <div class="bg-white p-3 rounded-lg border border-[#E5E5E0]">
                  <span class="text-[#626262] block text-[11px]">Precio Final / kg:</span>
                  <span id="preview-price-kg" class="text-base font-extrabold text-[#171717]">$4.80 USDC</span>
                  <span class="text-[10px] text-[#626262] block">Base $4.80 × Calidad</span>
                </div>
                <div class="bg-white p-3 rounded-lg border border-[#E5E5E0]">
                  <span class="text-[#626262] block text-[11px]">Importe en Bolivianos:</span>
                  <span id="preview-total-bob" class="text-base font-extrabold text-[#C76A32]">Bs. 11,024.64</span>
                  <span class="text-[10px] text-[#626262] block">T/C Oficial 6.96</span>
                </div>
              </div>

              <div class="flex items-center justify-between pt-2 border-t border-[#E5E5E0] text-xs font-bold text-[#171717]">
                <span>Total a Liquidar al Productor:</span>
                <span id="preview-total" class="text-sm font-extrabold text-[#C76A32]">$1,584.00 USDC</span>
              </div>
            </div>

            <!-- Submit Action -->
            <button type="submit" id="btn-submit-delivery" class="w-full py-3.5 rounded-xl bg-[#171717] hover:bg-black text-white text-xs font-extrabold tracking-wide uppercase transition shadow-md flex items-center justify-center space-x-2">
              <i class="fa-solid fa-stamp text-[#D5A332]"></i>
              <span id="btn-submit-delivery-text">Etapa 3 · Emitir Boleta & Notarizar en Stellar</span>
            </button>
          </form>

          <!-- Etapa 3: Success Confirmation with Kairo Mascot (Section 7.3) -->
          <div id="delivery-result-box" class="hidden bg-[#EBF4EC] border border-[#3F7D44]/30 rounded-2xl p-6 space-y-4">
            <div class="flex flex-col sm:flex-row items-center gap-4">
              <div class="w-20 h-20 flex-shrink-0">
                <img src="/static/kairo-mascot-transparent.png" alt="Kairo celebra" class="w-full h-full object-contain mascot-shadow" onerror="this.src='/kairo-mascot-transparent.png'">
              </div>
              <div class="space-y-1 text-center sm:text-left">
                <div class="inline-flex items-center space-x-1 px-2.5 py-0.5 rounded-full bg-[#3F7D44] text-white text-[11px] font-bold">
                  <i class="fa-solid fa-circle-check"></i>
                  <span>¡Boleta Notarizada en Stellar Testnet!</span>
                </div>
                <h3 class="text-base font-bold text-[#171717]">KAIRO ha registrado tu acopio exitosamente</h3>
                <p class="text-xs text-[#626262]">El ticket ha quedado blindado criptográficamente contra alteraciones.</p>
              </div>
            </div>

            <div id="delivery-result-content" class="bg-white rounded-xl p-4 border border-[#3F7D44]/20 font-mono text-xs text-[#171717] space-y-1.5 overflow-x-auto">
              <!-- Filled via JS -->
            </div>

            <div class="flex justify-end pt-2">
              <button onclick="dismissDeliveryResult()" class="px-3.5 py-1.5 rounded-lg bg-white border border-[#E5E5E0] text-xs font-semibold text-[#171717] hover:bg-[#F4F4F0] transition">
                Cerrar Comprobante
              </button>
            </div>
          </div>

        </div>
      </div>
    </div>

    <!-- ==================================================================== -->
    <!-- TAB 4: FACTORING ML & ORÁCULO DE RIESGO AGRONÓMICO                    -->
    <!-- ==================================================================== -->
    <div id="tab-factoring" class="tab-content hidden space-y-6">
      
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-2 border-b border-[#E5E5E0]">
        <div>
          <h1 class="text-2xl font-display font-bold text-[#171717]">Factoring Agrícola Predictivo & Oráculo ML</h1>
          <p class="text-xs sm:text-sm text-[#626262]">
            Evaluación de riesgo crediticio con variables microclimáticas de Alto Beni y desembolso vía Simple QR en Bolivianos.
          </p>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        <!-- Left: Simulator Controls -->
        <div class="lg:col-span-6 bg-white rounded-2xl border border-[#E5E5E0] p-6 shadow-card space-y-5">
          <div class="border-b border-[#EFEFEA] pb-3">
            <h2 class="text-sm font-bold text-[#171717] uppercase tracking-wider flex items-center space-x-2">
              <i class="fa-solid fa-sliders text-[#C76A32]"></i>
              <span>Parámetros del Oráculo Climático</span>
            </h2>
            <p class="text-xs text-[#626262] mt-0.5">Modelo RandomForest evaluando historial de socio y estrés hídrico.</p>
          </div>

          <div class="space-y-4 text-xs">
            <div>
              <label for="fac-producer-id" class="block font-semibold text-[#171717] mb-1">Socio Solicitante</label>
              <select id="fac-producer-id" class="w-full bg-[#FAFAF8] border border-[#E5E5E0] rounded-xl px-3 py-2 text-[#171717] font-medium">
                <option value="1">Mateo Mamani (El Ceibo · Sapecho — 96% Cumplimiento)</option>
                <option value="2">Elena Quispe (Palos Blancos — 78% Cumplimiento)</option>
                <option value="3">Carlos Condori (Bella Vista — 55% Nuevo Productor)</option>
              </select>
            </div>

            <div>
              <label for="fac-expected-kg" class="block font-semibold text-[#171717] mb-1">Cosecha Proyectada Comprometida (kg secos)</label>
              <input type="number" id="fac-expected-kg" value="1500" min="100" class="w-full bg-[#FAFAF8] border border-[#E5E5E0] rounded-xl px-3 py-2 text-[#171717] font-bold">
            </div>

            <!-- Rainfall Slider with microclimate guidelines -->
            <div class="p-3.5 bg-[#F4F4F0] rounded-xl border border-[#E5E5E0] space-y-2">
              <div class="flex justify-between items-center">
                <label for="fac-rainfall" class="font-semibold text-[#171717]">Precipitación Mensual Alto Beni</label>
                <span id="label-rainfall" class="text-xs font-bold text-[#3F7D44]">160 mm (Óptimo)</span>
              </div>
              <input type="range" id="fac-rainfall" min="40" max="320" value="160" step="5" oninput="updateWeatherLabels()" class="w-full accent-[#C76A32]">
              <div class="flex justify-between text-[10px] text-[#626262]">
                <span>&lt;80mm (Sequía)</span>
                <span>140-180mm (Óptimo)</span>
                <span>&gt;240mm (Riesgo Moniliasis)</span>
              </div>
            </div>

            <!-- Humidity Slider -->
            <div class="p-3.5 bg-[#F4F4F0] rounded-xl border border-[#E5E5E0] space-y-2">
              <div class="flex justify-between items-center">
                <label for="fac-humidity" class="font-semibold text-[#171717]">Humedad Relativa del Bosque</label>
                <span id="label-humidity" class="text-xs font-bold text-[#3F7D44]">75% (Seguro)</span>
              </div>
              <input type="range" id="fac-humidity" min="50" max="98" value="75" step="1" oninput="updateWeatherLabels()" class="w-full accent-[#C76A32]">
              <div class="flex justify-between text-[10px] text-[#626262]">
                <span>50%</span>
                <span>&gt;85% (Alerta Mazorca Negra)</span>
                <span>98%</span>
              </div>
            </div>

            <button onclick="runSimulation()" id="btn-simulate" class="w-full py-3 rounded-xl bg-[#C76A32] hover:bg-[#B25A25] text-white text-xs font-bold shadow-sm transition flex items-center justify-center space-x-2">
              <i class="fa-solid fa-microchip"></i>
              <span>Calcular Capacidad de Factoring con Oráculo</span>
            </button>
          </div>
        </div>

        <!-- Right: Results & Payout Execution -->
        <div class="lg:col-span-6 bg-white rounded-2xl border border-[#E5E5E0] p-6 shadow-card space-y-5">
          <div class="border-b border-[#EFEFEA] pb-3">
            <h2 class="text-sm font-bold text-[#171717] uppercase tracking-wider flex items-center space-x-2">
              <i class="fa-solid fa-qrcode text-[#3F7D44]"></i>
              <span>Resultado de Evaluación & Desembolso</span>
            </h2>
            <p class="text-xs text-[#626262] mt-0.5">Propuesta crediticia, cupo pre-aprobado y generación de QR.</p>
          </div>

          <div id="sim-empty-state" class="py-12 text-center text-[#626262] space-y-2">
            <i class="fa-solid fa-cloud-sun-rain text-4xl text-[#E5E5E0]"></i>
            <p class="text-xs">Presiona "Calcular Capacidad" para que el modelo estime el anticipo seguro.</p>
          </div>

          <!-- Simulation Details Box -->
          <div id="sim-result-box" class="hidden space-y-4">
            
            <div class="grid grid-cols-2 gap-3">
              <div class="p-3 bg-[#FAFAF8] rounded-xl border border-[#E5E5E0]">
                <span class="text-[10px] text-[#626262] uppercase font-bold block">Nivel de Riesgo</span>
                <span id="res-risk-tier" class="text-base font-extrabold text-[#3F7D44]">RIESGO BAJO</span>
                <span id="res-risk-score" class="text-[10px] text-[#626262] block">Score: 24.5 / 100</span>
              </div>
              <div class="p-3 bg-[#FAFAF8] rounded-xl border border-[#E5E5E0]">
                <span class="text-[10px] text-[#626262] uppercase font-bold block">Anticipo Pre-aprobado</span>
                <span id="res-advance-pct" class="text-base font-extrabold text-[#C76A32]">53.0%</span>
                <span class="text-[10px] text-[#626262] block">Del valor de cosecha</span>
              </div>
            </div>

            <div class="p-3.5 bg-[#FAF7F3] rounded-xl border border-[#C76A32]/20">
              <span class="text-[11px] font-bold text-[#171717] block mb-1">Monto Máximo de Anticipo:</span>
              <div class="flex items-baseline space-x-2">
                <span id="res-advance-amount" class="text-xl font-extrabold text-[#C76A32]">$3,816.00 USDC</span>
                <span id="res-advance-bob" class="text-xs text-[#626262] font-semibold">(Bs. 26,559.36)</span>
              </div>
            </div>

            <!-- Risk factors list -->
            <div class="p-3 bg-[#FAFAF8] rounded-xl border border-[#E5E5E0] text-xs space-y-1.5">
              <span class="font-bold text-[#171717] block text-[11px] uppercase tracking-wider">Diagnóstico Explicativo:</span>
              <ul id="res-factors-list" class="space-y-1 text-[#626262] list-disc list-inside"></ul>
            </div>

            <!-- Request Execution -->
            <div class="pt-2 border-t border-[#EFEFEA] space-y-3">
              <div class="flex items-center justify-between text-xs">
                <span class="font-semibold text-[#171717]">Monto Solicitado a Desembolsar (USDC):</span>
                <input type="number" id="exec-requested-amount" value="800" class="w-32 bg-[#FAFAF8] border border-[#E5E5E0] rounded-lg px-2.5 py-1 text-right font-bold text-[#171717]">
              </div>
              <button onclick="executeLoan()" id="btn-exec-loan" class="w-full py-3 rounded-xl bg-[#171717] hover:bg-black text-white text-xs font-bold transition flex items-center justify-center space-x-2">
                <i class="fa-solid fa-bolt text-[#D5A332]"></i>
                <span>Desembolsar Inmediato (Pollar Simple QR en Bs.)</span>
              </button>
            </div>

          </div>

          <!-- Pollar QR Voucher -->
          <div id="qr-modal-view" class="hidden bg-[#FEF9EC] border border-[#D5A332]/40 rounded-xl p-5 space-y-3 text-xs">
            <div class="flex items-center justify-between">
              <span class="font-bold text-[#75452D] flex items-center space-x-1.5">
                <i class="fa-solid fa-qrcode text-[#C76A32]"></i>
                <span>Orden de Pago Simple QR (Bolivia)</span>
              </span>
              <span class="px-2 py-0.5 rounded-full bg-[#3F7D44]/15 text-[#3F7D44] font-bold text-[10px]">ACTIVE_ESCROW</span>
            </div>
            
            <div class="bg-white p-4 rounded-xl border border-[#E5E5E0] flex flex-col items-center justify-center space-y-2">
              <div class="w-36 h-36 bg-[#FAFAF8] border-2 border-dashed border-[#E5E5E0] rounded-xl flex items-center justify-center">
                <i class="fa-solid fa-qrcode text-6xl text-[#171717]"></i>
              </div>
              <div class="text-center">
                <div class="text-base font-black text-[#171717]" id="qr-amount-bob">Bs. 5,568.00</div>
                <div class="text-[10px] text-[#626262] font-mono" id="qr-payout-id">pol_out_...</div>
              </div>
            </div>

            <div class="space-y-1 text-[11px] text-[#626262]">
              <div>• <strong>Vaquita Pool Reserva:</strong> <span id="qr-vaquita-res" class="font-mono text-[#171717]">vaq_res_...</span></div>
              <div>• <strong>Trustless Work Escrow:</strong> <span id="qr-escrow-id" class="font-mono text-[#171717]">escrow_tw_...</span></div>
            </div>

            <a id="qr-deep-link" href="#" target="_blank" rel="noopener" class="block text-center py-2 rounded-lg bg-[#C76A32] hover:bg-[#B25A25] text-white font-bold text-xs transition">
              Abrir en Pollar App
            </a>
          </div>

        </div>

      </div>
    </div>

    <!-- ==================================================================== -->
    <!-- TAB 5: TWO-STAGE ML (Rendimiento por Biometría & Pronóstico Precios)  -->
    <!-- ==================================================================== -->
    <div id="tab-ml-forecast" class="tab-content hidden space-y-6">
      
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-2 border-b border-[#E5E5E0]">
        <div>
          <h1 class="text-2xl font-display font-bold text-[#171717]">Modelo Two-Stage (LightGBM) & Pronóstico de Precios</h1>
          <p class="text-xs sm:text-sm text-[#626262]">
            Etapa 1: Probabilidad de fructificación P(y &gt; 0) + Etapa 2: Regresión logarítmica de gramos por árbol + Proyección estocástica ICCO.
          </p>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        <!-- Biometric Yield Estimator -->
        <div class="bg-white rounded-2xl border border-[#E5E5E0] p-6 shadow-card space-y-4">
          <div class="border-b border-[#EFEFEA] pb-3">
            <h2 class="text-sm font-bold text-[#171717] uppercase tracking-wider flex items-center space-x-2">
              <i class="fa-solid fa-tree text-[#3F7D44]"></i>
              <span>Estimación de Rendimiento por Biometría</span>
            </h2>
            <p class="text-xs text-[#626262] mt-0.5">Parámetros morfológicos de plantas para predecir cosecha real.</p>
          </div>

          <div class="grid grid-cols-2 gap-3 text-xs">
            <div>
              <label for="ml-height" class="block font-semibold text-[#171717] mb-1">Altura Árbol (cm)</label>
              <input type="number" id="ml-height" value="170" class="w-full bg-[#FAFAF8] border border-[#E5E5E0] rounded-lg px-2.5 py-1.5 font-medium">
            </div>
            <div>
              <label for="ml-diam" class="block font-semibold text-[#171717] mb-1">Diámetro Tronco (cm)</label>
              <input type="number" id="ml-diam" value="8.0" step="0.1" class="w-full bg-[#FAFAF8] border border-[#E5E5E0] rounded-lg px-2.5 py-1.5 font-medium">
            </div>
            <div>
              <label for="ml-leaves" class="block font-semibold text-[#171717] mb-1">Conteo de Hojas</label>
              <input type="number" id="ml-leaves" value="260" class="w-full bg-[#FAFAF8] border border-[#E5E5E0] rounded-lg px-2.5 py-1.5 font-medium">
            </div>
            <div>
              <label for="ml-cherelle" class="block font-semibold text-[#171717] mb-1">Cherelles por Árbol</label>
              <input type="number" id="ml-cherelle" value="0.3" step="0.1" class="w-full bg-[#FAFAF8] border border-[#E5E5E0] rounded-lg px-2.5 py-1.5 font-medium">
            </div>
            <div>
              <label for="ml-density" class="block font-semibold text-[#171717] mb-1">Densidad (Árboles/ha)</label>
              <input type="number" id="ml-density" value="1111" class="w-full bg-[#FAFAF8] border border-[#E5E5E0] rounded-lg px-2.5 py-1.5 font-medium">
            </div>
            <div>
              <label for="ml-variety" class="block font-semibold text-[#171717] mb-1">Variedad Cacao</label>
              <select id="ml-variety" class="w-full bg-[#FAFAF8] border border-[#E5E5E0] rounded-lg px-2.5 py-1.5 font-medium">
                <option value="Nacional">Nacional (Alto Beni)</option>
                <option value="Criollo">Criollo Amazónico</option>
                <option value="CCN-51">CCN-51</option>
              </select>
            </div>
          </div>

          <button onclick="estimateYield()" id="btn-ml-yield" class="w-full py-2.5 rounded-xl bg-[#3F7D44] hover:bg-[#346838] text-white text-xs font-bold transition flex items-center justify-center space-x-2 shadow-sm">
            <i class="fa-solid fa-microchip"></i>
            <span>Inferir Rendimiento con LightGBM</span>
          </button>

          <!-- Yield Result Box -->
          <div id="ml-yield-result" class="hidden p-4 bg-[#EBF4EC] rounded-xl border border-[#3F7D44]/30 space-y-2 text-xs">
            <div class="text-[10px] uppercase text-[#3F7D44] font-bold tracking-wider">Inferencia Two-Stage Completada</div>
            <div class="flex justify-between items-baseline">
              <span class="text-[#626262]">Rendimiento por Árbol:</span>
              <span id="res-yield-g" class="text-base font-extrabold text-[#3F7D44]">48.47 g/árbol</span>
            </div>
            <div class="flex justify-between items-baseline">
              <span class="text-[#626262]">Rendimiento por Hectárea:</span>
              <span id="res-yield-ha" class="text-base font-extrabold text-[#171717]">53.85 kg/ha</span>
            </div>
            <div class="flex justify-between text-[11px] text-[#626262] pt-1.5 border-t border-[#3F7D44]/20">
              <span>Probabilidad Fructificación P(y&gt;0):</span>
              <span id="res-yield-prob" class="font-bold text-[#171717]">95.1%</span>
            </div>
          </div>
        </div>

        <!-- Cacao Price Forecast -->
        <div class="bg-white rounded-2xl border border-[#E5E5E0] p-6 shadow-card space-y-4">
          <div class="border-b border-[#EFEFEA] pb-3">
            <h2 class="text-sm font-bold text-[#171717] uppercase tracking-wider flex items-center space-x-2">
              <i class="fa-solid fa-arrow-trend-up text-[#D5A332]"></i>
              <span>Pronóstico de Precios Internacionales (ICCO)</span>
            </h2>
            <p class="text-xs text-[#626262] mt-0.5">Modelo estocástico de reversión a la media y bandas de confianza al 95%.</p>
          </div>

          <div class="grid grid-cols-2 gap-3 text-xs">
            <div>
              <label for="ml-horizon" class="block font-semibold text-[#171717] mb-1">Horizonte de Tiempo</label>
              <select id="ml-horizon" class="w-full bg-[#FAFAF8] border border-[#E5E5E0] rounded-lg px-2.5 py-1.5 font-medium">
                <option value="15">15 Días</option>
                <option value="30" selected>30 Días (1 Mes)</option>
                <option value="60">60 Días (2 Meses)</option>
                <option value="90">90 Días (Cosecha)</option>
              </select>
            </div>
            <div>
              <label for="ml-current-price" class="block font-semibold text-[#171717] mb-1">Precio Referencial ($/kg)</label>
              <input type="number" id="ml-current-price" value="4.80" step="0.05" class="w-full bg-[#FAFAF8] border border-[#E5E5E0] rounded-lg px-2.5 py-1.5 font-bold">
            </div>
          </div>

          <button onclick="forecastPrice()" id="btn-ml-price" class="w-full py-2.5 rounded-xl bg-[#171717] hover:bg-black text-white text-xs font-bold transition flex items-center justify-center space-x-2 shadow-sm">
            <i class="fa-solid fa-chart-line text-[#D5A332]"></i>
            <span>Simular Trayectoria de Precios</span>
          </button>

          <!-- Price Result Box -->
          <div id="ml-price-result" class="hidden p-4 bg-[#FEF9EC] rounded-xl border border-[#D5A332]/30 space-y-2 text-xs">
            <div class="flex items-center justify-between">
              <span class="text-[10px] uppercase text-[#75452D] font-bold">Proyección a <span id="res-price-days">30</span> días</span>
              <span id="res-price-trend" class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-[#D5A332]/20 text-[#75452D]">NEUTRAL</span>
            </div>
            <div class="flex justify-between items-baseline">
              <span class="text-[#626262]">Precio Proyectado:</span>
              <span id="res-price-val" class="text-lg font-extrabold text-[#171717]">$4.80 USDC/kg</span>
            </div>
            <div class="flex justify-between text-[11px] text-[#626262] pt-1.5 border-t border-[#D5A332]/20">
              <span>Banda de Confianza (95%):</span>
              <span id="res-price-ci" class="font-bold text-[#171717]">[$4.41 - $5.22]</span>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- ==================================================================== -->
    <!-- TAB 6: PROGRESO & GAMIFICACIÓN CON MASCOTA KAIRO (Section 13)         -->
    <!-- ==================================================================== -->
    <div id="tab-progress" class="tab-content hidden space-y-6">
      
      <!-- Gamification Hero Header -->
      <section class="bg-gradient-to-br from-white via-[#FAF7F3] to-[#FEF9EC] rounded-2xl border border-[#E5E5E0] p-6 sm:p-8 shadow-card overflow-hidden">
        <div class="grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
          
          <div class="md:col-span-8 space-y-3">
            <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-[#D5A332]/10 border border-[#D5A332]/20 text-[#75452D] text-xs font-semibold">
              <i class="fa-solid fa-award text-[#D5A332]"></i>
              <span>Programa de Lealtad & Mérito Agroforestal</span>
            </div>
            <h1 class="text-2xl sm:text-3xl font-display font-extrabold text-[#171717] tracking-tight">
              Avanza con <span class="text-[#C76A32]">KAIRO</span> en Cada Cosecha
            </h1>
            <p class="text-sm text-[#626262] leading-relaxed max-w-xl">
              Gana Puntos KAIRO y certificaciones verificables en Stellar por mantener tu parcela libre de deforestación (EUDR), entregar cacao fermentado Grado A y cumplir tus liquidaciones a tiempo.
            </p>
            <div class="flex items-center space-x-3 pt-1 text-xs text-[#626262]">
              <span class="flex items-center"><i class="fa-solid fa-circle-check text-[#3F7D44] mr-1"></i>Puntos Verificables</span>
              <span class="flex items-center"><i class="fa-solid fa-circle-check text-[#3F7D44] mr-1"></i>Respaldado en Stellar</span>
              <span class="flex items-center"><i class="fa-solid fa-circle-check text-[#3F7D44] mr-1"></i>Preferencia en Factoring</span>
            </div>
          </div>

          <!-- Kairo Mascot Protagonist -->
          <div class="md:col-span-4 flex justify-center md:justify-end">
            <div class="w-48 sm:w-56 h-48 sm:h-56 relative flex items-center justify-center">
              <div class="absolute inset-0 bg-[#D5A332]/10 rounded-full blur-2xl transform scale-90"></div>
              <img src="/static/kairo-mascot-transparent.png" 
                   alt="Kairo te acompaña en tu progreso" 
                   class="relative w-full h-full object-contain mascot-shadow transform hover:scale-105 transition-transform duration-300"
                   onerror="this.src='/kairo-mascot-transparent.png'">
            </div>
          </div>

        </div>
      </section>

      <!-- Producer Levels Progression Roadmap -->
      <section class="space-y-4">
        <div>
          <h2 class="text-base font-bold text-[#171717]">Niveles de Reconocimiento del Productor</h2>
          <p class="text-xs text-[#626262]">Tu trayectoria acumulada como socio cacaotero en Alto Beni.</p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          
          <!-- Level 1: Semilla -->
          <div class="bg-white rounded-xl border-2 border-[#3F7D44] p-5 shadow-subtle relative space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-[#3F7D44]/15 text-[#3F7D44]">ACTUAL</span>
              <i class="fa-solid fa-seedling text-lg text-[#3F7D44]"></i>
            </div>
            <div>
              <h3 class="font-bold text-sm text-[#171717]">Nivel 1 · Productor Semilla</h3>
              <p class="text-[11px] text-[#626262] mt-0.5">Registro oficial en cooperativa con parcela georreferenciada.</p>
            </div>
            <div class="space-y-1 text-xs">
              <div class="flex justify-between text-[11px]">
                <span class="text-[#626262]">Progreso:</span>
                <span class="font-bold text-[#3F7D44]">100% Completado</span>
              </div>
              <div class="w-full bg-[#E5E5E0] h-2 rounded-full overflow-hidden">
                <div class="bg-[#3F7D44] h-full w-full"></div>
              </div>
            </div>
          </div>

          <!-- Level 2: Guardián Agroforestal -->
          <div class="bg-white rounded-xl border border-[#E5E5E0] p-5 shadow-subtle space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-[#F4F4F0] text-[#626262]">SIGUIENTE</span>
              <i class="fa-solid fa-tree text-lg text-[#C76A32]"></i>
            </div>
            <div>
              <h3 class="font-bold text-sm text-[#171717]">Nivel 2 · Guardián Agroforestal</h3>
              <p class="text-[11px] text-[#626262] mt-0.5">Cumplimiento EUDR con cero deforestación verificado en satélite.</p>
            </div>
            <div class="space-y-1 text-xs">
              <div class="flex justify-between text-[11px]">
                <span class="text-[#626262]">Requisito:</span>
                <span class="font-semibold text-[#171717]">3 Entregas Grado A</span>
              </div>
              <div class="w-full bg-[#E5E5E0] h-2 rounded-full overflow-hidden">
                <div class="bg-[#C76A32] h-full w-2/3"></div>
              </div>
            </div>
          </div>

          <!-- Level 3: Mazorca de Oro -->
          <div class="bg-white rounded-xl border border-[#E5E5E0] p-5 shadow-subtle space-y-3 opacity-90">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-[#F4F4F0] text-[#626262]">NIVEL 3</span>
              <i class="fa-solid fa-medal text-lg text-[#D5A332]"></i>
            </div>
            <div>
              <h3 class="font-bold text-sm text-[#171717]">Nivel 3 · Mazorca de Oro</h3>
              <p class="text-[11px] text-[#626262] mt-0.5">Cumplimiento en microcrédito y más de 3,000 kg acopiados.</p>
            </div>
            <div class="space-y-1 text-xs">
              <div class="flex justify-between text-[11px]">
                <span class="text-[#626262]">Beneficio:</span>
                <span class="font-semibold text-[#D5A332]">60% Anticipo en Factoring</span>
              </div>
              <div class="w-full bg-[#E5E5E0] h-2 rounded-full overflow-hidden">
                <div class="bg-[#D5A332] h-full w-1/4"></div>
              </div>
            </div>
          </div>

          <!-- Level 4: Maestro del Cacao -->
          <div class="bg-white rounded-xl border border-[#E5E5E0] p-5 shadow-subtle space-y-3 opacity-75">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-[#F4F4F0] text-[#626262]">ELITE</span>
              <i class="fa-solid fa-crown text-lg text-[#75452D]"></i>
            </div>
            <div>
              <h3 class="font-bold text-sm text-[#171717]">Nivel 4 · Maestro El Ceibo</h3>
              <p class="text-[11px] text-[#626262] mt-0.5">Líder comunal con sello orgánico y cero penalidades.</p>
            </div>
            <div class="space-y-1 text-xs">
              <div class="flex justify-between text-[11px]">
                <span class="text-[#626262]">Beneficio:</span>
                <span class="font-semibold text-[#75452D]">Tasa Preferencial 1.5%</span>
              </div>
              <div class="w-full bg-[#E5E5E0] h-2 rounded-full overflow-hidden">
                <div class="bg-[#75452D] h-full w-0"></div>
              </div>
            </div>
          </div>

        </div>
      </section>

      <!-- Verifiable Achievements & Activity Guide -->
      <section class="bg-white rounded-xl border border-[#E5E5E0] p-6 shadow-subtle space-y-4">
        <div class="flex items-center justify-between border-b border-[#EFEFEA] pb-3">
          <div>
            <h3 class="text-sm font-bold text-[#171717] uppercase tracking-wider flex items-center space-x-2">
              <i class="fa-solid fa-shield-halved text-[#3F7D44]"></i>
              <span>Insignias Criptográficas Disponibles</span>
            </h3>
            <p class="text-xs text-[#626262]">Méritos auditables vinculados a la cuenta de Stellar del productor.</p>
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div class="p-4 bg-[#FAFAF8] rounded-xl border border-[#E5E5E0] flex items-start space-x-3">
            <div class="w-9 h-9 rounded-xl bg-[#3F7D44]/15 text-[#3F7D44] flex items-center justify-center flex-shrink-0">
              <i class="fa-solid fa-leaf text-sm"></i>
            </div>
            <div>
              <h4 class="text-xs font-bold text-[#171717]">Cero Deforestación EUDR</h4>
              <p class="text-[11px] text-[#626262] mt-0.5">Parcela validada con polígonos satelitales sin chaqueo.</p>
              <span class="inline-block mt-2 text-[10px] font-bold text-[#3F7D44]">✓ Verificado</span>
            </div>
          </div>

          <div class="p-4 bg-[#FAFAF8] rounded-xl border border-[#E5E5E0] flex items-start space-x-3">
            <div class="w-9 h-9 rounded-xl bg-[#C76A32]/15 text-[#C76A32] flex items-center justify-center flex-shrink-0">
              <i class="fa-solid fa-award text-sm"></i>
            </div>
            <div>
              <h4 class="text-xs font-bold text-[#171717]">Calidad Grado A Superior</h4>
              <p class="text-[11px] text-[#626262] mt-0.5">Más del 80% del cacao entregado con fermentación óptima.</p>
              <span class="inline-block mt-2 text-[10px] font-bold text-[#C76A32]">2/3 Entregas</span>
            </div>
          </div>

          <div class="p-4 bg-[#FAFAF8] rounded-xl border border-[#E5E5E0] flex items-start space-x-3">
            <div class="w-9 h-9 rounded-xl bg-[#D5A332]/15 text-[#D5A332] flex items-center justify-center flex-shrink-0">
              <i class="fa-solid fa-clock-rotate-left text-sm"></i>
            </div>
            <div>
              <h4 class="text-xs font-bold text-[#171717]">Puntualidad en Liquidación</h4>
              <p class="text-[11px] text-[#626262] mt-0.5">Cierre del contrato de factoring en la fecha de cosecha pactada.</p>
              <span class="inline-block mt-2 text-[10px] font-bold text-[#D5A332]">1 Liquidado</span>
            </div>
          </div>
        </div>
      </section>

    </div>

  </main>

  <!-- Modern Clean Footer -->
  <footer class="border-t border-[#E5E5E0] bg-white py-6 mt-auto">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-[#626262]">
      <div class="flex items-center space-x-2">
        <span class="font-bold text-[#171717]">KAIRO 3.0</span>
        <span>·</span>
        <span>Stellar Hackathon 2026</span>
        <span>·</span>
        <span class="text-[#C76A32] font-medium">Clean Architecture & ML Oracles</span>
      </div>
      <div class="flex items-center space-x-4">
        <span>Alto Beni & Palos Blancos, Bolivia</span>
        <a href="/docs" target="_blank" class="text-[#171717] hover:underline font-semibold">Swagger API</a>
      </div>
    </div>
  </footer>

  <!-- ==================================================================== -->
  <!-- JAVASCRIPT APPLICATION CORE (Strict preservation of all logic & APIs) -->
  <!-- ==================================================================== -->
  <script>
    // Tab switching with responsive and accessible state
    function switchTab(tabName) {
      document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('nav-tab-active');
        btn.classList.add('text-[#626262]');
      });

      const target = document.getElementById('tab-' + tabName);
      if (target) target.classList.remove('hidden');

      const activeBtns = document.querySelectorAll(`[data-tab="${tabName}"]`);
      activeBtns.forEach(b => {
        b.classList.remove('text-[#626262]');
        b.classList.add('nav-tab-active');
      });

      window.scrollTo({ top: 0, behavior: 'smooth' });

      if (tabName === 'dashboard') loadDashboardData();
      if (tabName === 'producers') loadProducersData();
    }

    function toggleMobileMenu() {
      const menu = document.getElementById('mobile-menu');
      if (menu) menu.classList.toggle('hidden');
    }

    // Weather label updater for factoring simulation
    function updateWeatherLabels() {
      const rainfall = parseInt(document.getElementById('fac-rainfall').value) || 160;
      const humidity = parseInt(document.getElementById('fac-humidity').value) || 75;

      const rLabel = document.getElementById('label-rainfall');
      if (rainfall < 80) {
        rLabel.textContent = `${rainfall} mm (Alerta Sequía)`;
        rLabel.className = 'text-xs font-bold text-[#A74445]';
      } else if (rainfall > 240) {
        rLabel.textContent = `${rainfall} mm (Riesgo Moniliasis)`;
        rLabel.className = 'text-xs font-bold text-[#C76A32]';
      } else {
        rLabel.textContent = `${rainfall} mm (Óptimo)`;
        rLabel.className = 'text-xs font-bold text-[#3F7D44]';
      }

      const hLabel = document.getElementById('label-humidity');
      if (humidity > 85) {
        hLabel.textContent = `${humidity}% (Riesgo Mazorca Negra)`;
        hLabel.className = 'text-xs font-bold text-[#A74445]';
      } else {
        hLabel.textContent = `${humidity}% (Seguro)`;
        hLabel.className = 'text-xs font-bold text-[#3F7D44]';
      }
    }

    // Delivery calculation preview (Strictly preserving original business rules)
    function calculatePreview() {
      const type = document.getElementById('del-cacao-type').value;
      const gross = parseFloat(document.getElementById('del-gross-weight').value) || 0;
      const moisture = parseFloat(document.getElementById('del-moisture').value) || 0;
      const grade = document.getElementById('del-quality').value;
      const basePrice = 4.80;

      let netWeight = gross;
      let penaltyText = 'Sin penalización';

      if (type === 'BABA') {
        netWeight = gross * 0.33;
        penaltyText = 'Factor baba 0.33x a seco';
      } else if (type === 'SECO' && moisture > 7.5) {
        const excess = (moisture - 7.5) / 100.0;
        netWeight = gross * (1.0 - excess);
        const penaltyKg = (gross * excess).toFixed(1);
        penaltyText = `Exceso humedad: -${penaltyKg} kg`;
      }

      let gradeMult = 1.0;
      if (grade === 'B') gradeMult = 0.90;
      if (grade === 'C') gradeMult = 0.75;

      const finalPrice = basePrice * gradeMult;
      const totalUSDC = netWeight * finalPrice;
      const totalBOB = totalUSDC * 6.96;

      document.getElementById('preview-net-weight').textContent = netWeight.toFixed(2) + ' kg';
      document.getElementById('preview-penalty').textContent = penaltyText;
      document.getElementById('preview-price-kg').textContent = '$' + finalPrice.toFixed(2) + ' USDC';
      document.getElementById('preview-total-bob').textContent = 'Bs. ' + totalBOB.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
      document.getElementById('preview-total').textContent = '$' + totalUSDC.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' USDC';
    }

    // Load Dashboard Metrics (Section 8 Bug Fix: supports both vaquita_pool and pool_status)
    async function loadDashboardData() {
      const icon = document.getElementById('icon-refresh');
      if (icon) icon.classList.add('fa-spin');

      try {
        const res = await fetch('/api/v1/dashboard');
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();

        // Safe extraction of pool status (resolving bug where vaquita_pool vs pool_status caused crash)
        const pool = data.vaquita_pool || data.pool_status || {};
        const poolAvail = pool.available_liquidity_usdc ?? 25000;
        const poolTotal = pool.total_liquidity_usdc ?? 25000;
        const poolRes = pool.reserved_liquidity_usdc ?? 0;

        document.getElementById('stat-pool-avail').textContent = '$' + Number(poolAvail).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
        document.getElementById('stat-pool-total').textContent = '$' + Number(poolTotal).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
        document.getElementById('stat-pool-res').textContent = '$' + Number(poolRes).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});

        const totalUSDC = data.total_advanced_usdc ?? 0;
        const totalBOB = data.total_advanced_bob ?? (totalUSDC * 6.96);
        document.getElementById('stat-total-usdc').textContent = '$' + Number(totalUSDC).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
        document.getElementById('stat-total-bob').textContent = 'Bs. ' + Number(totalBOB).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});

        document.getElementById('stat-deliveries-count').textContent = data.total_deliveries_count ?? (data.recent_deliveries?.length || 0);
        document.getElementById('stat-active-loans').textContent = data.active_loans_count ?? (data.active_loans?.length || 0);

        // Populate Deliveries Table
        const tbody = document.getElementById('recent-deliveries-body');
        if (data.recent_deliveries && data.recent_deliveries.length > 0) {
          tbody.innerHTML = data.recent_deliveries.map(d => `
            <tr class="hover:bg-[#F4F4F0] transition">
              <td class="px-4 py-3 font-mono font-bold text-[#C76A32] text-xs">${d.delivery_code}</td>
              <td class="px-4 py-3 font-semibold text-[#171717]">
                ${d.producer_name || ('Socio #' + d.producer_id)}
              </td>
              <td class="px-4 py-3">
                <span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-semibold ${d.cacao_type === 'BABA' ? 'bg-[#C76A32]/10 text-[#C76A32]' : 'bg-[#3F7D44]/10 text-[#3F7D44]'}">
                  ${d.cacao_type} · Grado ${d.quality_grade}
                </span>
              </td>
              <td class="px-4 py-3 text-xs text-[#626262]">
                <span>${d.gross_weight_kg} kg</span>
                <span class="text-[#171717] font-bold block">&rarr; ${d.net_dry_weight_kg} kg seco</span>
              </td>
              <td class="px-4 py-3 text-xs">
                <span class="font-extrabold text-[#171717]">$${d.total_amount_usdc.toFixed(2)} USDC</span>
                <span class="text-[#626262] block text-[11px]">Bs. ${d.total_amount_bob.toFixed(2)}</span>
              </td>
              <td class="px-4 py-3 text-[11px] font-mono text-[#626262] max-w-xs truncate" title="${d.stellar_tx_hash}">
                <i class="fa-solid fa-link text-[#3F7D44] mr-1"></i>${(d.stellar_tx_hash || '').substring(0, 16)}...
              </td>
              <td class="px-4 py-3 text-right">
                <span class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold bg-[#3F7D44]/15 text-[#3F7D44]">
                  ${d.status || 'NOTARIZED'}
                </span>
              </td>
            </tr>
          `).join('');
        } else {
          tbody.innerHTML = '<tr><td colspan="7" class="text-center py-6 text-[#626262]">Aún no hay boletas de acopio registradas.</td></tr>';
        }

        // Populate Active Loans Table
        const loansBody = document.getElementById('active-loans-body');
        if (data.active_loans && data.active_loans.length > 0) {
          loansBody.innerHTML = data.active_loans.map(loan => `
            <tr class="hover:bg-[#F4F4F0] transition">
              <td class="px-4 py-3 font-mono font-bold text-[#171717]">${loan.loan_code}</td>
              <td class="px-4 py-3 font-semibold text-[#171717]">${loan.producer_name || ('Socio #' + loan.producer_id)}</td>
              <td class="px-4 py-3 font-bold text-[#3F7D44]">$${loan.approved_amount_usdc.toFixed(2)} USDC</td>
              <td class="px-4 py-3 text-[#626262]">Bs. ${(loan.amount_bob || (loan.approved_amount_usdc * 6.96)).toFixed(2)}</td>
              <td class="px-4 py-3 font-mono text-[11px] text-[#626262] truncate max-w-xs" title="${loan.trustless_escrow_id}">
                ${loan.trustless_escrow_id || 'escrow_tw_...'}
              </td>
              <td class="px-4 py-3 text-right">
                <button onclick="settleLoan(${loan.id || loan.loan_id})" class="px-2.5 py-1 rounded bg-[#171717] hover:bg-black text-white text-[10px] font-bold transition">
                  Liquidar Cosecha
                </button>
              </td>
            </tr>
          `).join('');
        } else {
          loansBody.innerHTML = '<tr><td colspan="6" class="text-center py-6 text-[#626262]">No hay préstamos en escrow actualmente.</td></tr>';
        }

      } catch (err) {
        console.error('Error fetching dashboard:', err);
        const tbody = document.getElementById('recent-deliveries-body');
        if (tbody) {
          tbody.innerHTML = `<tr><td colspan="7" class="text-center py-6 text-[#A74445] font-semibold">
            <i class="fa-solid fa-triangle-exclamation mr-1.5"></i>Error al consultar el backend. Presiona "Actualizar" para reintentar.
          </td></tr>`;
        }
      } finally {
        if (icon) setTimeout(() => icon.classList.remove('fa-spin'), 400);
      }
    }

    // Load Producers & EUDR Traceability
    async function loadProducersData() {
      try {
        const res = await fetch('/api/v1/producers');
        if (!res.ok) throw new Error('Error al cargar productores');
        const producers = await res.json();

        const grid = document.getElementById('producers-grid');
        grid.innerHTML = producers.map(p => `
          <div class="bg-white rounded-2xl border border-[#E5E5E0] p-5 shadow-subtle hover:shadow-card transition flex flex-col justify-between space-y-4">
            
            <div class="flex items-start justify-between">
              <div>
                <h3 class="font-bold text-[#171717] text-base">${p.name}</h3>
                <p class="text-xs text-[#C76A32] font-semibold">${p.cooperative}</p>
                <p class="text-xs text-[#626262]">${p.community}</p>
              </div>
              <span class="px-2.5 py-1 rounded-full text-[10px] font-extrabold ${
                p.risk_tier === 'BAJO' ? 'bg-[#3F7D44]/15 text-[#3F7D44] border border-[#3F7D44]/30' :
                p.risk_tier === 'MEDIO' ? 'bg-[#D5A332]/20 text-[#75452D] border border-[#D5A332]/40' :
                'bg-[#A74445]/15 text-[#A74445] border border-[#A74445]/30'
              }">
                RIESGO ${p.risk_tier}
              </span>
            </div>

            <div class="bg-[#FAFAF8] rounded-xl p-3.5 text-xs space-y-2 border border-[#E5E5E0] font-mono">
              <div class="flex justify-between text-[#626262]">
                <span>Código Parcela:</span>
                <span class="text-[#171717] font-bold">${p.eudr_plot_code}</span>
              </div>
              <div class="flex justify-between text-[#626262]">
                <span>Superficie:</span>
                <span class="text-[#171717] font-semibold">${p.parcel_hectares || p.hectares || 2.5} ha (${p.tree_age_years || 8} años)</span>
              </div>
              <div class="flex justify-between text-[#626262]">
                <span>Coordenadas GPS:</span>
                <span class="text-[#3F7D44] font-semibold text-[11px]">${p.eudr_latitude}, ${p.eudr_longitude}</span>
              </div>
              <div class="flex justify-between text-[#626262]">
                <span>Trazabilidad EUDR:</span>
                <span class="${p.eudr_certified ? 'text-[#3F7D44] font-bold' : 'text-[#626262]'}">
                  ${p.eudr_certified ? '✓ Registro Cero Deforestación' : 'Documentación en revisión'}
                </span>
              </div>
            </div>

            <div class="flex items-center justify-between text-xs pt-2 border-t border-[#EFEFEA] text-[#626262]">
              <span>Score Histórico:</span>
              <span class="font-extrabold text-[#171717]">${((p.compliance_score || 0.90) * 100).toFixed(0)}% de cumplimiento</span>
            </div>

          </div>
        `).join('');
      } catch (err) {
        console.error('Error fetching producers:', err);
      }
    }

    // Submit Delivery (Section 10: 3 stages, duplicates prevented, confirmation with KAIRO mascot)
    async function submitDelivery(e) {
      e.preventDefault();
      const btn = document.getElementById('btn-submit-delivery');
      const btnText = document.getElementById('btn-submit-delivery-text');
      btn.disabled = true;
      btnText.textContent = 'Notarizando ticket en Stellar Testnet...';

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
            <div>• <strong>Código de Boleta:</strong> <span class="text-[#C76A32] font-bold">${data.delivery_code}</span></div>
            <div>• <strong>Peso Neto Seco:</strong> ${data.net_dry_weight_kg} kg (Descuento penalidad: ${data.penalty_discount_kg} kg)</div>
            <div>• <strong>Total Liquidado:</strong> $${data.total_amount_usdc.toFixed(2)} USDC &bull; Bs. ${data.total_amount_bob.toFixed(2)}</div>
            <div>• <strong>Hash SHA-256 Boleta:</strong> <span class="text-[#626262] break-all">${data.payload_hash}</span></div>
            <div>• <strong>Stellar Transaction Hash:</strong> <span class="text-[#3F7D44] font-bold break-all">${data.stellar_tx_hash}</span></div>
          `;
          
          // Switch to Step 3 visually
          document.getElementById('step-pill-1').className = 'py-2 rounded-lg text-[#626262]';
          document.getElementById('step-pill-2').className = 'py-2 rounded-lg text-[#626262]';
          document.getElementById('step-pill-3').className = 'py-2 rounded-lg bg-white text-[#171717] shadow-subtle border border-[#E5E5E0] font-bold';

          loadDashboardData();
          resBox.scrollIntoView({ behavior: 'smooth' });
        } else {
          alert('Error al registrar boleta: ' + (data.detail || 'Ocurrió un error en el servidor'));
        }
      } catch (err) {
        alert('Error de conexión: ' + err.message);
      } finally {
        btn.disabled = false;
        btnText.textContent = 'Etapa 3 · Emitir Boleta & Notarizar en Stellar';
      }
    }

    function dismissDeliveryResult() {
      document.getElementById('delivery-result-box').classList.add('hidden');
      document.getElementById('step-pill-1').className = 'py-2 rounded-lg bg-white text-[#171717] shadow-subtle border border-[#E5E5E0] font-bold';
      document.getElementById('step-pill-2').className = 'py-2 rounded-lg text-[#626262]';
      document.getElementById('step-pill-3').className = 'py-2 rounded-lg text-[#626262]';
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
          document.getElementById('res-risk-tier').className = 'text-base font-extrabold ' + (
            data.risk_level === 'BAJO' ? 'text-[#3F7D44]' :
            data.risk_level === 'MEDIO' ? 'text-[#D5A332]' : 'text-[#A74445]'
          );
          document.getElementById('res-risk-score').textContent = 'Score: ' + data.risk_score + ' / 100';
          document.getElementById('res-advance-pct').textContent = data.approved_advance_pct + '%';
          document.getElementById('res-advance-amount').textContent = '$' + data.max_advance_usdc.toFixed(2) + ' USDC';
          document.getElementById('res-advance-bob').textContent = '(Bs. ' + data.max_advance_bob.toFixed(2) + ')';

          document.getElementById('exec-requested-amount').value = Math.min(800, data.max_advance_usdc);

          const list = document.getElementById('res-factors-list');
          list.innerHTML = (data.risk_factors || []).map(f => `<li>${f}</li>`).join('');
        } else {
          alert('Error en simulación: ' + (data.detail || 'Error'));
        }
      } catch (err) {
        alert('Error de conexión: ' + err.message);
      } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-microchip mr-2"></i>Calcular Capacidad de Factoring con Oráculo';
      }
    }

    // Execute Loan & Generate Pollar Simple QR
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

          document.getElementById('qr-amount-bob').textContent = 'Bs. ' + (data.amount_bob || (data.approved_amount_usdc * 6.96)).toFixed(2);
          document.getElementById('qr-payout-id').textContent = data.pollar_payout_id || 'pol_out_confirmed';
          document.getElementById('qr-vaquita-res').textContent = data.vaquita_reservation_id;
          document.getElementById('qr-escrow-id').textContent = data.trustless_escrow_id;
          document.getElementById('qr-deep-link').href = data.qr_deep_link || '#';

          loadDashboardData();
          qrView.scrollIntoView({ behavior: 'smooth' });
        } else {
          alert('Error al ejecutar factoring: ' + (data.detail || 'Ocurrió un error'));
        }
      } catch (err) {
        alert('Error de conexión: ' + err.message);
      } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-bolt mr-2 text-[#D5A332]"></i>Desembolsar Inmediato (Pollar Simple QR en Bs.)';
      }
    }

    // Settle Loan Operation
    async function settleLoan(loanId) {
      if (!confirm(`¿Confirmas la liquidación y entrega final de cosecha para el préstamo #${loanId}?`)) return;
      try {
        const res = await fetch(`/api/v1/factoring/${loanId}/settle`, { method: 'POST' });
        const data = await res.json();
        if (res.ok) {
          alert(`Liquidación completada. Se liberó el escrow de Trustless Work y se acreditaron las comisiones al Pool Vaquita.`);
          loadDashboardData();
        } else {
          alert('Error al liquidar préstamo: ' + (data.detail || 'Error'));
        }
      } catch (err) {
        alert('Error de conexión: ' + err.message);
      }
    }

    // Two-Stage ML Yield Estimation
    async function estimateYield() {
      const btn = document.getElementById('btn-ml-yield');
      btn.disabled = true;
      btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-2"></i>Iniciando modelo Two-Stage...';

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
          alert('Error en estimación Two-Stage: ' + (data.detail || 'Error'));
        }
      } catch (err) {
        alert('Error de conexión: ' + err.message);
      } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-microchip mr-2"></i>Inferir Rendimiento con LightGBM';
      }
    }

    // ICCO Price Forecast
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
          trendSpan.textContent = (data.trend || 'NEUTRAL').toUpperCase();
          if (data.trend === 'bullish') {
            trendSpan.className = 'px-2 py-0.5 rounded-full text-[10px] font-bold bg-[#3F7D44]/15 text-[#3F7D44]';
          } else if (data.trend === 'bearish') {
            trendSpan.className = 'px-2 py-0.5 rounded-full text-[10px] font-bold bg-[#A74445]/15 text-[#A74445]';
          } else {
            trendSpan.className = 'px-2 py-0.5 rounded-full text-[10px] font-bold bg-[#D5A332]/20 text-[#75452D]';
          }
        } else {
          alert('Error en pronóstico de precios: ' + (data.detail || 'Error'));
        }
      } catch (err) {
        alert('Error de conexión: ' + err.message);
      } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-chart-line mr-2 text-[#D5A332]"></i>Simular Trayectoria de Precios';
      }
    }

    // Initial boot on DOM load
    document.addEventListener('DOMContentLoaded', () => {
      calculatePreview();
      loadDashboardData();
    });

    // ====================================================================
    // AUTO-DEMO AUTOMATION ENGINE (Designed for Screen Recording & Pitch)
    // ====================================================================
    let autoDemoRunning = false;
    let autoDemoPaused = false;
    let autoDemoAbort = false;
    let autoDemoNextRequested = false;
    let countdownTimer = null;

    function startAutoDemo() {
      document.getElementById('autodemo-countdown-modal').classList.remove('hidden');
      let count = 5;
      document.getElementById('countdown-number').textContent = count;
      if (countdownTimer) clearInterval(countdownTimer);
      countdownTimer = setInterval(() => {
        count--;
        if (count > 0) {
          document.getElementById('countdown-number').textContent = count;
        } else {
          clearInterval(countdownTimer);
          startAutoDemoImmediate();
        }
      }, 1000);
    }

    function cancelCountdown() {
      if (countdownTimer) clearInterval(countdownTimer);
      document.getElementById('autodemo-countdown-modal').classList.add('hidden');
    }

    function stopAutoDemo() {
      autoDemoAbort = true;
      autoDemoRunning = false;
      autoDemoPaused = false;
      document.getElementById('autodemo-teleprompter').classList.add('hidden');
      const ptr = document.getElementById('autodemo-pointer');
      if (ptr) ptr.classList.add('hidden');
      document.getElementById('autodemo-countdown-modal').classList.add('hidden');
    }

    function togglePauseAutoDemo() {
      autoDemoPaused = !autoDemoPaused;
      const btn = document.getElementById('btn-pause-demo');
      if (autoDemoPaused) {
        btn.innerHTML = '<i class="fa-solid fa-play mr-1"></i>Reanudar';
        btn.className = 'px-2.5 py-1 rounded-lg bg-[#3F7D44] text-white font-semibold transition';
      } else {
        btn.innerHTML = '<i class="fa-solid fa-pause mr-1"></i>Pausar';
        btn.className = 'px-2.5 py-1 rounded-lg bg-white/10 hover:bg-white/20 text-white font-semibold transition';
      }
    }

    function skipNextAutoDemoStep() {
      autoDemoNextRequested = true;
    }

    function sleepDemo(ms) {
      return new Promise(resolve => {
        const start = Date.now();
        const interval = setInterval(() => {
          if (autoDemoAbort || autoDemoNextRequested) {
            clearInterval(interval);
            autoDemoNextRequested = false;
            resolve();
          } else if (!autoDemoPaused) {
            if (Date.now() - start >= ms) {
              clearInterval(interval);
              resolve();
            }
          }
        }, 80);
      });
    }

    function updateTeleprompter(stepNum, totalSteps, title, timeStr, text, progressPct) {
      document.getElementById('demo-step-badge').textContent = `Paso ${stepNum} de ${totalSteps} · ${title} (${timeStr})`;
      document.getElementById('demo-teleprompter-text').textContent = text;
      document.getElementById('demo-progress-bar').style.width = `${progressPct}%`;
    }

    function movePointer(selectorOrEl) {
      const el = typeof selectorOrEl === 'string' ? document.querySelector(selectorOrEl) : selectorOrEl;
      const pointer = document.getElementById('autodemo-pointer');
      if (!el || !pointer) return;
      pointer.classList.remove('hidden');
      const rect = el.getBoundingClientRect();
      pointer.style.left = `${rect.left + rect.width / 2}px`;
      pointer.style.top = `${rect.top + rect.height / 2}px`;
      el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    async function typeValue(inputSelector, targetText, duration = 800) {
      const input = typeof inputSelector === 'string' ? document.querySelector(inputSelector) : inputSelector;
      if (!input) return;
      input.focus();
      input.value = '';
      const textStr = String(targetText);
      const stepTime = Math.max(30, duration / textStr.length);
      for (let i = 0; i < textStr.length; i++) {
        if (autoDemoAbort) return;
        input.value += textStr[i];
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
        await sleepDemo(stepTime);
      }
    }

    async function startAutoDemoImmediate() {
      if (countdownTimer) clearInterval(countdownTimer);
      document.getElementById('autodemo-countdown-modal').classList.add('hidden');
      document.getElementById('autodemo-teleprompter').classList.remove('hidden');

      autoDemoRunning = true;
      autoDemoPaused = false;
      autoDemoAbort = false;
      autoDemoNextRequested = false;

      // 1. Reset demo state silently so all metrics start clean
      try {
        await fetch('/api/v1/dashboard/reset-demo', { method: 'POST' });
        loadDashboardData();
      } catch(e) {}

      // ==========================================
      // PASO 1: DASHBOARD & MASCOTA KAIRO (0:00 - 0:25)
      // ==========================================
      switchTab('dashboard');
      window.scrollTo({ top: 0, behavior: 'smooth' });
      updateTeleprompter(1, 6, 'Dashboard & Mascota KAIRO', '0:00 / 02:30',
        'Bienvenido a KAIRO 3.0: la plataforma AgriTech & FinTech construida sobre Stellar para las cooperativas cacaoteras de Alto Beni, Palos Blancos y Sapecho.',
        8
      );
      movePointer('img[alt="Kairo la mascota oficial de cacao"]');
      await sleepDemo(8000);
      if (autoDemoAbort) return;

      updateTeleprompter(1, 6, 'Dashboard · Métricas Financieras', '0:12 / 02:30',
        'Conectamos liquidez descentralizada vía Vaquita Pool ($25,000 USDC iniciales) con acopio transparente y boletas inmutables en Stellar.',
        16
      );
      movePointer('#stat-pool-avail');
      await sleepDemo(5000);
      if (autoDemoAbort) return;

      movePointer('#recent-deliveries-body');
      await sleepDemo(6000);
      if (autoDemoAbort) return;

      // ==========================================
      // PASO 2: EUDR & PARCELAS GEORREFERENCIADAS (0:25 - 0:50)
      // ==========================================
      switchTab('producers');
      updateTeleprompter(2, 6, 'EUDR & Trazabilidad Satelital', '0:25 / 02:30',
        'El reglamento europeo EUDR 2023/1115 exige cero deforestación. KAIRO georreferencia cada parcela para habilitar la exportación del cacao boliviano.',
        28
      );
      await sleepDemo(4000);
      if (autoDemoAbort) return;

      movePointer('#producers-grid > div:first-child');
      updateTeleprompter(2, 6, 'Socio Mateo Mamani · El Ceibo', '0:35 / 02:30',
        'Don Mateo Mamani en Sapecho tiene 4.5 ha certificadas (BO-LPZ-AB-ELCEIBO-001) y 96% de cumplimiento, convirtiendo su compromiso ambiental en un activo.',
        40
      );
      await sleepDemo(12000);
      if (autoDemoAbort) return;

      // ==========================================
      // PASO 3: ACOPIO & NOTARIZACIÓN STELLAR (0:50 - 01:25)
      // ==========================================
      switchTab('deliveries');
      window.scrollTo({ top: 0, behavior: 'smooth' });
      updateTeleprompter(3, 6, 'Acopio Digital en Balanza', '0:50 / 02:30',
        'En el centro de acopio digitalizamos el pesaje. Seleccionamos a Don Mateo: 1,000 kg de cacao en baba con 55% de humedad.',
        48
      );
      movePointer('#del-producer-id');
      document.getElementById('del-producer-id').value = '1';
      document.getElementById('del-cacao-type').value = 'BABA';
      await sleepDemo(3000);
      if (autoDemoAbort) return;

      movePointer('#del-gross-weight');
      await typeValue('#del-gross-weight', '1000', 600);
      await sleepDemo(1000);
      if (autoDemoAbort) return;

      movePointer('#del-moisture');
      await typeValue('#del-moisture', '55.0', 600);
      calculatePreview();
      await sleepDemo(2000);
      if (autoDemoAbort) return;

      updateTeleprompter(3, 6, 'Cálculo Agronómico en Vivo', '01:04 / 02:30',
        'La fórmula calcula 330 kg netos secos y una liquidación de $1,584 USDC (Bs. 11,024). Notarizamos el comprobante en Stellar.',
        58
      );
      movePointer('#preview-total');
      await sleepDemo(4000);
      if (autoDemoAbort) return;

      movePointer('#btn-submit-delivery');
      await sleepDemo(1500);
      document.getElementById('delivery-form').dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));

      await sleepDemo(3000);
      updateTeleprompter(3, 6, 'Boleta Notarizada en Stellar', '01:14 / 02:30',
        '¡Boleta blindada! KAIRO genera el hash canónico SHA-256 grabado en el Memo Hash de Stellar, haciendo imposible alterar el pesaje o el pago.',
        65
      );
      movePointer('#delivery-result-box');
      await sleepDemo(10000);
      if (autoDemoAbort) return;

      // ==========================================
      // PASO 4: FACTORING ML & SIMPLE QR (01:25 - 01:55)
      // ==========================================
      switchTab('factoring');
      window.scrollTo({ top: 0, behavior: 'smooth' });
      updateTeleprompter(4, 6, 'Factoring ML & Oráculo Climático', '01:25 / 02:30',
        'Antes de la cosecha, el productor necesita capital. El oráculo climático evalúa precipitación y humedad relativa de Alto Beni.',
        70
      );
      document.getElementById('fac-rainfall').value = 160;
      document.getElementById('fac-humidity').value = 75;
      updateWeatherLabels();
      movePointer('#fac-rainfall');
      await sleepDemo(4000);
      if (autoDemoAbort) return;

      movePointer('#btn-simulate');
      await sleepDemo(1500);
      await runSimulation();

      updateTeleprompter(4, 6, 'Cupo Pre-Aprobado & Escrow', '01:36 / 02:30',
        'Diagnóstico: Riesgo Bajo. Pre-aprobado $3,816 USDC. Don Mateo solicita $800 para cosecha: se reserva liquidez en Vaquita y contrato Trustless Work.',
        78
      );
      movePointer('#res-advance-amount');
      await sleepDemo(5000);
      if (autoDemoAbort) return;

      movePointer('#exec-requested-amount');
      document.getElementById('exec-requested-amount').value = '800';
      await sleepDemo(1500);
      if (autoDemoAbort) return;

      movePointer('#btn-exec-loan');
      await sleepDemo(1500);
      await executeLoan();

      updateTeleprompter(4, 6, 'Desembolso Simple QR en Bolivianos', '01:45 / 02:30',
        'A través de Pollar, se emite una orden Simple QR por Bs. 5,568.00. Don Mateo cobra al instante en su banco sin lidiar con criptomonedas.',
        84
      );
      movePointer('#qr-modal-view');
      await sleepDemo(10000);
      if (autoDemoAbort) return;

      // ==========================================
      // PASO 5: TWO-STAGE ML & PRECIOS ICCO (01:55 - 02:15)
      // ==========================================
      switchTab('ml-forecast');
      window.scrollTo({ top: 0, behavior: 'smooth' });
      updateTeleprompter(5, 6, 'Modelo Two-Stage (LightGBM)', '01:55 / 02:30',
        'Para mitigar el riesgo crediticio, integramos un modelo Two-Stage (LightGBM) que infiere la cosecha por biometría (53.85 kg/ha con 95.1% probabilidad).',
        88
      );
      movePointer('#btn-ml-yield');
      await sleepDemo(2000);
      await estimateYield();
      movePointer('#ml-yield-result');
      await sleepDemo(6000);
      if (autoDemoAbort) return;

      updateTeleprompter(5, 6, 'Proyección Precios Internacionales ICCO', '02:05 / 02:30',
        'Simulamos la trayectoria del mercado internacional de cacao a 30 días con bandas de confianza al 95%, protegiendo a la cooperativa de la volatilidad.',
        94
      );
      movePointer('#btn-ml-price');
      await sleepDemo(2000);
      await forecastPrice();
      movePointer('#ml-price-result');
      await sleepDemo(7000);
      if (autoDemoAbort) return;

      // ==========================================
      // PASO 6: PROGRESO & CIERRE (02:15 - 02:30)
      // ==========================================
      switchTab('progress');
      window.scrollTo({ top: 0, behavior: 'smooth' });
      updateTeleprompter(6, 6, 'Progreso & Gamificación KAIRO', '02:15 / 02:30',
        'Nuestra mascota KAIRO y el sistema de niveles premian las buenas prácticas agrícolas con insignias criptográficas verificables en Stellar.',
        98
      );
      movePointer('img[alt="Kairo te acompaña en tu progreso"]');
      await sleepDemo(7000);
      if (autoDemoAbort) return;

      switchTab('dashboard');
      window.scrollTo({ top: 0, behavior: 'smooth' });
      updateTeleprompter(6, 6, 'Demostración Finalizada', '02:30 / 02:30',
        'KAIRO une inteligencia artificial, finanzas regenerativas y la red Stellar para empoderar al productor de cacao boliviano. ¡Gracias!',
        100
      );
      movePointer('#stat-deliveries-count');
      await sleepDemo(6000);

      document.getElementById('demo-step-badge').textContent = '✅ Demo Completa · ¡Detén tu grabación!';
      document.getElementById('demo-teleprompter-text').textContent = '🎬 ¡Demostración guiada completada exitosamente! Puedes detener tu grabador de pantalla.';
      const ptr = document.getElementById('autodemo-pointer');
      if (ptr) ptr.classList.add('hidden');
    }
  </script>

  <!-- ==================================================================== -->
  <!-- FLOATING AUTO-DEMO TELEPROMPTER, POINTER & COUNTDOWN MODAL OVERLAYS   -->
  <!-- ==================================================================== -->

  <!-- Floating Teleprompter Bar -->
  <div id="autodemo-teleprompter" class="hidden fixed bottom-6 left-1/2 -translate-x-1/2 z-50 w-[94vw] max-w-3xl bg-[#171717]/95 backdrop-blur-md text-white rounded-2xl p-4 sm:p-5 shadow-2xl border border-white/15 space-y-2.5 transition-all duration-300">
    <div class="flex items-center justify-between gap-2 border-b border-white/10 pb-2">
      <div class="flex items-center space-x-2">
        <span class="w-2.5 h-2.5 rounded-full bg-[#C76A32] animate-pulse"></span>
        <span id="demo-step-badge" class="px-2.5 py-0.5 rounded-full bg-white/10 text-white text-[11px] font-bold">
          Paso 1 de 6 · Dashboard (0:00 / 02:30)
        </span>
      </div>
      <div class="flex items-center space-x-1.5 text-xs">
        <button onclick="togglePauseAutoDemo()" id="btn-pause-demo" class="px-2.5 py-1 rounded-lg bg-white/10 hover:bg-white/20 text-white font-semibold transition flex items-center space-x-1">
          <i class="fa-solid fa-pause text-[10px]"></i>
          <span>Pausar</span>
        </button>
        <button onclick="skipNextAutoDemoStep()" class="px-2.5 py-1 rounded-lg bg-white/10 hover:bg-white/20 text-white font-semibold transition flex items-center space-x-1">
          <i class="fa-solid fa-forward-step text-[10px]"></i>
          <span>Saltar</span>
        </button>
        <button onclick="stopAutoDemo()" class="px-2.5 py-1 rounded-lg bg-[#A74445]/30 text-red-300 hover:bg-[#A74445]/50 font-semibold transition flex items-center space-x-1">
          <i class="fa-solid fa-stop text-[10px]"></i>
          <span>Detener</span>
        </button>
      </div>
    </div>
    <div class="text-xs sm:text-sm font-medium text-white/95 leading-relaxed min-h-[42px] flex items-center" id="demo-teleprompter-text">
      Iniciando demostración guiada...
    </div>
    <div class="w-full bg-white/10 h-1.5 rounded-full overflow-hidden">
      <div id="demo-progress-bar" class="bg-gradient-to-r from-[#C76A32] via-[#D5A332] to-[#3F7D44] h-full w-0 transition-all duration-300"></div>
    </div>
  </div>

  <!-- Virtual Laser Spotlight Pointer -->
  <div id="autodemo-pointer" class="hidden fixed pointer-events-none z-50 w-8 h-8 rounded-full border-2 border-[#C76A32] bg-[#C76A32]/40 shadow-lg transform -translate-x-1/2 -translate-y-1/2 transition-all duration-700 ease-out flex items-center justify-center">
    <div class="w-2.5 h-2.5 rounded-full bg-white shadow-sm animate-ping"></div>
  </div>

  <!-- Countdown Modal Overlay -->
  <div id="autodemo-countdown-modal" class="hidden fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-white rounded-3xl p-6 sm:p-8 max-w-md w-full text-center space-y-4 shadow-2xl border border-[#E5E5E0]">
      <div class="w-20 h-20 mx-auto">
        <img src="/static/kairo-mascot-transparent.png" alt="Kairo" class="w-full h-full object-contain mascot-shadow" onerror="this.src='/kairo-mascot-transparent.png'">
      </div>
      <div class="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-[#C76A32]/10 text-[#C76A32] text-xs font-bold">
        <i class="fa-solid fa-video"></i>
        <span>Modo Grabación de Demostración</span>
      </div>
      <h3 class="text-xl font-display font-extrabold text-[#171717]">¡Prepara tu Grabador de Pantalla!</h3>
      <p class="text-xs text-[#626262]">
        Inicia tu grabación (QuickTime, OBS o atajo de pantalla). El sistema conducirá la plataforma automáticamente por los 6 módulos mostrando el valor de Stellar.
      </p>
      <div class="text-6xl font-black text-[#C76A32] font-mono py-2" id="countdown-number">
        5
      </div>
      <div class="flex justify-center space-x-3 pt-2">
        <button onclick="startAutoDemoImmediate()" class="px-4 py-2 rounded-xl bg-[#171717] hover:bg-black text-white text-xs font-bold transition">
          Empezar Ahora Mismo
        </button>
        <button onclick="cancelCountdown()" class="px-4 py-2 rounded-xl bg-white border border-[#E5E5E0] text-xs font-semibold text-[#626262] hover:bg-[#F4F4F0] transition">
          Cancelar
        </button>
      </div>
    </div>
  </div>

</body>
</html>
"""
