from pydantic import BaseModel

class Employee(BaseModel):
    id: int
    name: str
    salary: int
    department: str = None

class User(BaseModel):
    username: str
    password: str