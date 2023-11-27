# uvicorn main:app
# uvicorn main:app --reload

# main imports
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai

# Custom functions imports
from functions.openai_requests import convert_audio_to_text, find_nearby_hospitals, get_chat_response, get_location_from_ip
from functions.database import store_messages, reset_messages
from functions.tech_to_speech import convert_text_to_speech
# Initiate app
app = FastAPI()

#Cors origin
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:3000",
    "http://localhost:8000"
];
#Cors- Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]


)

# Check Health
@app.get("/health")
async def check_health():
    
    return {"message": "Hello World healthy"}


# Reset messages
@app.get("/reset")
async def reset_conversation():
    reset_messages()
    
    return {"message": "conversation reset"}

#Get audio
#@app.get("/post-audio-get/")
@app.post("/post-audio")

#async def get_audio():
async def post_audio(file:UploadFile = File(...)):
   
   #Get saved audio
   #audio_input = open("voice.mp3", "rb")

   #Save file from Frontend
   with open(file.filename, "wb") as buffer:
       buffer.write(file.file.read())
   audio_input = open(file.filename, "rb")
   #Decode Audio
   message_decoded = convert_audio_to_text(audio_input)

   #Guard ensure message decoded
   if not message_decoded:
       return HTTPException(status_code=400, detail="Failed to decode Audio")
   
   #Get ChatGTP response
   chat_response = get_chat_response(message_decoded)

   #Guard ensure message decoded
   if not chat_response:
       return HTTPException(status_code=400, detail="Failed to get chat response")
   

    #Store Messages
   store_messages(message_decoded, chat_response)

   #Convert chat response to audio
   audio_output = convert_text_to_speech(chat_response)

   #Guard ensure message decoded
   if not audio_output:
       return HTTPException(status_code=400, detail="Failed to get ElevenLabs response")
   
  #Create a generator that yields chunks of data

   def iterfile():
       yield audio_output

   # Return audio file

   return StreamingResponse(iterfile(), media_type ="application/octet-stream")   


  

# FastAPI route to handle the user's request for nearby hospitals
# FastAPI route to handle the user's request for nearby hospitals
@app.get("/nearest-hospitals")
async def get_nearest_hospitals(request: Request):
    try:
        # Use IP-based location
        user_ip = request.client.host
        user_location = get_location_from_ip(user_ip)

       # Print user_location for debugging
        print("User Location:", user_location)


        # Check if user_location is valid
        if not user_location:
            return {"error": "Invalid user location."}

        # Call the function to find nearby hospitals
        hospitals = find_nearby_hospitals(user_location)

        if hospitals:
            # Format the response
            hospital_names = [hospital["name"] for hospital in hospitals]
            response_message = f"Here are some nearby hospitals: {', '.join(hospital_names)}"
        else:
            response_message = "No hospitals found nearby."

        return {"message": response_message}

    except Exception as e:
        print(e)
        return {"error": "Failed to retrieve nearby hospitals."}

# Your existing code...



  
