import hashlib
from datetime import datetime, timezone


class User:
    def __init__(self, email, full_name, password_hash=None, id=None, created_at=None):

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
    def first_name(self):
        return self.full_name.split()[0] if self.full_name else ""


    @property
    def email_domain(self):
        return self.email.split('@')[-1]


    def verify_password(self, password):
        """Проверяет, совпадает ли введенный пароль с хешем"""
        if not self.password_hash:
            return False
        return self.password_hash == self._hash_password(password)


    @classmethod
    def new(cls, email, full_name, password):
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
    
"""
//тест
    if __name__ == "__main__":
        # Создаем пользователя
        user = User.new("ivan@mail.ru", "Иван Петров", "mypass123")
        
        # Проверяем свойства
        print(user)
        print(f"First name: {user.first_name}")
        print(f"Email domain: {user.email_domain}")
        print(f"Password hash: {user.password_hash}")
        print(f"Password verify: {user.verify_password('mypass123')}")  # True
        print(f"Password verify: {user.verify_password('wrong')}")     # False
"""