async function createTodo(){
    const title = document.getElementById("title").value
    const desc = document.getElementById("desc").value
    if(!title || !desc) return alert("All the fields are required")
    const user_id = localStorage.getItem("user_id")
    if(!user_id) return alert("Please login first")
    
    try {
        const response = await fetch(`/todos/${user_id}`,{
            method: "POST",
            headers:{
                "Content-Type": "application/json"
            },
            body: JSON.stringify({title: title, description: desc, completed: false})
        })
        if(response.ok) {
            document.getElementById("title").value = ""
            document.getElementById("desc").value = ""
            getTodos()
        } else {
            alert("Failed to create todo")
        }
    } catch(error) {
        alert("Error: " + error.message)
    }
}

async function getTodos() {
    const todos = document.getElementById("todo-list")
    const user_id = localStorage.getItem("user_id")
    if(!user_id) return
    
    try {
        const response = await fetch(`/todos/${user_id}`)
        if(!response.ok) alert("Failed to fetch todos")
        const data = await response.json()
        todos.innerHTML = ""
        if(Array.isArray(data)) {
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
    } catch(error) {
        console.error("Error fetching todos:", error)
    }
}

function editTodo(id, title, description) {
    document.getElementById("title").value = title
    document.getElementById("desc").value = description
    const button = document.getElementById("submit-btn")
    button.innerText = "Update"
    button.onclick = () => updateTodo(id)
}

async function updateTodo(id) {
    const title = document.getElementById("title").value
    const desc = document.getElementById("desc").value
    
    try {
        const response = await fetch(`/todos/${id}`, {
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
        if(response.ok) {
            document.getElementById("title").value = ""
            document.getElementById("desc").value = ""
            const button = document.getElementById("submit-btn")
            button.innerText = "Add"
            button.onclick = () => createTodo()
            getTodos()
        } else {
            alert("Failed to update todo")
        }
    } catch(error) {
        alert("Error: " + error.message)
    }
}

async function deleteTodo(id){
    try {
        const response = await fetch(`/todos/${id}`,{ method: "DELETE"})
        if(response.ok) {
            getTodos()
        } else {
            alert("Failed to delete todo")
        }
    } catch(error) {
        alert("Error: " + error.message)
    }
}

async function signUp(){
    const email = document.getElementById("email").value
    const pass = document.getElementById("password").value
    
    if(!email || !pass) {
        return alert("Email and password are required")
    }
    if(!email.includes("@gmail.com")) {
        return alert("Please use a valid Gmail address (must contain @gmail.com)")
    }
    try {
        const res = await fetch("/signup", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({email: email, password: pass})
        })
        
        const data = await res.json()
        
        if(data.Message && data.Message.includes("Already")) {
            alert(data.Message)
        } else if(data.Message && data.Message.includes("Successfully")) {
            alert("Account Created Successfully")
            window.location.href = "/login"
        } else {
            alert("Signup failed. Please try again.")
        }
    } catch(error) {
        alert("Error: " + error.message)
    }
}

async function login(){
    const email = document.getElementById("email").value
    const pass = document.getElementById("password").value
    
    if(!email || !pass) {
        return alert("Email and password are required")
    }
    if(!email.includes("@gmail.com")) {
        return alert("Please use a valid Gmail address (must contain @gmail.com)")
    }
    try {
        const res = await fetch("/signin", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({email: email, password: pass})
        })

        const data = await res.json()

        if(data.User_id){
            localStorage.setItem("user_id", data.User_id)
            alert("Logged in Successfully")
            window.location.href = "/"
        }
        else{
            alert(data.Message || "Login Failed")
        }
    } catch(error) {
        alert("Error: " + error.message)
    }
}


async function logout(){
    localStorage.removeItem("user_id")
    window.location.href = "/login"
}

if(window.location.pathname === "/"){
    const user = localStorage.getItem("user_id")
    if(!user) window.location.href = "/login"
    else getTodos()
}