from shiny import App, ui
import urllib.parse
import app_values


# Define the UI
app_ui = ui.page_fluid(
        ui.panel_title(title="Govertment of Kuwait - Social Media Dashboard", window_title="Home Page"),
        ui.tags.br(),       
        ui.p("This is the home page. Click on below button to open the links"),
        ui.tags.br(),
        ui.row(
                ui.column(2,
                        ui.tags.a(
                                "Login with Facebook",
                                href=app_values.FACEBOOK_LOGIN_URL,
                                class_="btn btn-primary"
                        )
                ),
                ui.column(2,
                        ui.tags.a(
                                "Login with Google",
                                href=app_values.GOOGLE_LOGIN_URL,
                                class_="btn btn-primary"
                        )
                ),
                ui.column(2,
                        ui.tags.a("About us",href="../aboutus",class_="btn btn-primary")
                )
        )
)

app_home = App(app_ui, server=None)