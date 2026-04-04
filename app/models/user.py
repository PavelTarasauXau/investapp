from datetime import datetime, timezone
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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



    def verify_password(self, password: str) -> bool:
        if not self.password_hash:
            return False
        return pwd_context.verify(password, self.password_hash) 


    @classmethod
    def new(cls, email: str, full_name: str, password: str) -> "User":
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")

        password_hash = cls._hash_password(password)
        return cls(
            email=email,
            full_name=full_name,
            password_hash=password_hash,
            created_at=datetime.now(timezone.utc)
        )


    @staticmethod
    def _hash_password(password: str) -> str:
        return pwd_context.hash(password)

    
    def __repr__(self):
        return f"<User {self.email}>"
    
    #когда надо будет работать с репозиториями
    def change_password(self):
        pass