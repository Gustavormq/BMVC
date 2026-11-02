# BMVC Finance · Controle de Despesas Pessoais (Bottle + MVC)

Projeto completo desenvolvido utilizando o padrão arquitetural **BMVC (Bottle + Model-View-Controller)** para gerenciamento de finanças pessoais (receitas e despesas).

---

## Propósito do Projeto
Aplicação web responsiva para controle financeiro pessoal. Permite gerenciar receitas e despesas com persistência em backend JSON (`DataRecord`), calcular automaticamente o saldo consolidado, editar e excluir lançamentos, classificar por categorias, visualizar gráficos interativos (pizza e evolução temporal), filtrar histórico por período, categoria, tipo ou busca textual e exportar os dados em CSV.

---

## Arquitetura do Projeto (Padrão MVC)

```text
bmvc_start_from_this/
├── route.py                         # Roteamento Bottle (Páginas, Ações CRUD, CSV e API JSON)
├── Dockerfile                       # Imagem Docker da aplicação
├── bmvc_setup.sh                    # Script de build e execução do container
├── docker_install.sh                # Script auxiliar de instalação do Docker
└── app/
    ├── models/
    │   └── expense.py               # Model Expense (entidade de lançamento financeiro)
    ├── controllers/
    │   ├── application.py           # Controller Application (regras de negócio e renderização)
    │   ├── datarecord.py            # Persistência de objetos Expense em banco JSON
    │   └── db/
    │       └── expenses.json        # Base de dados JSON persistente
    ├── views/
    │   └── html/
    │       ├── despesas.tpl         # View principal (painel, filtros, tabela e gráficos)
    │       ├── editar_despesa.tpl   # View de edição de lançamento
    │       └── helper.tpl           # View auxiliar do template BMVC
    └── static/
        ├── css/
        │   └── despesas.css         # Estilização responsiva Dark Mode
        └── js/
            └── despesas.js          # Interatividade frontend, filtros, Chart.js e sync REST
```

---

## Como Executar

### Opção 1: Diretamente com Python (Local)

1. Instale o framework Bottle:
   ```bash
   pip install bottle
   ```

2. Execute o servidor na raiz do projeto (`bmvc_start_from_this`):
   ```bash
   python route.py
   ```

3. Abra o navegador em:
   [http://localhost:8080](http://localhost:8080)

---

### Opção 2: Com Docker

1. Construir e executar usando o script:
   ```bash
   ./bmvc_setup.sh
   ```
   Ou manualmente:
   ```bash
   docker build -t bmetimg .
   docker run --name bmetaap -p 8080:8080 -v $(pwd):/bmeta bmetimg
   ```

2. Acesse em:
   [http://localhost:8080](http://localhost:8080)
