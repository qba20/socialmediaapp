from shiny import App, ui
import urllib.parse
import app_values

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
        href=f"{app_values.AUTHORIZATION_URL}?client_id={app_values.FACEBOOK_CLIENT_ID}&redirect_uri={urllib.parse.quote(app_values.REDIRECT_URI)}&scope=email,public_profile,ads_read",
        class_="btn btn-primary"
    ),
)

# Create the Shiny app
app_fblogin = App(app_ui, server=None)


