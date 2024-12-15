# New imports
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.responses import RedirectResponse

# Our pages
from app_home import app_home
from app_fblogin import app_fblogin
from app_aboutus import app_aboutus
from app_callback import app_callback
from app_report import app_report

async def redirect_to_home(request):
    return RedirectResponse(url="/home")

# Use Starlette to construct routes
routes = [
    Route("/", endpoint=redirect_to_home),
    Mount("/home", app_home, name="Home"),    
    Mount("/fb-login", app=app_fblogin),
    Mount("/aboutus", app=app_aboutus),
    Mount("/callback", app_callback),
    Mount("/report", app=app_report)
]

# Declare an app with Startlette
app = Starlette(routes=routes)