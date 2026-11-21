class FinancialProfile:
    """Model representando o Perfil Financeiro do titular da carteira (Orçamento e Credenciais)."""

    def __init__(self, username, password, monthly_budget=3500.0, currency="BRL"):
        self.username = str(username).strip()
        self.password = str(password).strip()
        self.monthly_budget = float(monthly_budget)
        self.currency = str(currency).strip()

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "monthly_budget": self.monthly_budget,
            "currency": self.currency
        }
