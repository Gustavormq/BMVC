/**
 * BMVC Finance - Lógica Interativa Integrada ao Backend Bottle MVC
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

    // Filtros adicionais (migrados do Expense-Tracker)
    const filterStartInput = document.getElementById('filter-start');
    const filterEndInput = document.getElementById('filter-end');
    const filterCategoryInput = document.getElementById('filter-category');
    const clearFiltersBtn = document.getElementById('btn-clear-filters');

    // Cards de resumo
    const totalIncomeEl = document.getElementById('total-income');
    const totalExpenseEl = document.getElementById('total-expense');
    const currentBalanceEl = document.getElementById('current-balance');
    const categoryBarsEl = document.getElementById('category-bars');
    const toastEl = document.getElementById('toast');

    // Instâncias de Gráficos (Chart.js)
    let categoryChartInstance = null;
    let dayChartInstance = null;

    // Estado da Aplicação
    let currentFilter = 'all';
    let searchQuery = '';
    let startDateFilter = filterStartInput ? filterStartInput.value : '';
    let endDateFilter = filterEndInput ? filterEndInput.value : '';
    let categoryFilter = filterCategoryInput ? filterCategoryInput.value : '';

    // Dados iniciais de fallback
    const initialData = [
        { id: 1, type: 'receita', description: 'Salário Mensal', amount: 4500.00, category: 'Salário', date: '2026-10-05' },
        { id: 2, type: 'despesa', description: 'Aluguel do Apartamento', amount: 1500.00, category: 'Moradia', date: '2026-10-10' },
        { id: 3, type: 'despesa', description: 'Compras Supermercado', amount: 620.50, category: 'Alimentação', date: '2026-10-12' },
        { id: 4, type: 'despesa', description: 'Abastecimento Carro', amount: 250.00, category: 'Transporte', date: '2026-10-15' },
        { id: 5, type: 'despesa', description: 'Cinema e Jantar', amount: 180.00, category: 'Lazer', date: '2026-10-18' },
        { id: 6, type: 'receita', description: 'Projeto Freelance', amount: 800.00, category: 'Salário', date: '2026-10-20' },
        { id: 7, type: 'despesa', description: 'Farmácia / Remédios', amount: 95.40, category: 'Saúde', date: '2026-10-22' },
        { id: 8, type: 'despesa', description: 'Mercado', amount: 250.00, category: 'Alimentação', date: '2026-08-17' },
        { id: 9, type: 'despesa', description: 'Carro', amount: 320.00, category: 'Transporte', date: '2026-08-15' }
    ];

    let transactions = Array.isArray(window.INITIAL_TRANSACTIONS)
        ? window.INITIAL_TRANSACTIONS
        : (JSON.parse(localStorage.getItem('bmvc_transactions')) || initialData);

    if (dateInput && !dateInput.value) {
        dateInput.value = new Date().toISOString().split('T')[0];
    }

    function saveTransactions() {
        localStorage.setItem('bmvc_transactions', JSON.stringify(transactions));
    }

    function formatCurrency(value) {
        return Number(value).toLocaleString('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        });
    }

    function formatDate(dateStr) {
        if (!dateStr) return '';
        const parts = dateStr.split('-');
        if (parts.length === 3) {
            return `${parts[2]}/${parts[1]}/${parts[0]}`;
        }
        return dateStr;
    }

    function showToast(message, isError = false) {
        if (!toastEl) return;
        toastEl.textContent = message;
        toastEl.style.backgroundColor = isError ? '#ef4444' : '#10b981';
        toastEl.classList.add('show');
        setTimeout(() => {
            toastEl.classList.remove('show');
        }, 2500);
    }

    function getFilteredTransactions() {
        return transactions.filter(t => {
            const matchesType = (currentFilter === 'all') || (t.type === currentFilter);
            const matchesCategory = !categoryFilter || (t.category === categoryFilter);
            const matchesStart = !startDateFilter || (t.date >= startDateFilter);
            const matchesEnd = !endDateFilter || (t.date <= endDateFilter);
            const matchesSearch = !searchQuery ||
                t.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
                t.category.toLowerCase().includes(searchQuery.toLowerCase());
            return matchesType && matchesCategory && matchesStart && matchesEnd && matchesSearch;
        });
    }

    function updateSummaryAndCharts() {
        const filtered = getFilteredTransactions();
        let income = 0;
        let expense = 0;
        const categoryTotals = {};
        const dayTotals = {};

        filtered.forEach(t => {
            const val = parseFloat(t.amount);
            if (t.type === 'receita') {
                income += val;
            } else {
                expense += val;
                categoryTotals[t.category] = (categoryTotals[t.category] || 0) + val;
                dayTotals[t.date] = (dayTotals[t.date] || 0) + val;
            }
        });

        const balance = income - expense;

        if (totalIncomeEl) totalIncomeEl.textContent = formatCurrency(income);
        if (totalExpenseEl) totalExpenseEl.textContent = formatCurrency(expense);
        if (currentBalanceEl) {
            currentBalanceEl.textContent = formatCurrency(balance);
            currentBalanceEl.style.color = balance >= 0 ? '#10b981' : '#ef4444';
        }

        renderCategoryBars(categoryTotals, expense);
        renderCharts(categoryTotals, dayTotals);
    }

    function renderCategoryBars(categoryTotals, totalExpense) {
        if (!categoryBarsEl) return;
        categoryBarsEl.innerHTML = '';

        const categories = Object.keys(categoryTotals);
        if (categories.length === 0 || totalExpense === 0) {
            categoryBarsEl.innerHTML = '<p style="color: #94a3b8; font-size: 0.85rem; font-style: italic;">Nenhuma despesa registrada no filtro atual.</p>';
            return;
        }

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

    function renderCharts(categoryTotals, dayTotals) {
        if (typeof Chart === 'undefined') return;

        const catCanvas = document.getElementById('catChart');
        if (catCanvas) {
            if (categoryChartInstance) categoryChartInstance.destroy();
            const labels = Object.keys(categoryTotals);
            const values = Object.values(categoryTotals);

            categoryChartInstance = new Chart(catCanvas, {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        data: values,
                        backgroundColor: [
                            '#38bdf8', '#f87171', '#fbbf24', '#34d399',
                            '#a78bfa', '#f472b6', '#60a5fa', '#fb923c'
                        ],
                        borderColor: '#1e293b',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: { color: '#cbd5e1' }
                        },
                        tooltip: {
                            callbacks: {
                                label: (ctx) => `${ctx.label}: ${formatCurrency(ctx.raw)}`
                            }
                        }
                    }
                }
            });
        }

        const dayCanvas = document.getElementById('dayChart');
        if (dayCanvas) {
            if (dayChartInstance) dayChartInstance.destroy();
            const sortedDays = Object.keys(dayTotals).sort();
            const dayValues = sortedDays.map(d => dayTotals[d]);

            dayChartInstance = new Chart(dayCanvas, {
                type: 'line',
                data: {
                    labels: sortedDays.map(formatDate),
                    datasets: [{
                        label: 'Despesas (R$)',
                        data: dayValues,
                        borderColor: '#38bdf8',
                        backgroundColor: 'rgba(56, 189, 248, 0.2)',
                        tension: 0.3,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            labels: { color: '#cbd5e1' }
                        },
                        tooltip: {
                            callbacks: {
                                label: (ctx) => formatCurrency(ctx.raw)
                            }
                        }
                    },
                    scales: {
                        x: { ticks: { color: '#94a3b8' } },
                        y: {
                            beginAtZero: true,
                            ticks: {
                                color: '#94a3b8',
                                callback: (v) => 'R$ ' + v
                            }
                        }
                    }
                }
            });
        }
    }

    function renderTable() {
        if (!tableBody) return;
        tableBody.innerHTML = '';

        const filtered = getFilteredTransactions();

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
                    <div class="action-buttons">
                        <a href="/edit/${t.id}" class="btn-edit" title="Editar lançamento">
                            ✏️ Editar
                        </a>
                        <button type="button" class="btn-delete" data-id="${t.id}" title="Excluir lançamento">
                            🗑️ Excluir
                        </button>
                    </div>
                </td>
            `;

            tableBody.appendChild(tr);
        });

        document.querySelectorAll('.btn-delete').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const idToDelete = parseInt(e.target.closest('button').dataset.id);
                deleteTransaction(idToDelete);
            });
        });
    }

    async function deleteTransaction(id) {
        try {
            const res = await fetch(`/api/transactions/${id}`, { method: 'DELETE' });
            if (res.ok) {
                transactions = transactions.filter(t => t.id !== id);
                saveTransactions();
                updateSummaryAndCharts();
                renderTable();
                showToast('Lançamento removido com sucesso!');
                return;
            }
        } catch (_) {
            // Fallback offline
        }
        transactions = transactions.filter(t => t.id !== id);
        saveTransactions();
        updateSummaryAndCharts();
        renderTable();
        showToast('Lançamento removido com sucesso!');
    }

    if (form) {
        form.addEventListener('submit', async (e) => {
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

            try {
                const res = await fetch('/api/transactions', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ type, description, amount, category, date })
                });
                if (res.ok) {
                    const created = await res.json();
                    transactions.unshift(created);
                } else {
                    transactions.unshift({ id: Date.now(), type, description, amount, category, date });
                }
            } catch (_) {
                transactions.unshift({ id: Date.now(), type, description, amount, category, date });
            }

            saveTransactions();
            updateSummaryAndCharts();
            renderTable();

            descInput.value = '';
            amountInput.value = '';
            descInput.focus();

            showToast(`Novo lançamento adicionado: ${description}`);
        });
    }

    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            filterButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentFilter = btn.dataset.filter;
            updateSummaryAndCharts();
            renderTable();
        });
    });

    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            searchQuery = e.target.value.trim();
            updateSummaryAndCharts();
            renderTable();
        });
    }

    if (filterStartInput) {
        filterStartInput.addEventListener('change', (e) => {
            startDateFilter = e.target.value;
            updateSummaryAndCharts();
            renderTable();
        });
    }

    if (filterEndInput) {
        filterEndInput.addEventListener('change', (e) => {
            endDateFilter = e.target.value;
            updateSummaryAndCharts();
            renderTable();
        });
    }

    if (filterCategoryInput) {
        filterCategoryInput.addEventListener('change', (e) => {
            categoryFilter = e.target.value;
            updateSummaryAndCharts();
            renderTable();
        });
    }

    if (clearFiltersBtn) {
        clearFiltersBtn.addEventListener('click', () => {
            startDateFilter = '';
            endDateFilter = '';
            categoryFilter = '';
            searchQuery = '';
            currentFilter = 'all';
            if (filterStartInput) filterStartInput.value = '';
            if (filterEndInput) filterEndInput.value = '';
            if (filterCategoryInput) filterCategoryInput.value = '';
            if (searchInput) searchInput.value = '';
            filterButtons.forEach(b => b.classList.toggle('active', b.dataset.filter === 'all'));
            updateSummaryAndCharts();
            renderTable();
        });
    }

    if (resetDataBtn) {
        resetDataBtn.addEventListener('click', async () => {
            if (confirm('Deseja restaurar os dados de exemplo padrão?')) {
                try {
                    const res = await fetch('/api/reset', { method: 'POST' });
                    if (res.ok) {
                        transactions = await res.json();
                    } else {
                        transactions = [...initialData];
                    }
                } catch (_) {
                    transactions = [...initialData];
                }
                saveTransactions();
                updateSummaryAndCharts();
                renderTable();
                showToast('Dados de exemplo restaurados!');
            }
        });
    }

    // Sincronizar com a API do Backend ao abrir a página
    async function syncFromServer() {
        try {
            const res = await fetch('/api/transactions');
            if (res.ok) {
                transactions = await res.json();
                saveTransactions();
                updateSummaryAndCharts();
                renderTable();
            }
        } catch (_) {
            // Usa dados locais
        }
    }

    updateSummaryAndCharts();
    renderTable();
    syncFromServer();
});
