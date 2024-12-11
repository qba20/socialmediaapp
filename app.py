# New imports
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.responses import RedirectResponse


# Our pages
from app_home import app_home
from app_fblogin import app_fblogin
from app_aboutus import app_aboutus
from app_login import app_login
from app_report import app_report


# Make App instance from your pages
#page_charts = app_fblogin
#page_about = app_aboutus

async def redirect_to_home(request):
    return RedirectResponse(url="/home")

# Use Starlette to construct routes
routes = [
    Route("/", endpoint=redirect_to_home),
    Mount("/home", app_home, name="Home"),    
    Mount("/fb-login", app=app_fblogin),
    Mount("/aboutus", app=app_aboutus),
    Mount("/login", app_login),
    Mount("/report", app=app_report)
]

# Declare an app with Startlette
app = Starlette(routes=routes)