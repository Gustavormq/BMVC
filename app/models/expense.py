from datetime import date


class Expense:
    """Model representando um lançamento financeiro (Despesa ou Receita) no padrão BMVC."""

    CATEGORIES = [
        "Alimentação",
        "Transporte",
        "Moradia",
        "Aluguel",
        "Contas",
        "Lazer",
        "Saúde",
        "Salário",
        "Outros"
    ]

    def __init__(self, id, description, amount, category, expense_date=None, expense_type="despesa"):
        self.id = int(id)
        self.description = str(description).strip()
        self.amount = float(amount)
        self.category = str(category).strip()
        self.date = str(expense_date) if expense_date else date.today().strftime("%Y-%m-%d")
        self.type = str(expense_type).strip().lower() if expense_type in ("despesa", "receita") else "despesa"

    @property
    def formatted_date(self):
        parts = self.date.split("-")
        if len(parts) == 3:
            return f"{parts[2]}/{parts[1]}/{parts[0]}"
        return self.date

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "description": self.description,
            "amount": self.amount,
            "category": self.category,
            "date": self.date
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id", 0),
            description=data.get("description", ""),
            amount=data.get("amount", 0.0),
            category=data.get("category", "Outros"),
            expense_date=data.get("date"),
            expense_type=data.get("type", "despesa")
        )

