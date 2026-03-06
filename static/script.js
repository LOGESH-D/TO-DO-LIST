async function createTodo(){
        const title = document.getElementById("title").value
        const desc = document.getElementById("desc").value
        if(!title || !desc) return alert("All the fields are required")
        await fetch("/todos",{
            method: "POST",
            headers:{
                "Content-Type": "application/json"
            },
            body: JSON.stringify({title: title, description: desc, completed: false})
        })
        getTodos()
    }

    async function getTodos() {
        const todos = document.getElementById("todo-list")
        const response = await fetch("/todos")
        const data = await response.json()
        todos.innerHTML = ""
        data.forEach(todo => {
            const li = document.createElement("li")
            li.innerHTML = `
                Title: ${todo.title}<br><br>
                Description: ${todo.description}<br><br>
                <button onclick="editTodo('${todo._id}','${todo.title}','${todo.description}')">Edit</button><br>
                <button onclick="deleteTodo('${todo._id}')">Delete</button>
            `
            todos.appendChild(li)
        })
    }

    function editTodo(id, title, description) {
        document.getElementById("title").value = title
        document.getElementById("desc").value = description
        const button = document.querySelector("button")
        button.innerText = "Update"
        button.onclick = () => updateTodo(id)
    }

    async function updateTodo(id) {
        const title = document.getElementById("title").value
        const desc = document.getElementById("desc").value
        await fetch(`/todos/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: title,
                description: desc,
                completed: false
            })
        })
        document.querySelector("button").innerText = "Add"
        getTodos()
    }

    async function deleteTodo(id){
        await fetch(`/todos/${id}`,{ method: "DELETE"})
        getTodos()
    }
    getTodos()