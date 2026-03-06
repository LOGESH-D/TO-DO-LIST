from pydantic import BaseModel # BaseModel is a class from the Pydantic library that provides data validation and settings management using Python type annotations.

class Todo(BaseModel): # Define a Pydantic model called Todo that inherits from BaseModel.
    title: str
    description: str
    completed: bool = False

class User(BaseModel):
    email: str
    password: str