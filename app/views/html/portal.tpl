<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portal de Acesso · BMVC Finance</title>
    <link rel="stylesheet" type="text/css" href="/static/css/despesas.css">
</head>
<body>

    <header class="app-header">
        <div class="header-container">
            <div class="brand">
                <div class="brand-icon">🔐</div>
                <div>
                    <h1>BMVC Finance &bull; Portal</h1>
                    <p class="subtitle">Controle de Acesso e Autenticação de Sessão (BMVC Nível 3)</p>
                </div>
            </div>
            <div class="header-actions">
                <a href="/despesas" class="btn btn-sm btn-outline">⬅️ Ir para o Painel</a>
            </div>
        </div>
    </header>

    <main class="main-container" style="max-width: 820px;">

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

        <div class="charts-grid">
            <!-- Card de Login -->
            <section class="panel-card">
                <div class="panel-header">
                    <h3>🔑 Entrar na Conta</h3>
                </div>
                <form action="/portal" method="POST" class="form-grid">
                    <div class="form-group">
                        <label for="username">Usuário</label>
                        <input id="username" name="username" type="text" placeholder="Ex: gustavo ou Henrique" required>
                    </div>

                    <div class="form-group">
                        <label for="password">Senha</label>
                        <input id="password" name="password" type="password" placeholder="••••••" required>
                    </div>

                    <button type="submit" class="btn btn-primary">
                        Entrar no Sistema
                    </button>
                </form>

                <div style="margin-top: 1.2rem; padding-top: 1rem; border-top: 1px solid #334155; font-size: 0.8rem; color: #94a3b8;">
                    <p><strong>Contas de demonstração:</strong></p>
                    <p>&bull; Usuário: <code>gustavo</code> | Senha: <code>123456</code></p>
                    <p>&bull; Usuário: <code>Henrique</code> | Senha: <code>123456</code></p>
                </div>
            </section>

            <!-- Card de Cadastro de Novo Usuário (Nível 4) -->
            <section class="panel-card">
                <div class="panel-header">
                    <h3>👤 Cadastrar Novo Usuário</h3>
                </div>
                <form action="/register" method="POST" class="form-grid">
                    <div class="form-group">
                        <label for="reg-username">Novo Usuário</label>
                        <input id="reg-username" name="username" type="text" placeholder="Escolha um nome de usuário" required>
                    </div>

                    <div class="form-group">
                        <label for="reg-password">Nova Senha</label>
                        <input id="reg-password" name="password" type="password" placeholder="Crie uma senha" required>
                    </div>

                    <button type="submit" class="btn btn-outline" style="padding: 0.75rem 1.2rem; margin-top: 0.25rem;">
                        ➕ Criar Conta
                    </button>
                </form>

                % if defined('current_user') and current_user:
                <div style="margin-top: 1.2rem; padding-top: 1rem; border-top: 1px solid #334155;">
                    <p style="font-size: 0.85rem; margin-bottom: 0.5rem;">Conectado atualmente como: <strong>{{current_user.username}}</strong></p>
                    <form action="/logout" method="POST">
                        <button type="submit" class="btn-delete" style="width: 100%; padding: 0.5rem;">
                            🚪 Realizar Logout
                        </button>
                    </form>
                </div>
                % end
            </section>
        </div>

    </main>

    <footer class="app-footer">
        <p>Projeto Acadêmico &bull; BMVC Finance &bull; Autenticação via Cookies HTTPOnly + UUID Session</p>
    </footer>

</body>
</html>

