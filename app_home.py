from shiny import App, ui

# Define the UI
app_ui = ui.page_fluid(
        ui.h4("Home Page"),
        ui.tags.br(),
        ui.h1("Govertment of Kuwait - Social Media Dashboard"),
        ui.tags.br(),       
        ui.p("This is the home page. Click on below button to open the links"),
        ui.tags.br(),ui.tags.br(),
        ui.tags.a( "Login with Facebook",href="../fb-login",class_="btn btn-primary"),
        ui.tags.br(),ui.tags.br(),ui.tags.br(),
        ui.tags.a( "About us",href="../aboutus",class_="btn btn-primary")
)

app_home = App(app_ui, server=None)