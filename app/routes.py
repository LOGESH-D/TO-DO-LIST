from fastapi import APIRouter # Import APIRouter to create a router for our API endpoints
from app.database import collection 
from app.models import Todo
from bson import ObjectId # Import ObjectId to handle MongoDB's unique identifiers (id's)

router = APIRouter() # Create an instance of APIRouter to define our API routes

@router.post("/todos")
async def create_todo(todo: Todo):# It takes a Todo object as input.
    data = todo.dict() # Convert the Todo object to a dictionary .
    result = collection.insert_one(data) # Insert the data into the MongoDB collection and store the result.
    return {"id": str(result.inserted_id)}

@router.get("/todos")
async def get_all_todos():
    todos = []
    for todo in collection.find():
        todo["_id"] = str(todo["_id"]) # Convert the MongoDB ObjectId to a string and assign it to the new "id" field of the todo item.
        todos.append(todo)
    return todos

@router.delete("/todos/{id}")
async def delete_todo(id: str):
    collection.delete_one({"_id": ObjectId(id)})
    return {"message": "Todo deleted successfully"}

@router.put("/todos/{id}")
async def update_todo(id: str, todo: Todo):
    collection.update_one({"_id": ObjectId(id)}, {"$set": todo.dict()})
    return {"message": "Todo updated"}