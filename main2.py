#import packages
import requests
import pandas as pd
from pandas import json_normalize
import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

# Setup Strava connection
auth_url = "https://www.strava.com/oauth/token"
activities_url = "https://www.strava.com/api/v3/athlete/activities"

payload = {
    'client_id': os.getenv('customer_id'),
    'client_secret': os.getenv('customer_secret'),
    'refresh_token': os.getenv('refresh_token'),
    'grant_type': 'refresh_token',
    'f': 'json'
}

res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']

header = {'Authorization': 'Bearer ' + access_token}
param = {'per_page': 200, 'page': 1}
my_dataset = requests.get(activities_url, headers=header, params=param).json()

#convert to dataframe
activities = json_normalize(my_dataset)