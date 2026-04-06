from pydantic import BaseModel, EmailStr, field_validator, computed_field

class UserCreate(BaseModel):
    email: EmailStr  
    full_name: str
    password: str

    @field_validator("full_name")
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Full name cannot be empty")
        return v.strip()

    @field_validator("password")
    def password_min_length(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str

    @computed_field
    def first_name(self) -> str:
        return self.full_name.split()[0]

    model_config = {"from_attributes": True}