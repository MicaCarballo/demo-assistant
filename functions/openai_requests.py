from http.client import HTTPException
import openai
from decouple import config
import requests



# Retrieve environment variables

openai.organization = config("OPEN_AI_ORG")
openai.api_key = config("OPEN_AI_KEY")
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI

#Import custom function
from functions.database import get_recent_messages
OPEN_AI_KEY= config("OPEN_AI_KEY")
SERVAPI_KEY= config("SERVAPI_KEY")

# OpenAI - Whisper
# Convert Audio to Text

def convert_audio_to_text(audio_file):
  try:
       transcript = openai.Audio.transcribe("whisper-1", audio_file)
       message_text = transcript["text"]
       return message_text
  except Exception as e:
    print(e)
    return

 
#Open AI - ChatGTP
llm = OpenAI(openai_api_key= OPEN_AI_KEY, temperature=0.9)
tools = load_tools(["serpapi", "llm-math"], llm=llm, serpapi_api_key= SERVAPI_KEY)
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# Get response to our message
# def get_chat_response(message_input):
#    messages = get_recent_messages()
#    user_message = {"role": "user", "content": message_input}
#    messages.append(user_message)
#    print(messages)

#    try:
#        response = openai.ChatCompletion.create(
#           model="gpt-3.5-turbo",
#           messages= messages
#        )
#        #print(response)
#        message_text = response["choices"][0]["message"]["content"]
#        return message_text
#    except Exception as e:
#       print(e)
#       return

# def get_chat_response(message_input):
#    messages = get_recent_messages()
#    user_message = {"role": "user", "content": message_input}
#    messages.append(user_message)

#    try:
#        response = agent.run(messages)  # Use LangChain agent instead of direct OpenAI API call
#        print(response) 
#        choices = response.get("choices", [])

#        if choices:
#            message_text = choices[0].get("content", "")
#            if message_text:
#                return message_text

#        # If no valid response is received
#        raise Exception("Invalid response format from LangChain")

#    except Exception as e:
#       print(e)
#       return
def get_chat_response(message_input):
    messages = get_recent_messages()
    user_message = {"role": "user", "content": message_input}
    messages.append(user_message)

    try:
        # response = agent.run(messages)  # Use LangChain agent instead of direct OpenAI API call
        # print(response)  
        # # Add this line to print the response
         # Modify the user's query to include the site restriction
        modified_query = f"site:webmd.com {message_input}"
        response = agent.run([{"role": "user", "content": modified_query}])

        print(response)  # Add this line to print the response


        return str(response)  # Convert response to string and return

    except Exception as e:
        print(e)
        raise Exception("Invalid response format")


# Google Maps API key
google_maps_api_key = config("GOOGLE_MAPS_API_KEY")

# Function to get user location based on IP
def get_location_from_ip(ip_address):
    response = requests.get(f"https://ipapi.co/{ip_address}/json/")
    data = response.json()

    # Print the full response for debugging
    print("IP Geolocation API Response:", data)

    # Extract latitude and longitude from the response
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    # Check if both latitude and longitude are available
    if latitude is not None and longitude is not None:
        return f"{latitude},{longitude}"
    else:
        return None


# Function to find nearby hospitals


def find_nearby_hospitals(location, radius=5000, type="hospital"):
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "key": google_maps_api_key,
        "location": location,
        "radius": radius,
        "type": type,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    print("Google Maps API Response:", data)

    if "results" in data:
        hospitals = data["results"]
        return hospitals

    return None
