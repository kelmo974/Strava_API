import requests
import os
from dotenv import load_dotenv
import json
import pandas as pd

load_dotenv()

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
refresh_token = os.getenv("refresh_token")
print(client_id)


if not all([client_id, client_secret, refresh_token]):
    raise ValueError("Missing Strava API Credentials from .env file")

# Strava endpoints
token_url = "https://www.strava.com/oauth/token"
activities_url = "https://www.strava.com/api/v3/athlete/activities"

def refresh_access_token():
    """Refreshes the access token using the refresh token."""
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }

    try:
        response = requests.post(token_url, data=payload)
        response.raise_for_status()
        token_data = response.json()
        access_token = token_data["access_token"]
        return access_token
    except requests.exceptions.RequestException as e:
        print(f"Error refreshing access token: {e}")
        return None
    
def get_strava_activities(access_token, per_page=30):
    """Retrieves Strava activities."""
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"per_page": per_page}

    try:
        response = requests.get(activities_url, headers=headers, params=params)
        response.raise_for_status()
        activities = response.json()
        return activities
    except requests.exceptions.RequestException as e:
        print(f"Error getting activities: {e}")
        return None

if __name__ == "__main__":
    access_token = refresh_access_token()

    if access_token:
        activities = get_strava_activities(access_token)

        if activities:
            print("Successfully retrieved activities!")
            #print(json.dumps(activities, indent=4))  # Pretty print JSON for inspection

            for activity in activities:
                print(activity.get("name", "Unknown Activity"))

            # Now you have the activities list; proceed with your analysis.

        else:
            print("Failed to retrieve activities.")
    else:
        print("Failed to refresh access token.")