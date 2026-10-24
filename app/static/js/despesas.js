/**
 * BMVC Finance - Lógica Interativa do Frontend (Nível 1)
 * Arquivo: app/static/js/despesas.js
 */

document.addEventListener('DOMContentLoaded', () => {
    // Referências aos elementos do DOM
    const form = document.getElementById('transaction-form');
    const typeInput = document.getElementById('type');
    const descInput = document.getElementById('description');
    const amountInput = document.getElementById('amount');
    const categoryInput = document.getElementById('category');
    const dateInput = document.getElementById('date');
    const tableBody = document.getElementById('transaction-table-body');
    const emptyState = document.getElementById('empty-state');
    const searchInput = document.getElementById('search-input');
    const filterButtons = document.querySelectorAll('.filter-btn');
    const resetDataBtn = document.getElementById('btn-reset-data');

    // Cards de resumo
    const totalIncomeEl = document.getElementById('total-income');
    const totalExpenseEl = document.getElementById('total-expense');
    const currentBalanceEl = document.getElementById('current-balance');
    const categoryBarsEl = document.getElementById('category-bars');
    const toastEl = document.getElementById('toast');

    // Estado da Aplicação
    let currentFilter = 'all';
    let searchQuery = '';

    // Dados iniciais de demonstração (caso não haja no LocalStorage)
    const initialData = [
        { id: 1, type: 'receita', description: 'Salário Mensal', amount: 4500.00, category: 'Salário', date: '2026-10-05' },
        { id: 2, type: 'despesa', description: 'Aluguel do Apartamento', amount: 1500.00, category: 'Moradia', date: '2026-10-10' },
        { id: 3, type: 'despesa', description: 'Compras Supermercado', amount: 620.50, category: 'Alimentação', date: '2026-10-12' },
        { id: 4, type: 'despesa', description: 'Abastecimento Carro', amount: 250.00, category: 'Transporte', date: '2026-10-15' },
        { id: 5, type: 'despesa', description: 'Cinema e Jantar', amount: 180.00, category: 'Lazer', date: '2026-10-18' },
        { id: 6, type: 'receita', description: 'Projeto Freelance', amount: 800.00, category: 'Salário', date: '2026-10-20' },
        { id: 7, type: 'despesa', description: 'Farmácia / Remédios', amount: 95.40, category: 'Saúde', date: '2026-10-22' }
    ];

    // Carregar dados salvos ou padrão
    let transactions = JSON.parse(localStorage.getItem('bmvc_transactions')) || initialData;

    // Inicializar data de hoje no campo de formulário
    if (dateInput) {
        dateInput.value = new Date().toISOString().split('T')[0];
    }

    // Salvar no LocalStorage
    function saveTransactions() {
        localStorage.setItem('bmvc_transactions', JSON.stringify(transactions));
    }

    // Formatar moeda BRL
    function formatCurrency(value) {
        return value.toLocaleString('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        });
    }

    // Formatar data DD/MM/AAAA
    function formatDate(dateStr) {
        if (!dateStr) return '';
        const parts = dateStr.split('-');
        if (parts.length === 3) {
            return `${parts[2]}/${parts[1]}/${parts[0]}`;
        }
        return dateStr;
    }

    // Exibir Notificação Toast
    function showToast(message, isError = false) {
        toastEl.textContent = message;
        toastEl.style.backgroundColor = isError ? '#ef4444' : '#10b981';
        toastEl.classList.add('show');
        setTimeout(() => {
            toastEl.classList.remove('show');
        }, 2500);
    }

    // Atualizar Métricas e Cards
    function updateSummary() {
        let income = 0;
        let expense = 0;
        const categoryTotals = {};

        transactions.forEach(t => {
            const val = parseFloat(t.amount);
            if (t.type === 'receita') {
                income += val;
            } else {
                expense += val;
                categoryTotals[t.category] = (categoryTotals[t.category] || 0) + val;
            }
        });

        const balance = income - expense;

        totalIncomeEl.textContent = formatCurrency(income);
        totalExpenseEl.textContent = formatCurrency(expense);
        currentBalanceEl.textContent = formatCurrency(balance);

        // Cor dinâmica do saldo
        if (balance >= 0) {
            currentBalanceEl.style.color = '#10b981';
        } else {
            currentBalanceEl.style.color = '#ef4444';
        }

        // Renderizar barras de categoria
        renderCategoryBars(categoryTotals, expense);
    }

    // Renderizar gráfico de barras de categorias
    function renderCategoryBars(categoryTotals, totalExpense) {
        categoryBarsEl.innerHTML = '';

        const categories = Object.keys(categoryTotals);
        if (categories.length === 0 || totalExpense === 0) {
            categoryBarsEl.innerHTML = '<p style="color: #94a3b8; font-size: 0.85rem; font-style: italic;">Nenhuma despesa registrada.</p>';
            return;
        }

        // Ordenar da maior para a menor despesa
        categories.sort((a, b) => categoryTotals[b] - categoryTotals[a]);

        categories.forEach(cat => {
            const amount = categoryTotals[cat];
            const percent = ((amount / totalExpense) * 100).toFixed(1);

            const item = document.createElement('div');
            item.className = 'category-item';
            item.innerHTML = `
                <div class="cat-item-info">
                    <span>${cat}</span>
                    <span><strong>${formatCurrency(amount)}</strong> (${percent}%)</span>
                </div>
                <div class="cat-bar-bg">
                    <div class="cat-bar-fill" style="width: ${percent}%;"></div>
                </div>
            `;
            categoryBarsEl.appendChild(item);
        });
    }

    // Renderizar Tabela
    function renderTable() {
        tableBody.innerHTML = '';

        const filtered = transactions.filter(t => {
            const matchesType = (currentFilter === 'all') || (t.type === currentFilter);
            const matchesSearch = t.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
                                  t.category.toLowerCase().includes(searchQuery.toLowerCase());
            return matchesType && matchesSearch;
        });

        if (filtered.length === 0) {
            emptyState.classList.remove('hidden');
        } else {
            emptyState.classList.add('hidden');
        }

        filtered.forEach(t => {
            const tr = document.createElement('tr');

            const isIncome = t.type === 'receita';
            const typeBadge = isIncome
                ? '<span class="badge badge-income">Receita</span>'
                : '<span class="badge badge-expense">Despesa</span>';

            const formattedVal = (isIncome ? '+ ' : '- ') + formatCurrency(parseFloat(t.amount));
            const valColor = isIncome ? '#10b981' : '#ef4444';

            tr.innerHTML = `
                <td>${typeBadge}</td>
                <td>${formatDate(t.date)}</td>
                <td><strong>${t.description}</strong></td>
                <td><span class="badge badge-cat">${t.category}</span></td>
                <td style="color: ${valColor}; font-weight: 600;">${formattedVal}</td>
                <td>
                    <button class="btn-delete" data-id="${t.id}" title="Excluir lançamento">
                        🗑️ Excluir
                    </button>
                </td>
            `;

            tableBody.appendChild(tr);
        });

        // Adicionar eventos aos botões de exclusão
        document.querySelectorAll('.btn-delete').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const idToDelete = parseInt(e.target.closest('button').dataset.id);
                deleteTransaction(idToDelete);
            });
        });
    }

    // Excluir lançamento
    function deleteTransaction(id) {
        transactions = transactions.filter(t => t.id !== id);
        saveTransactions();
        updateSummary();
        renderTable();
        showToast('Lançamento removido com sucesso!');
    }

    // Adicionar lançamento via formulário
    form.addEventListener('submit', (e) => {
        e.preventDefault();

        const type = typeInput.value;
        const description = descInput.value.trim();
        const amount = parseFloat(amountInput.value);
        const category = categoryInput.value;
        const date = dateInput.value;

        if (!description || isNaN(amount) || amount <= 0 || !date) {
            showToast('Preencha todos os campos corretamente!', true);
            return;
        }

        const newTransaction = {
            id: Date.now(),
            type,
            description,
            amount,
            category,
            date
        };

        transactions.unshift(newTransaction);
        saveTransactions();
        updateSummary();
        renderTable();

        // Resetar formulário
        descInput.value = '';
        amountInput.value = '';
        descInput.focus();

        showToast(`Novo lançamento adicionado: ${description}`);
    });

    // Filtros por Tipo (Todos, Despesas, Receitas)
    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            filterButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentFilter = btn.dataset.filter;
            renderTable();
        });
    });

    // Busca por Texto
    searchInput.addEventListener('input', (e) => {
        searchQuery = e.target.value.trim();
        renderTable();
    });

    // Restaurar dados de exemplo
    resetDataBtn.addEventListener('click', () => {
        if (confirm('Deseja restaurar os dados de exemplo padrão?')) {
            transactions = [...initialData];
            saveTransactions();
            updateSummary();
            renderTable();
            showToast('Dados de exemplo restaurados!');
        }
    });

    // Inicialização da tela
    updateSummary();
    renderTable();
});

