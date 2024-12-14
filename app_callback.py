from shiny import App, ui, reactive, render
import requests
import urllib.parse
from starlette.responses import RedirectResponse


import fbdatamodule

# Facebook OAuth details
FACEBOOK_CLIENT_ID = '2087135655067065'

FACEBOOK_CLIENT_SECRET = '588767d6d1b7b6bcb6c09704c61e6fc3'

REDIRECT_URI = 'http://localhost:8000/callback'

# Facebook OAuth URLs
AUTHORIZATION_URL = 'https://www.facebook.com/v21.0/dialog/oauth'
TOKEN_URL = 'https://graph.facebook.com/v21.0/oauth/access_token'
USER_INFO_URL = 'https://graph.facebook.com/v21.0/me'

# Define the UI
app_ui = ui.page_fluid(
    ui.panel_title(title="Authentication", window_title=None),
    ui.br(),ui.br(),
    ui.output_text('status'),
    ui.br(),ui.br(),
    ui.tags.a( "Go to Reports",href="../report",class_="btn btn-primary"),
    ui.tags.a( "Home",href="../",class_="btn btn-primary"),
    ui.br(),ui.br(),
    ui.output_text_verbatim("output",placeholder=True)
)


# Server logic
def server(input, output, session):
    @reactive.Effect
    def handle_auth_code():
        
        @render.text
        def status():
            return 'Authenticating.'

        #Read query string code from URL
        query_string = session.input['.clientdata_url_search']()
        code = urllib.parse.parse_qs(query_string)['?code'][0]

        if not code:
            @render.text
            def output():
                return "Authorization code not received."
            @render.text
            def status():
                return 'Please go to FB login page and try again.'
            return
        
        try:
            # Exchange the authorization code for an access token
            token_response = requests.get(
                TOKEN_URL,
                params={
                    "client_id": FACEBOOK_CLIENT_ID,
                    "redirect_uri": REDIRECT_URI,
                    "client_secret": FACEBOOK_CLIENT_SECRET,
                    "code": code,
                },
            )
            token_response.raise_for_status()
            token_data = token_response.json()
 
            access_token = token_data.get("access_token")
            if not access_token:
                @render.text
                def output():
                    return "Error: Could not retrieve access token!"
                @render.text
                def status():
                    return 'Please go to FB login page and try again.'
                return
 
            # Retrieve user info
            user_info_response = requests.get(
                USER_INFO_URL,
                params={"fields": "id,name,adaccounts", "access_token": access_token},
            )
            user_info_response.raise_for_status()
            user_info = user_info_response.json()
            fbdatamodule.fbapidata = user_info

            # Redirect to report page once data is fetched from API
            # RedirectResponse(url="/report")

            # Display user info
            @render.text
            def output():
                return f"Logged in as: {user_info}"
            @render.text
            def status():
                return 'Login succeeded! Please go to Reports page.'
        except requests.exceptions.RequestException as e:
            @render.text
            def output():
                return f"An error occurred: {str(e.strerror)}"
            @render.text
            def status():
                return 'Error Occurred!'
 
# Create the Shiny app
app_callback = App(app_ui, server)


'''
if __name__ == "__main__":
    from shiny import run_app
 
    # Run the Shiny app on localhost
    run_app(app_fblogin, port=8000, host="127.0.0.1")
'''
