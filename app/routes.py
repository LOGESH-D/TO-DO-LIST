from fastapi import APIRouter # Import APIRouter to create a router for our API endpoints
from app.models import Todo, User
from app.database import db, todo_collection, user_collection
from app.auth import hash_password, verify_password
from bson import ObjectId # Import ObjectId to handle MongoDB's unique identifiers (id's)

router = APIRouter() # Create an instance of APIRouter to define our API routes


@router.post("/todos/{user_id}")
async def create_todo(user_id: str, todo: Todo):# It takes a Todo object as input.
    data = todo.dict() # Convert the Todo object to a dictionary .
    data["user_id"] = user_id
    result = todo_collection.insert_one(data) # Insert the data into the MongoDB collection and store the result.
    return {"id": str(result.inserted_id)}

@router.get("/todos/{user_id}")
async def get_all_todos(user_id: str):
    todos = []
    for todo in todo_collection.find({"user_id": user_id}):
        todo["_id"] = str(todo["_id"]) # Convert the MongoDB ObjectId to a string and assign it to the new "id" field of the todo item.
        todos.append(todo)
    return todos

@router.delete("/todos/{id}")
async def delete_todo(id: str):
    todo_collection.delete_one({"_id": ObjectId(id)})
    return {"message": "Todo deleted successfully"}

@router.put("/todos/{id}")
async def update_todo(id: str, todo: Todo):
    todo_collection.update_one({"_id": ObjectId(id)}, {"$set": todo.dict()}) # comes pydantic model have to convert to dict to store
    return {"message": "Todo updated"}

@router.post("/signup")
async def signup_user(user: User):
    exist = user_collection.find_one({"email": user.email})
    if exist:
        return {"Message": "User Already Esists"}
    hashed_pass = hash_password(user.password)
    user_collection.insert_one({
        "email": user.email,
        "password": hashed_pass
    })
    return {"Message": "Signed up Successfully"}

@router.post("/signin")
async def signin_user(user: User):
    exist = user_collection.find_one({
        "email": user.email
    })
    if not exist:
        return {"Message": "Invalid Email"}
    
    if not verify_password(user.password, exist["password"]):
        return {"Message": "Invalid Password"}
    
    return {"Message": "Signed in Successfully", "User_id": str(exist["_id"])}