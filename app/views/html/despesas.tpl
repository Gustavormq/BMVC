<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BMVC Finance · Controle de Gastos Pessoais</title>
    <!-- Carregamento do CSS externo obrigatório no BMVC -->
    <link rel="stylesheet" type="text/css" href="/static/css/despesas.css">
    <!-- Chart.js para os gráficos de pizza e linha -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>

    <!-- Cabeçalho Principal -->
    <header class="app-header">
        <div class="header-container">
            <div class="brand">
                <div class="brand-icon">💰</div>
                <div>
                    <h1>BMVC Finance</h1>
                    <p class="subtitle">Gestor de Despesas &bull; Arquitetura Bottle MVC Completa</p>
                </div>
            </div>
            <div class="header-actions">
                <a href="/export" class="btn btn-sm btn-outline" title="Exportar todos os lançamentos em CSV">
                    📥 Exportar CSV
                </a>
                % if defined('current_user') and current_user:
                <div class="header-badge">
                    <span class="status-dot"></span> 👤 {{current_user.username}}
                </div>
                <form action="/logout" method="POST" style="display:inline;">
                    <button type="submit" class="btn btn-sm btn-outline" title="Sair da conta">🚪 Sair</button>
                </form>
                % else:
                <a href="/portal" class="btn btn-sm btn-outline" title="Acessar Portal de Login (Nível 3)">
                    🔐 Login / Portal
                </a>
                <div class="header-badge">
                    <span class="status-dot"></span> Servidor Ativo (Bottle MVC)
                </div>
                % end
            </div>
        </div>
    </header>

    <main class="main-container">

        % if defined('msg') and msg:
        <div class="alert alert-success">
            ✅ {{msg}}
        </div>
        % end

        % if defined('err') and err:
        <div class="alert alert-error">
            ⚠️ {{err}}
        </div>
        % end

        <!-- Cards de Resumo Financeiro -->
        <section class="summary-grid">
            <div class="summary-card card-income">
                <div class="card-info">
                    <span class="card-label">Total de Receitas</span>
                    <h2 id="total-income" class="card-value">R$ {{f"{total_income:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if defined('total_income') else '0,00'}}</h2>
                </div>
                <div class="card-icon">⬆️</div>
            </div>

            <div class="summary-card card-expense">
                <div class="card-info">
                    <span class="card-label">Total de Despesas</span>
                    <h2 id="total-expense" class="card-value">R$ {{f"{total_expense:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if defined('total_expense') else '0,00'}}</h2>
                </div>
                <div class="card-icon">⬇️</div>
            </div>

            <div class="summary-card card-balance">
                <div class="card-info">
                    <span class="card-label">Saldo Atual</span>
                    <h2 id="current-balance" class="card-value">R$ {{f"{balance:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if defined('balance') else '0,00'}}</h2>
                </div>
                <div class="card-icon">💼</div>
            </div>
        </section>

        <!-- Seção Principal de Conteúdo -->
        <div class="content-grid">

            <!-- Coluna Esquerda: Formulário e Métricas -->
            <div class="left-column">

                <!-- Formulário de Novo Lançamento -->
                <section class="panel-card">
                    <div class="panel-header">
                        <h3>➕ Novo Lançamento</h3>
                    </div>
                    <form id="transaction-form" method="POST" action="/add" class="form-grid">
                        <div class="form-group">
                            <label for="type">Tipo</label>
                            <select id="type" name="type" required>
                                <option value="despesa" selected>Despesa (Saída)</option>
                                <option value="receita">Receita (Entrada)</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="description">Descrição</label>
                            <input type="text" id="description" name="description" placeholder="Ex: Supermercado, Salário..." required>
                        </div>

                        <div class="form-group">
                            <label for="amount">Valor (R$)</label>
                            <input type="number" id="amount" name="amount" step="0.01" min="0.01" placeholder="0,00" required>
                        </div>

                        <div class="form-group">
                            <label for="category">Categoria</label>
                            <select id="category" name="category" required>
                                % for c in (categories if defined('categories') else ['Alimentação', 'Transporte', 'Moradia', 'Aluguel', 'Contas', 'Lazer', 'Saúde', 'Salário', 'Outros']):
                                <option value="{{c}}">{{c}}</option>
                                % end
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="date">Data</label>
                            <input type="date" id="date" name="date" value="{{today if defined('today') else ''}}" required>
                        </div>

                        <button type="submit" class="btn btn-primary">
                            Registrar Lançamento
                        </button>
                    </form>
                </section>

                <!-- Distribuição de Despesas por Categoria -->
                <section class="panel-card">
                    <div class="panel-header">
                        <h3>📊 Gastos por Categoria (%)</h3>
                    </div>
                    <div id="category-bars" class="category-list">
                        <!-- Gerado via JavaScript -->
                    </div>
                </section>

            </div>

            <!-- Coluna Direita: Filtros, Tabela e Gráficos -->
            <div class="right-column">

                <!-- Painel de Filtros Avançados (Data, Categoria, Tipo e Busca) -->
                <section class="panel-card">
                    <div class="panel-header extrato-header">
                        <h3>🔍 Filtros de Período e Categoria</h3>
                        <div class="filter-controls">
                            <button type="button" class="filter-btn active" data-filter="all">Todos</button>
                            <button type="button" class="filter-btn" data-filter="despesa">Despesas</button>
                            <button type="button" class="filter-btn" data-filter="receita">Receitas</button>
                        </div>
                    </div>

                    <form id="filter-form" method="GET" action="/despesas" class="filter-grid">
                        <div class="form-group">
                            <label for="filter-start">Data Início</label>
                            <input type="date" id="filter-start" name="start" value="{{start if defined('start') else ''}}">
                        </div>

                        <div class="form-group">
                            <label for="filter-end">Data Fim</label>
                            <input type="date" id="filter-end" name="end" value="{{end if defined('end') else ''}}">
                        </div>

                        <div class="form-group">
                            <label for="filter-category">Categoria</label>
                            <select id="filter-category" name="category">
                                <option value="">Todas as Categorias</option>
                                % for c in (categories if defined('categories') else []):
                                <option value="{{c}}" {{'selected' if defined('selected_category') and selected_category == c else ''}}>{{c}}</option>
                                % end
                            </select>
                        </div>

                        <div class="filter-actions">
                            <button type="button" id="btn-clear-filters" class="btn btn-sm btn-outline">
                                Limpar Filtros
                            </button>
                        </div>
                    </form>

                    <div class="search-bar" style="margin-top: 1rem; margin-bottom: 0;">
                        <input type="text" id="search-input" name="search" value="{{search if defined('search') else ''}}" placeholder="🔍 Buscar por descrição ou categoria...">
                        <button type="button" id="btn-reset-data" class="btn btn-sm btn-outline" title="Restaurar dados padrão para demonstração">
                            🔄 Dados Exemplo
                        </button>
                    </div>
                </section>

                <!-- Tabela de Extrato -->
                <section class="panel-card">
                    <div class="panel-header extrato-header">
                        <h3>📋 Extrato de Lançamentos</h3>
                        <a href="/export" class="btn btn-sm btn-outline">📥 Baixar CSV</a>
                    </div>

                    <div class="table-responsive">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Tipo</th>
                                    <th>Data</th>
                                    <th>Descrição</th>
                                    <th>Categoria</th>
                                    <th>Valor</th>
                                    <th>Ações</th>
                                </tr>
                            </thead>
                            <tbody id="transaction-table-body">
                                <!-- Preenchido e sincronizado via JS + API Backend -->
                            </tbody>
                        </table>
                    </div>

                    <div id="empty-state" class="empty-state hidden">
                        <p>Nenhum lançamento encontrado para os filtros selecionados.</p>
                    </div>
                </section>

                <!-- Gráficos Interativos (Migrados do Expense-Tracker) -->
                <div class="charts-grid">
                    <section class="panel-card">
                        <div class="panel-header">
                            <h3>🍕 Despesas por Categoria</h3>
                        </div>
                        <div class="chart-container">
                            <canvas id="catChart" height="180"></canvas>
                        </div>
                    </section>

                    <section class="panel-card">
                        <div class="panel-header">
                            <h3>📈 Gastos ao Longo do Tempo</h3>
                        </div>
                        <div class="chart-container">
                            <canvas id="dayChart" height="180"></canvas>
                        </div>
                    </section>
                </div>

            </div>

        </div>

    </main>

    <!-- Notificações Toast do JS -->
    <div id="toast" class="toast"></div>

    <footer class="app-footer">
        <p>Projeto Acadêmico &bull; BMVC Finance &bull; Padrão Arquitetural Model-View-Controller (Bottle)</p>
    </footer>

    <!-- Dados iniciais injetados pelo Controller (Backend Bottle) -->
    <script>
        window.INITIAL_TRANSACTIONS = {{!expenses_json if defined('expenses_json') else 'null'}};
    </script>

    <!-- Carregamento do JS externo obrigatório no BMVC -->
    <script src="/static/js/despesas.js"></script>
</body>
</html>
