import openai
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
import config  # Import your API key from the config module

app = Flask(__name__)
CORS(app)

# Set the OpenAI API key
openai.api_key = config.OPENAI_API_KEY

# The chatbot's identity as The Business Hero
chatbot_identity = "The Business Hero"
team_identity = "The Business Hero Team"

def get_chatgpt_response(prompt, max_tokens=500):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.4,
        max_tokens=max_tokens,
    )
    return response.choices[0].text.strip()

# Function to display chatbot responses with delays
def display_response_with_delay(response, delay=2):
    print(f"{chatbot_identity}: {response}")
    time.sleep(delay)

def generate_business_guide(user_business):
    prompt = f"{chatbot_identity}, Please provide a step-by-step guide for starting a {user_business}."
    guide = get_chatgpt_response(prompt, max_tokens=500)
    return guide

# Flask Route to get chatbot response
@app.route('/get_response', methods=['POST'])
def get_chatbot_response():
    user_message = request.json.get('user_message')
    chatbot_response = get_chatgpt_response(user_message)
    return jsonify({"response": chatbot_response})

# Introduction of the chatbot
print(f"{chatbot_identity}: Hello! I am an AI chatbot created by {team_identity}. "
      "I can provide step-by-step guides for starting a business. "
      "Do you have an existing business? (Please answer with 'yes' or 'no')")

while True:
    user_response = input("You: ").lower()

    if user_response == 'exit':
        break

    if user_response == 'yes':
        print(f"{chatbot_identity}: How can I assist you with your existing business?")
        user_question = input("You: ")

        while user_question.lower() != 'exit':
            prompt = f"{user_question}"
            response = get_chatgpt_response(prompt, max_tokens=200)
            display_response_with_delay(response, delay=3)
            user_question = input("You: ")

    elif user_response == 'no':
        print(f"{chatbot_identity}: What business would you like to start?")
        user_business = input("You: ")

        guide = generate_business_guide(user_business)
        display_response_with_delay(guide, delay=5)

        print(f"{chatbot_identity}: Do you have any specific questions about the steps mentioned in the guide?")
        user_question = input("You: ")

        while user_question.lower() != 'exit':
            if "step" in user_question.lower():
                step_number = user_question.split()[-1]
                prompt = f"{guide}, How do I perform step {step_number}?"
            else:
                prompt = f"{user_question}"

            response = get_chatgpt_response(prompt, max_tokens=200)
            display_response_with_delay(response, delay=3)
            user_question = input("You: ")

    else:
        prompt = f"{user_response}"
        response = get_chatgpt_response(prompt, max_tokens=200)
        display_response_with_delay(response, delay=3)

print(f"{chatbot_identity}: Thank you for using The Business Hero! If you have any more questions or need further assistance, "
      "feel free to come back anytime. Good luck with your business!")

if __name__ == '__main__':
    app.run(debug=True)
