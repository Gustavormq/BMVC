import json
import os
import uuid
from datetime import datetime
from app.models.expense import Expense
from app.models.financial_profile import FinancialProfile

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DB_FILE = os.path.join(BASE_DIR, 'app', 'controllers', 'db', 'expenses.json')
PROFILES_DB_FILE = os.path.join(BASE_DIR, 'app', 'controllers', 'db', 'financial_profiles.json')


class DataRecord:
    """Gerenciador de persistência em JSON para os modelos Expense e FinancialProfile (Padrão BMVC)."""

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
        self.__profiles = []
        self.__authenticated_users = {}
        self.read()
        self.read_profiles()

    # -------------------------------------------------------------------------
    # Gerenciamento de Perfis Financeiros e Sessões
    # -------------------------------------------------------------------------
    def read_profiles(self):
        try:
            with open(PROFILES_DB_FILE, "r", encoding="utf-8") as f:
                raw_profiles = json.load(f)
                self.__profiles = [FinancialProfile(**data) for data in raw_profiles]
        except (FileNotFoundError, json.JSONDecodeError):
            self.__profiles = [
                FinancialProfile("gustavo", "123456", 3500.0, "BRL"),
                FinancialProfile("admin", "123456", 5000.0, "BRL")
            ]
            self.write_profiles()

    def write_profiles(self):
        os.makedirs(os.path.dirname(PROFILES_DB_FILE), exist_ok=True)
        with open(PROFILES_DB_FILE, "w", encoding="utf-8") as f:
            json.dump(
                [p.to_dict() for p in self.__profiles],
                f,
                ensure_ascii=False,
                indent=4
            )

    def book_user(self, username, password, monthly_budget=3500.0):
        for p in self.__profiles:
            if p.username.lower() == username.strip().lower():
                return None
        new_profile = FinancialProfile(username, password, monthly_budget)
        self.__profiles.append(new_profile)
        self.write_profiles()
        return new_profile

    def getCurrentUser(self, session_id):
        if session_id in self.__authenticated_users:
            return self.__authenticated_users[session_id]
        return None

    def getUserName(self, session_id):
        if session_id in self.__authenticated_users:
            return self.__authenticated_users[session_id].username
        return None

    def getUserSessionId(self, username):
        for session_id, user in self.__authenticated_users.items():
            if username == user.username:
                return session_id
        return None

    def checkUser(self, username, password):
        for profile in self.__profiles:
            if profile.username == username and profile.password == password:
                session_id = str(uuid.uuid4())
                self.__authenticated_users[session_id] = profile
                return session_id
        return None

    def logout(self, session_id):
        if session_id in self.__authenticated_users:
            del self.__authenticated_users[session_id]

    def work_with_parameter(self, parameter):
        try:
            index = int(parameter)
            if 0 <= index < len(self.__expenses):
                return self.__expenses[index]
        except (ValueError, IndexError):
            return None
        return None

    # -------------------------------------------------------------------------
    # CRUD Completo do Modelo Expense (Lançamentos Financeiros)
    # -------------------------------------------------------------------------
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
