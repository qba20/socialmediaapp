from shiny import App, ui

# Define the UI
app_ui = ui.page_fluid(
    ui.panel_title(title="About us - QBA", window_title="About us - QBA"),
    ui.tags.a( "Home",href="../",class_="btn btn-primary"),
     ui.p("This is the company's about page.")
)

app_aboutus = App(app_ui, server=None)
