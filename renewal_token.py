import requests

def token_renewal(token_profile):
    APP_ID = "591300100157004"
    APP_SECRET = "c4c4f44a4dec6fec2cf4c810e3c261cc"
    SHORT_LIVED_TOKEN = token_profile

    url = f"https://graph.facebook.com/v18.0/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": APP_ID,
        "client_secret": APP_SECRET,
        "fb_exchange_token": SHORT_LIVED_TOKEN
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "access_token" in data:
        print("Long-Lived Token:", data["access_token"])
        return data["access_token"]
    else:
        print("Error:", data)
        return False
    
token_profile = "EAAIZAyMhs7kwBO3tk6DoiyyeNbVv7e9u0aIPZA1w66khoS0TZBZCHrvZCW8dsYZA7PZCuchAZBhZC5L6e7yzXRBgxKBrsh9vgNQdrdI2pbcRWcmob3g2cN7F2yHFXHgkLoqXnqcC3TzLBZAzSOkwwZBlRYZBZAGw02a6YUmWeMTWwfy33NtvyIP1d3CbOem0EgqRClZBq19dbyTiOZAr4Uvtb9y68AXhxtBRuKwoWd2QgZDZD"
token_renewal(token_profile)