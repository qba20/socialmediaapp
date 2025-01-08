from shiny import App, ui, reactive, render
import requests
import urllib.parse
# from starlette.responses import RedirectResponse
import app_values
import app_home

# Define the UI
app_ui = ui.page_fluid(
    ui.panel_title(title="Authentication", window_title=None),
    ui.br(),
    ui.output_text('status'),
    ui.br(),
    ui.row(
        ui.column(2,
            ui.tags.a( "Go to Reports",href="../report",class_="btn btn-primary"),
        ),
        ui.column(2,
            ui.tags.a( "Home",href="../",class_="btn btn-primary"),
        ),
        ui.column(2,
            ui.tags.a("About us",href="../aboutus",class_="btn btn-primary")
        )
    ),
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
                return 'Please go to Google login page and try again.'
            return
        else:
            print('code: ' + code)

        try:
            # Exchange the authorization code for a refresh token
            token_response = requests.post(
                app_values.GOOGLE_REFRESH_TOKEN_URL,
                params={
                    "code": code,
                    "client_id": app_values.GOOGLE_CLIENT_ID,
                    "client_secret": app_values.GOOGLE_CLIENT_SECRET,
                    "redirect_uri":app_values.GOOGLE_REDIRECT_URI,
                    "grant_type":"authorization_code"
                },
            )
            token_response.raise_for_status()
            token_data = token_response.json()

            #print('token_data: ' + token_data)
            #access_token = token_data.get("access_token")
            refresh_token = token_data.get("refresh_token")
            print('token_data')
            print(token_data)

            # if not refresh_token:
            #     @render.text
            #     def output():
            #         return "Error: Could not retrieve refresh token!"
            #     @render.text
            #     def status():
            #         return 'Please go to FB login page and try again.'
            #     return


            access_token = token_data.get("access_token")

            print('access_token: ')
            print(access_token)

            
        #     # Retrieve user info
            user_info_response = requests.get(
                app_values.GOOGLE_USER_INFO_URL,
                params={"access_token": access_token},
            )
            print('user_info_response.json()')
            print('____________________________________________________')
            print('____________________________________________________')
            print(user_info_response)
            print('____________________________________________________')
            print('____________________________________________________')

            # user_info_response.raise_for_status()
            user_info = user_info_response.json()
            # print('user_info: ' + user_info)

            app_values.fbapidata = user_info

        #     # Redirect to report page once data is fetched from API
        #     # RedirectResponse(url="/report")




            # # Exchange the refresh_token for an access token
            # token_response = requests.post(
            #     app_values.GOOGLE_REFRESH_TOKEN_URL,
            #     params={
            #         "client_id": app_values.GOOGLE_CLIENT_ID,
            #         "client_secret": app_values.GOOGLE_CLIENT_SECRET,
            #         "refresh_token": refresh_token,
            #         "grant_type": "refresh_token"
            #     },
            # )
            # token_response.raise_for_status()
            # token_data = token_response.json()

            # #print('token_data: ' + token_data)
            # access_token = token_data.get("access_token")
            # #refresh_token = token_data.get("refresh_token")
            # if not access_token:
            #     @render.text
            #     def output():
            #         return "Error: Could not retrieve access_token!"
            #     @render.text
            #     def status():
            #         return 'Please go to FB login page and try again.'
            #     return

            # print('Access Token: ' + access_token)



        # #     # Retrieve user info
        #     user_info_response = requests.get(
        #         app_values.USER_INFO_URL,
        #         params={"fields": "id,name,adaccounts", "access_token": access_token},
        #     )
        #     user_info_response.raise_for_status()
        #     user_info = user_info_response.json()
        #     app_values.fbapidata = user_info

        # #     # Redirect to report page once data is fetched from API
        # #     # RedirectResponse(url="/report")

        # #     # Display user info
            @render.text
            def output():
                return f"Logged in. Access Token : {access_token}"
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
app_g_callback = App(app_ui, server)



# if __name__ == "__main__":
#     from shiny import run_app
 
#     # Run the Shiny app on localhost
#     run_app(app_home.app_home, port=8000, host="127.0.0.1")

