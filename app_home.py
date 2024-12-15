from shiny import App, ui
import urllib.parse
import app_values

# Define the UI
app_ui = ui.page_fluid(
        ui.panel_title(title="Home", window_title="Home Page"),
        ui.tags.br(),
        ui.h1("Govertment of Kuwait - Social Media Dashboard"),
        ui.tags.br(),       
        ui.p("This is the home page. Click on below button to open the links"),
        ui.tags.br(),ui.tags.br(),

        ui.row(
                ui.column(2,
                        ui.tags.a(
                                "Login with Facebook",
                                href=f"{app_values.AUTHORIZATION_URL}?client_id={app_values.FACEBOOK_CLIENT_ID}&redirect_uri={urllib.parse.quote(app_values.REDIRECT_URI)}&scope=email,public_profile,ads_read",
                                class_="btn btn-primary"
                        )
                ),
                ui.column(2,
                        ui.tags.a("About us",href="../aboutus",class_="btn btn-primary")
                )
        ),
)

app_home = App(app_ui, server=None)