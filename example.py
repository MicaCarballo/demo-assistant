import json
import random

# Load the healthcare data
def load_healthcare_data():
    try:
        with open("healthcare_data.json") as file:
            return json.load(file)
    except Exception as e:
        print(e)
        return []

healthcare_data = load_healthcare_data()

# Get a random healthcare message pair
def get_random_healthcare_message():
    return random.choice(healthcare_data);


# (Omitted for brevity)

# You might modify get_recent_messages to sometimes use get_random_healthcare_message
def get_recent_messages():
    # ... (your existing code here)
    
    # Add a random element from healthcare_data
    x = random.uniform(0, 1)
    if x > 0.8:  # Adjust this threshold as you like
        random_message_pair = get_random_healthcare_message()
        messages.append({"role": "user", "content": random_message_pair["user"]})
        messages.append({"role": "assistant", "content": random_message_pair["assistant"]})
    
    # ... (your existing code here)
    
    return messages

# Your existing code...
# (Omitted for brevity)
