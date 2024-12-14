from shiny import App, ui
import urllib.parse

# Facebook OAuth details
FACEBOOK_CLIENT_ID = '2087135655067065'
REDIRECT_URI = 'http://localhost:8000/callback'

# Facebook OAuth URLs
AUTHORIZATION_URL = 'https://www.facebook.com/v21.0/dialog/oauth'

# Define the UI
app_ui = ui.page_fluid(
    ui.panel_title(title="Facebook Login", window_title="Facebook Login"),
    ui.tags.script("""
        // On page load, check if there is a 'code' parameter in the URL
        document.addEventListener('DOMContentLoaded', function () {
            const urlParams = new URLSearchParams(window.location.search);
            const code = urlParams.get('code');
 
            if (code) {
                // Send the code to the server via input binding
                Shiny.setInputValue('auth_code', code);
            }
        });
    """),
    ui.h2("Facebook Login Page"),
    ui.tags.a( "Home",href="../",class_="btn btn-primary"),
    ui.tags.a(
        "Login with Facebook",
        href=f"{AUTHORIZATION_URL}?client_id={FACEBOOK_CLIENT_ID}&redirect_uri={urllib.parse.quote(REDIRECT_URI)}&scope=email,public_profile,ads_read",
        class_="btn btn-primary"
    ),
)

# Create the Shiny app
app_fblogin = App(app_ui, server=None)


