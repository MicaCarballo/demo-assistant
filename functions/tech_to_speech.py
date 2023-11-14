import json
import requests
from decouple import config

ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")

#Eleven labs
#Convert text to speech

def convert_text_to_speech(message):
#Define Data Body
#  body ={
#     "text": message,
#     "voice_settings":{
#      "similarity_boost": 0
#     }
#   }
 
  body = {
  "text": message,
  "model_id": "eleven_monolingual_v1",
  "voice_settings": {
    "stability": 0,
    "similarity_boost": 0,
    "style": 0,
    "use_speaker_boost": "true"
  }
}

  #Define Voice
  voice_rachel ="21m00Tcm4TlvDq8ikWAM"

  #constructing header and endpoints
  print("eleven labs " + ELEVEN_LABS_API_KEY + "!")

  headers = {
    "xi-api-key": ELEVEN_LABS_API_KEY,
    "Content-Type": "application/json",
    "accept": "audio/mpeg"
  }
  endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_rachel}"

  # #Send request
  # try:
  #  response = requests.post(endpoint, json=body, headers=headers)
  # except Exception as e:
  #  print(e)
  #  return
  
  # #Handle Response
  # if response.status_code == 200:
  #   return response.content
  # else:
  #   return

  try:
        response = requests.post(endpoint, json=body, headers=headers)
  except Exception as e:
        print(f"Request failed: {e}")
        return

    # Detailed Logging
  print(f"Response Status Code: {response.status_code}")
  try:
        response_json = response.json()
        print(f"Response JSON: {json.dumps(response_json, indent=2)}")
  except json.JSONDecodeError:
        print("Failed to decode JSON from response")
    
    # Logging raw response content if it's not JSON
  if response.content:
        print(f"Response Content: {response.content}")

    # Handle Response
  if response.status_code == 200:
        return response.content
  else:
        print(f"Failed to get a successful response: {response.status_code}")
        return None