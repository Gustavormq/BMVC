# BMVC Finance · Controle de Despesas Pessoais (BMVC I)

Projeto desenvolvido para a obtenção do **Nível 1 (BMVC I)** da disciplina de Orientação a Objetos / Desenvolvimento FullStack, utilizando o padrão arquitetural **BMVC (Bottle + MVC)**.

---

## 🎯 Propósito do Projeto
Aplicação web responsiva para controle financeiro pessoal. Permite gerenciar receitas e despesas, calcular automaticamente o saldo consolidado, classificar lançamentos por categorias, visualizar a distribuição percentual de gastos e filtrar histórico por tipo ou busca textual.

---

## 🏗️ Arquitetura do Projeto (Padrão MVC)

- **Rotas (`route.py`):** Configuração do servidor Bottle, roteamento da URL raiz `/` e `/despesas` e entrega de arquivos estáticos (`/static/<filepath:path>`).
- **Controller (`app/controllers/application.py`):** Controlador `Application` responsável pela lógica de renderização dos templates.
- **View (`app/views/html/despesas.tpl`):** Interface visual estruturada com cards de resumo financeiro, formulário de lançamentos e tabela de extrato.
- **Assets Estáticos (`app/static/`):**
  - `css/despesas.css`: Estilização moderna, responsiva, com tema escuro (Dark Mode).
  - `js/despesas.js`: Script frontend interativo (validação de formulário, cálculos dinâmicos de saldo e porcentagem de categorias, persistência em LocalStorage e notificações toast).

---

## 🚀 Como Executar

### Opção 1: Diretamente com Python (Local)

1. Instale o framework Bottle:
   ```bash
   pip install bottle
   ```

2. Execute o servidor na raiz do projeto:
   ```bash
   python route.py
   ```

3. Abra o navegador em:
   [http://localhost:8080](http://localhost:8080)

---

### Opção 2: Com Docker

1. Construir a imagem Docker:
   ```bash
   docker build -t bmvci .
   ```

2. Executar o contêiner:
   ```bash
   docker run -d -p 8080:8080 -v $(pwd):/app bmvci
   ```

3. Acesse em:
   [http://localhost:8080](http://localhost:8080)
