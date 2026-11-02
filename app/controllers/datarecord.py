import json
import os
from datetime import datetime
from app.models.expense import Expense

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DB_FILE = os.path.join(BASE_DIR, 'app', 'controllers', 'db', 'expenses.json')


class DataRecord:
    """Banco de dados JSON para o recurso de Despesas/Lançamentos (Padrão BMVC)."""

    DEFAULT_RECORDS = [
        {"id": 1, "type": "receita", "description": "Salário Mensal", "amount": 4500.00, "category": "Salário", "date": "2026-10-05"},
        {"id": 2, "type": "despesa", "description": "Aluguel do Apartamento", "amount": 1500.00, "category": "Moradia", "date": "2026-10-10"},
        {"id": 3, "type": "despesa", "description": "Compras Supermercado", "amount": 620.50, "category": "Alimentação", "date": "2026-10-12"},
        {"id": 4, "type": "despesa", "description": "Abastecimento Carro", "amount": 250.00, "category": "Transporte", "date": "2026-10-15"},
        {"id": 5, "type": "despesa", "description": "Cinema e Jantar", "amount": 180.00, "category": "Lazer", "date": "2026-10-18"},
        {"id": 6, "type": "receita", "description": "Projeto Freelance", "amount": 800.00, "category": "Salário", "date": "2026-10-20"},
        {"id": 7, "type": "despesa", "description": "Farmácia / Remédios", "amount": 95.40, "category": "Saúde", "date": "2026-10-22"},
        {"id": 8, "type": "despesa", "description": "Mercado", "amount": 250.00, "category": "Alimentação", "date": "2026-08-17"},
        {"id": 9, "type": "despesa", "description": "Carro", "amount": 320.00, "category": "Transporte", "date": "2026-08-15"}
    ]

    def __init__(self):
        self.__expenses = []
        self.read()

    def read(self):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                self.__expenses = [Expense.from_dict(item) for item in raw_data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.reset()

    def write(self):
        os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(
                [exp.to_dict() for exp in self.__expenses],
                f,
                ensure_ascii=False,
                indent=4
            )

    def reset(self):
        self.__expenses = [Expense.from_dict(item) for item in self.DEFAULT_RECORDS]
        self.write()
        return self.get_all()

    def get_all(self):
        return sorted(self.__expenses, key=lambda x: (x.date, x.id), reverse=True)

    def get_by_id(self, expense_id):
        expense_id = int(expense_id)
        for exp in self.__expenses:
            if exp.id == expense_id:
                return exp
        return None

    def filter_expenses(self, start="", end="", category="", expense_type="", search=""):
        results = self.get_all()

        if start:
            try:
                datetime.strptime(start, "%Y-%m-%d")
                results = [e for e in results if e.date >= start]
            except ValueError:
                pass

        if end:
            try:
                datetime.strptime(end, "%Y-%m-%d")
                results = [e for e in results if e.date <= end]
            except ValueError:
                pass

        if category:
            results = [e for e in results if e.category == category]

        if expense_type and expense_type != "all":
            results = [e for e in results if e.type == expense_type]

        if search:
            q = search.lower()
            results = [
                e for e in results
                if q in e.description.lower() or q in e.category.lower()
            ]

        return results

    def book(self, description, amount, category, expense_date, expense_type="despesa"):
        next_id = max((e.id for e in self.__expenses), default=0) + 1
        new_expense = Expense(
            id=next_id,
            description=description,
            amount=amount,
            category=category,
            expense_date=expense_date,
            expense_type=expense_type
        )
        self.__expenses.append(new_expense)
        self.write()
        return new_expense

    def update(self, expense_id, description, amount, category, expense_date, expense_type=None):
        exp = self.get_by_id(expense_id)
        if not exp:
            return None
        exp.description = str(description).strip()
        exp.amount = float(amount)
        exp.category = str(category).strip()
        exp.date = str(expense_date).strip()
        if expense_type in ("despesa", "receita"):
            exp.type = expense_type
        self.write()
        return exp

    def remove(self, expense_id):
        exp = self.get_by_id(expense_id)
        if not exp:
            return False
        self.__expenses = [e for e in self.__expenses if e.id != int(expense_id)]
        self.write()
        return True

