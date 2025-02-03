import urllib.parse

# Facebook API version
FACEBOOK_API_VER = 21.0

# Facebook OAuth details
FACEBOOK_CLIENT_ID = "208XXXXXXXXXXXXXX065"
FACEBOOK_CLIENT_SECRET = "5887xxxxxxxxxxxxxxxxxxxx6fc3"
REDIRECT_URI = "http://localhost:8000/callback"

# Facebook OAuth URLs
AUTHORIZATION_URL = f"https://www.facebook.com/v{FACEBOOK_API_VER}/dialog/oauth"
TOKEN_URL = f"https://graph.facebook.com/v{FACEBOOK_API_VER}/oauth/access_token"
USER_INFO_URL = f"https://graph.facebook.com/v{FACEBOOK_API_VER}/me"


GOOGLE_AUTHORIZATION_URL = f"https://accounts.google.com/o/oauth2/auth"
GOOGLE_CLIENT_ID = (
    "1036xxxxxxxxxxxxxxxxxxxxxxxx82dh4.apps.googleusercontent.com"
)
GOOGLE_CLIENT_SECRET = "GOCxxxxxxxxxxxxxxxxxxXVj"
GOOGLE_DEVELOPER_TOKEN = "Y_xxxxxxxxxxxxxzw"
GOOGLE_API_SCOPE = "https://www.googleapis.com/auth/adwords"
GOOGLE_REDIRECT_URI = "http://localhost:8000/gcallback"


# Define the file path directly
JSON_FILE_PATH = r"D:\campaign_data.json"

# FACEBOOK_LOGIN_URL
FACEBOOK_LOGIN_URL = f"{AUTHORIZATION_URL}?client_id={FACEBOOK_CLIENT_ID}&redirect_uri={urllib.parse.quote(REDIRECT_URI)}&scope=email,public_profile,ads_read"


GOOGLE_LOGIN_URL = f"{GOOGLE_AUTHORIZATION_URL}?client_id={GOOGLE_CLIENT_ID}&redirect_uri={urllib.parse.quote(GOOGLE_REDIRECT_URI)}&response_type=code&scope={GOOGLE_API_SCOPE}&access_type=offline"
GOOGLE_REFRESH_TOKEN_URL = f"https://oauth2.googleapis.com/token"
GOOGLE_USER_INFO_URL = (
    f"https://googleads.googleapis.com/v13/customers:listAccessibleCustomers"
)

# To store data received from Facebook API
fbapidata = None
