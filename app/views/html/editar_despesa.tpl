<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Editar Lançamento · BMVC Finance</title>
    <link rel="stylesheet" type="text/css" href="/static/css/despesas.css">
</head>
<body>

    <header class="app-header">
        <div class="header-container">
            <div class="brand">
                <div class="brand-icon">💰</div>
                <div>
                    <h1>BMVC Finance</h1>
                    <p class="subtitle">Editar Lançamento #{{expense.id}}</p>
                </div>
            </div>
            <div class="header-actions">
                <a href="/despesas" class="btn btn-sm btn-outline">⬅️ Voltar ao Painel</a>
            </div>
        </div>
    </header>

    <main class="main-container" style="max-width: 640px;">

        % if defined('err') and err:
        <div class="alert alert-error">
            ⚠️ {{err}}
        </div>
        % end

        <section class="panel-card">
            <div class="panel-header">
                <h3>✏️ Editar Lançamento</h3>
            </div>

            <form method="POST" action="/edit/{{expense.id}}" class="form-grid">
                <div class="form-group">
                    <label for="type">Tipo</label>
                    <select id="type" name="type" required>
                        <option value="despesa" {{'selected' if expense.type == 'despesa' else ''}}>Despesa (Saída)</option>
                        <option value="receita" {{'selected' if expense.type == 'receita' else ''}}>Receita (Entrada)</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="description">Descrição</label>
                    <input type="text" id="description" name="description" value="{{expense.description}}" required>
                </div>

                <div class="form-group">
                    <label for="amount">Valor (R$)</label>
                    <input type="number" id="amount" name="amount" step="0.01" min="0.01" value="{{f'{expense.amount:.2f}'}}" required>
                </div>

                <div class="form-group">
                    <label for="category">Categoria</label>
                    <select id="category" name="category" required>
                        % for c in categories:
                        <option value="{{c}}" {{'selected' if expense.category == c else ''}}>{{c}}</option>
                        % end
                    </select>
                </div>

                <div class="form-group">
                    <label for="date">Data</label>
                    <input type="date" id="date" name="date" value="{{expense.date}}" required>
                </div>

                <div class="edit-actions">
                    <button type="submit" class="btn btn-primary">
                        💾 Salvar Alterações
                    </button>
                    <a href="/despesas" class="btn btn-outline" style="padding: 0.75rem 1.2rem; text-decoration: none;">
                        Cancelar
                    </a>
                </div>
            </form>
        </section>

    </main>

    <footer class="app-footer">
        <p>Projeto Acadêmico &bull; BMVC Finance &bull; Padrão Arquitetural Model-View-Controller (Bottle)</p>
    </footer>

</body>
</html>

