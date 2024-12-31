import urllib.parse

# Facebook API version
FACEBOOK_API_VER = 21.0

# Facebook OAuth details
FACEBOOK_CLIENT_ID = '2087135655067065'
FACEBOOK_CLIENT_SECRET = '588767d6d1b7b6bcb6c09704c61e6fc3'
REDIRECT_URI = 'http://localhost:8000/callback'

# Facebook OAuth URLs
AUTHORIZATION_URL = f'https://www.facebook.com/v{FACEBOOK_API_VER}/dialog/oauth'
TOKEN_URL = f'https://graph.facebook.com/v{FACEBOOK_API_VER}/oauth/access_token'
USER_INFO_URL = f'https://graph.facebook.com/v{FACEBOOK_API_VER}/me'


GOOGLE_AUTHORIZATION_URL = f'https://accounts.google.com/o/oauth2/auth'
GOOGLE_CLIENT_ID = '1036207747478-o2qdrm7lco3eg54novr5u8ri71i82dh4.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET= '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'
GOOGLE_DEVELOPER_TOKEN = 'Y_H8ik_J_cwcxmibrT_Yzw'
GOOGLE_API_SCOPE='https://www.googleapis.com/auth/adwords'
GOOGLE_REDIRECT_URI='http://localhost:8000/gcallback'


# Define the file path directly
JSON_FILE_PATH = r"D:\campaign_data.json"

#FACEBOOK_LOGIN_URL
FACEBOOK_LOGIN_URL=f"{AUTHORIZATION_URL}?client_id={FACEBOOK_CLIENT_ID}&redirect_uri={urllib.parse.quote(REDIRECT_URI)}&scope=email,public_profile,ads_read"


GOOGLE_LOGIN_URL = f'{GOOGLE_AUTHORIZATION_URL}?client_id={GOOGLE_CLIENT_ID}&redirect_uri={urllib.parse.quote(GOOGLE_REDIRECT_URI)}&response_type=code&scope={GOOGLE_API_SCOPE}&access_type=offline'


#To store data received from Facebook API
fbapidata = None
