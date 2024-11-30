from flask import Flask, render_template, request, send_file, redirect, url_for
import cv2 
import numpy as np
import os
from tensorflow.keras.utils import load_img
from tensorflow.keras.utils import img_to_array
from keras.models import load_model
import csv
import pandas as pd
import openai
import time

# Set the OpenAI API key
openai.api_key = "API key here "

# Define the name of the bot
name = 'MAIZE_ASSISTANT'

# Define the role of the bot
role = 'You are a helpful and kind AI Assistant, specialized in maize diseases and health. Feel free to ask me anything about Northern Leaf Blight, Cercospora Gray Leaf Spot, Common Rust, and general maize health.'

# Define the impersonated role with instructions
impersonated_role = f"""
    From now on, you are going to act as {name}. Your role is {role}.
    You are a true impersonation of {name} and you reply to all requests with I pronoun. You never give unknown information.
    Forward them to the website for more information.
    YOU ARE NOT AN AI MODEL!
"""

# Initialize variables for chat history
explicit_input = ""
chatgpt_output = 'Chat log: /n'
cwd = os.getcwd()
i = 1

# Find an available chat history file
while os.path.exists(os.path.join(cwd, f'chat_history{i}.txt')):
    i += 1

history_file = os.path.join(cwd, f'chat_history{i}.txt')

# Create a new chat history file
with open(history_file, 'w') as f:
    f.write('\n')

# Initialize chat history
chat_history = ''

# Create a Flask web application
app = Flask(__name__)

# Function to complete chat input using OpenAI's GPT-3.5 Turbo
def chatcompletion(user_input, impersonated_role, explicit_input, chat_history):
    output = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        temperature=1,
        presence_penalty=0,
        frequency_penalty=0,
        max_tokens=2000,
        messages=[
            {"role": "system", "content": f"{impersonated_role}. Conversation history: {chat_history}"},
            {"role": "user", "content": f"{user_input}. {explicit_input}"},
        ]
    )

    for item in output['choices']:
        chatgpt_output = item['message']['content']

    return chatgpt_output

# Function to handle user chat input
def chat(user_input):
    global chat_history, name, chatgpt_output
    current_day = time.strftime("%d/%m", time.localtime())
    current_time = time.strftime("%H:%M:%S", time.localtime())
    chat_history += f'\nUser: {user_input}\n'
    chatgpt_raw_output = chatcompletion(user_input, impersonated_role, explicit_input, chat_history).replace(f'{name}:', '')
    chatgpt_output = f'{name}: {chatgpt_raw_output}'
    chat_history += chatgpt_output + '\n'
    with open(history_file, 'a') as f:
        f.write('\n'+ current_day+ ' '+ current_time+ ' User: ' +user_input +' \n' + current_day+ ' ' + current_time+  ' ' +  chatgpt_output + '\n')
        f.close()
    return chatgpt_raw_output

# Function to get a response from the chatbot
def get_response(userText):
    return chat(userText)

# Load model
model = load_model("model/maize.h5")
print('@@ Model loaded')

v_username, v_password = 'admin', 'admin'

def detect_maize_leaf(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define bounds
    lower_green = np.array([40,50,50])
    upper_green = np.array([80,255,255])

    # Threshold
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Perform morphology
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Find contours
    contours, hierachy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate
    for contour in contours:
        # Calculate area
        area = cv2.contourArea(contour)

        # Set range
        if 580 < area < 55000:
            return True
    
    return False

def pred_cot_dieas(cott_plant):
    test_image = load_img(cott_plant, target_size=(150, 150))
    print("@@ Got Image for prediction")
   
    test_image = img_to_array(test_image)/255
    test_image = np.expand_dims(test_image, axis=0)
   
    result = model.predict(test_image).round(3)
    print('@@ Raw result = ', result)
   
    pred = np.argmax(result)
 
    if pred == 0:
        update_csv("Gray Leaf Spot")
        return "Cercospora leaf spot / Gray leaf spot", 'Cercospora_leaf_spot Gray_leaf_spot.html'
    elif pred == 1:
        update_csv("Common Rust")
        return 'Common Rust', 'Common_rust_.html'
    elif pred == 2:
        update_csv("Northern Leaf Blight")
        return 'Northern Leaf Blight', 'Northern_Leaf_Blight.html'
    elif pred == 3:
        update_csv("Healthy Maize")
        return 'Healthy', 'healthy.html'
    else:
        return "Healthy", 'healthy.html'

# Create Flask instance
app = Flask(__name__)

# render indexx.html page
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('indexx.html')

@app.route("/indexx")
def indexx():
    return render_template('indexx.html')

@app.route("/login", methods=['GET','POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username == v_username and password == v_password:
        return redirect(url_for('indexdash'))
    else:
        return redirect(url_for('indexx'))

# render indexdash.html page
@app.route("/indexdash.html")
def indexdash():
    return render_template('indexdash.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

# get input image from client then predict class and render respective .html page for solution
@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['image']
        filename = file.filename        
        print("@@ Input posted = ", filename)
         
        file_path = os.path.join('static/user uploaded', filename)
        file.save(file_path)

        test = detect_maize_leaf(file_path)

        if test:
            print("@@ Predicting class......")
            pred, output_page = pred_cot_dieas(cott_plant=file_path)
        else:
            return render_template('not_identified.html', user_image=file_path)

        return render_template(output_page, pred_output=pred, user_image=file_path)

# serve the CSV file
@app.route('/data')
def get_data():
    csv_file = r"static/Count.csv"
    return send_file(csv_file, mimetype='text/csv', as_attachment=True)

def update_csv(column_name):
    file_path = r"static/Count.csv"
    df = pd.read_csv(file_path)
    old_value = df.at[0,column_name]
    new_value = old_value + 1
    df.at[0, column_name] = new_value
    df.to_csv(file_path, index=False)

# Define app routes
@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

@app.route("/get")
# Function for the bot response
def get_bot_response():
    userText = request.args.get('msg')
    return str(get_response(userText))

@app.route('/refresh')
def refresh():
    time.sleep(600) # Wait for 10 minutes
    return redirect('/refresh')


# For local system & cloud
if __name__ == "__main__":
    app.run(debug=True, threaded=False, host='0.0.0.0', port=801)