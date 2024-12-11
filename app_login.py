from shiny import App, ui, reactive, render
import requests
import urllib.parse

import shiny

import fbdatamodule

# Facebook OAuth details
#FACEBOOK_CLIENT_ID = '1620231431897488'
FACEBOOK_CLIENT_ID = '2087135655067065'

#FACEBOOK_CLIENT_SECRET = 'df9ebeb23dfb620a2e71dda8c3247fd9'
FACEBOOK_CLIENT_SECRET = '588767d6d1b7b6bcb6c09704c61e6fc3'

REDIRECT_URI = 'http://localhost:8000/login'

# Facebook OAuth URLs
AUTHORIZATION_URL = 'https://www.facebook.com/v21.0/dialog/oauth'
TOKEN_URL = 'https://graph.facebook.com/v21.0/oauth/access_token'
USER_INFO_URL = 'https://graph.facebook.com/v21.0/me'


# Define the UI
app_ui = ui.page_fluid(
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
        
        print(f'shiny.Session dir {dir(shiny.Session)}')

        print(f'session.input dir {dir(session.input)}')
        print(f'session.output dir {dir(session.output)}')

        #param_value = session.param.get("code", "No 'param' found")
        #print(f'param_value: {param_value}')

        code = (session.input['.clientdata_url_search']())
        code = code.replace('?code=','')
        """Handle the Facebook OAuth code sent from the client."""
        #code = input.auth_code()

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
            #print(access_token)
            if not access_token:
                #print("Error: Could not retrieve access token!")
                #output["output"].set_value("Error: Could not retrieve access token!")
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
            #print(user_info)
            fbdatamodule.fbapidata = user_info
            
            # Display user info
            #output["output"].set_value(f"Logged in as: {user_info}")
            @render.text
            def output():
                return f"Logged in as: {user_info}"
            @render.text
            def status():
                return 'Login succeeded! Please go to Reports page.'
        except requests.exceptions.RequestException as e:
            #print(e)
            #output["output"].set_value(f"An error occurred: {str(e)}")
            @render.text
            def output():
                return f"An error occurred: {str(e.strerror)}"
            @render.text
            def status():
                return 'Error Occurred!'
 

# Create the Shiny app
app_login = App(app_ui, server)



'''
if __name__ == "__main__":
    from shiny import run_app
 
    # Run the Shiny app on localhost
    run_app(app_fblogin, port=8000, host="127.0.0.1")
'''