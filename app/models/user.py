import hashlib
from datetime import datetime, timezone


class User:
    def __init__(
            self, 
            email: str, 
            full_name: str, 
            password_hash: str | None = None, 
            id: int | None = None, 
            created_at: datetime | None = None
        ):

        if "@" not in email:
            raise ValueError("Invalid email, '@' is missing!")
        self.email = email.lower().strip()
        
        if not full_name or not full_name.strip():
            raise ValueError("Full name cannot be empty!")
        self.full_name = full_name.strip()
        
        self.id = id
        self.password_hash = password_hash
        self.created_at = created_at or datetime.now(timezone.utc)


    @property
    def first_name(self) -> str:
        parts = self.full_name.split()
        return parts[0] if parts else ""


    @property
    def email_domain(self) -> str:
        return self.email.split('@')[-1]


    def verify_password(self, password):
        """Проверяет, совпадает ли введенный пароль с хешем"""
        if not self.password_hash:
            return False
        return self.password_hash == self._hash_password(password)


    @classmethod
    def new(cls, email: str, full_name: str, password: str) -> "User":
        password_hash = cls._hash_password(password)
        return cls(
            email=email,
            full_name=full_name,
            password_hash=password_hash,
            created_at=datetime.now(timezone.utc)
        )


    @staticmethod
    def _hash_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    
    def __repr__(self):
        return f"<User {self.email}>"
    
    #когда надо будет работать с репозиториями
    def change_password(self):
        pass