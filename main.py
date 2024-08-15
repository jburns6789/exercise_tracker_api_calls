import requests
from datetime import datetime, time
import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv('APP_ID')
APP_KEY = os.getenv('APP_KEY')

SHEETS_KEY_JOEL = os.getenv('SHEETS_KEY_JOEL')
SHEETS_KEY_PYTHON_100_DAYS = os.getenv('SHEETS_KEY_PYTHON')

user_exercise = input("Tell me what you did")

GENDER = os.getenv('GENDER')
WEIGHT = os.getenv('WEIGHT')
HEIGHT = os.getenv('HEIGHT')
AGE = os.getenv('AGE')

current_date = datetime.now()
current_time = current_date.strftime("%H:%M:%S")
formatted_date = current_date.strftime("%Y-%m-%d")

sheet_endpoint = os.getenv('SHEET_ENDPOINT')

url = "https://trackapi.nutritionix.com"
natural_language_nutrients = "/v2/natural/exercise"

headers = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY,
    "Content-Type": "application/json"
}

params = {
    "query": user_exercise,
    "gender": GENDER,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE
}

request_url = f"{url}{natural_language_nutrients}"
exercise_response = requests.post(request_url, headers=headers, json=params)
result = exercise_response.json()

headers = {
    "Authorization": f"Bearer {SHEETS_KEY_JOEL}",
    "Content-Type": "application/json"
 }

for exercise in result["exercises"]:
    sheet_inputs = {
        "sheet1": {
            "date": formatted_date,
            "time": current_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }
    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs, headers=headers)
    print(sheet_response.text)

print(exercise_response.text)

