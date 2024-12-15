# Facebook API version
FACEBOOK_API_VER = 21.0

# Facebook OAuth details
FACEBOOK_CLIENT_ID = '2087135655067065'
FACEBOOK_CLIENT_SECRET = '588767d6d1b7b6bcb6c09704c61e6fc3'
REDIRECT_URI = 'http://localhost:8000/callback'

# Facebook OAuth URLs
AUTHORIZATION_URL = f'https://www.facebook.com/v{FACEBOOK_API_VER}.0/dialog/oauth'
TOKEN_URL = f'https://graph.facebook.com/v{FACEBOOK_API_VER}.0/oauth/access_token'
USER_INFO_URL = f'https://graph.facebook.com/v{FACEBOOK_API_VER}.0/me'

# Define the file path directly
JSON_FILE_PATH = r"D:\campaign_data.json"

#To store data received from Facebook API
fbapidata = None
