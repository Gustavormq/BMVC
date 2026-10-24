<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BMVC Finance · Controle de Gastos Pessoais</title>
    <!-- Carregamento do CSS externo obrigatório no BMVC -->
    <link rel="stylesheet" type="text/css" href="/static/css/despesas.css">
</head>
<body>

    <!-- Cabeçalho Principal -->
    <header class="app-header">
        <div class="header-container">
            <div class="brand">
                <div class="brand-icon">💰</div>
                <div>
                    <h1>BMVC Finance</h1>
                    <p class="subtitle">Gestor de Despesas &bull; Arquitetura Bottle MVC (Nível 1)</p>
                </div>
            </div>
            <div class="header-badge">
                <span class="status-dot"></span> Servidor Ativo (Bottle 0.13)
            </div>
        </div>
    </header>

    <main class="main-container">

        <!-- Cards de Resumo Financeiro -->
        <section class="summary-grid">
            <div class="summary-card card-income">
                <div class="card-info">
                    <span class="card-label">Total de Receitas</span>
                    <h2 id="total-income" class="card-value">R$ 0,00</h2>
                </div>
                <div class="card-icon">⬆️</div>
            </div>

            <div class="summary-card card-expense">
                <div class="card-info">
                    <span class="card-label">Total de Despesas</span>
                    <h2 id="total-expense" class="card-value">R$ 0,00</h2>
                </div>
                <div class="card-icon">⬇️</div>
            </div>

            <div class="summary-card card-balance">
                <div class="card-info">
                    <span class="card-label">Saldo Atual</span>
                    <h2 id="current-balance" class="card-value">R$ 0,00</h2>
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
                    <form id="transaction-form" class="form-grid">
                        <div class="form-group">
                            <label for="type">Tipo</label>
                            <select id="type" required>
                                <option value="despesa" selected>Despesa (Saída)</option>
                                <option value="receita">Receita (Entrada)</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="description">Descrição</label>
                            <input type="text" id="description" placeholder="Ex: Supermercado, Salário..." required>
                        </div>

                        <div class="form-group">
                            <label for="amount">Valor (R$)</label>
                            <input type="number" id="amount" step="0.01" min="0.01" placeholder="0,00" required>
                        </div>

                        <div class="form-group">
                            <label for="category">Categoria</label>
                            <select id="category" required>
                                <option value="Alimentação">Alimentação</option>
                                <option value="Transporte">Transporte</option>
                                <option value="Moradia">Moradia</option>
                                <option value="Lazer">Lazer</option>
                                <option value="Saúde">Saúde</option>
                                <option value="Salário">Salário</option>
                                <option value="Outros">Outros</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="date">Data</label>
                            <input type="date" id="date" required>
                        </div>

                        <button type="submit" class="btn btn-primary">
                            Registrar Lançamento
                        </button>
                    </form>
                </section>

                <!-- Distribuição de Despesas por Categoria -->
                <section class="panel-card">
                    <div class="panel-header">
                        <h3>📊 Gastos por Categoria</h3>
                    </div>
                    <div id="category-bars" class="category-list">
                        <!-- Gerado via JavaScript -->
                    </div>
                </section>

            </div>

            <!-- Coluna Direita: Tabela e Filtros -->
            <div class="right-column">

                <section class="panel-card">
                    <div class="panel-header extrato-header">
                        <h3>📋 Extrato de Lançamentos</h3>
                        <div class="filter-controls">
                            <button type="button" class="filter-btn active" data-filter="all">Todos</button>
                            <button type="button" class="filter-btn" data-filter="despesa">Despesas</button>
                            <button type="button" class="filter-btn" data-filter="receita">Receitas</button>
                        </div>
                    </div>

                    <div class="search-bar">
                        <input type="text" id="search-input" placeholder="🔍 Filtrar por descrição ou categoria...">
                        <button id="btn-reset-data" class="btn btn-sm btn-outline" title="Restaurar dados padrão para demonstração">
                            🔄 Dados Exemplo
                        </button>
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
                                <!-- Linhas inseridas dinamicamente via JS -->
                            </tbody>
                        </table>
                    </div>

                    <div id="empty-state" class="empty-state hidden">
                        <p>Nenhum lançamento encontrado para os filtros selecionados.</p>
                    </div>
                </section>

            </div>

        </div>

    </main>

    <!-- Notificações Toast do JS -->
    <div id="toast" class="toast"></div>

    <footer class="app-footer">
        <p>Projeto Acadêmico &bull; Avaliação BMVC Nível I &bull; Padrão Arquitetural Model-View-Controller</p>
    </footer>

    <!-- Carregamento do JS externo obrigatório no BMVC -->
    <script src="/static/js/despesas.js"></script>
</body>
</html>

