class UserAccount:
    """Model representando uma Conta de Usuário para controle de sessão e acesso (BMVC Nível 3)."""

    def __init__(self, username, password, role="user"):
        self.username = str(username).strip()
        self.password = str(password).strip()
        self.role = str(role).strip()

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role
        }

