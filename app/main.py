from fastapi import FastAPI
from app.routes import router
from fastapi.responses import HTMLResponse # response type used to return HTML pages
from fastapi.templating import Jinja2Templates # class used to load and render HTML files
from fastapi import Request # Request represents the HTTP request coming from the browser. eg: GET / . It contains information like: URL, headers, cookies, client info
from fastapi.staticfiles import StaticFiles

app = FastAPI() # Create a FastAPI instance or Creates the main application object.

app.include_router(router) # Include the router from the routes module to handle API endpoints
app.mount("/static", StaticFiles(directory="static"), name="static") # Mount the static files directory to serve CSS, JavaScript, and images. The URL path /static will be used to access these files.
run = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse) # Define a route for the root URL ("/") that returns an HTML response. The response_class=HTMLResponse parameter specifies that the response will be of type HTML.
def home(request: Request): # The Request object contains information about the incoming HTTP request, such as headers, query parameters, and client information.
    return run.TemplateResponse( # TemplateResponse loads and sends the HTML file.
        "index.html",
        {"request": request} # This sends the request object to the template. Jinja templates require request.
)