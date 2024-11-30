# Maize Disease Detection and Assistance Application

This project is a **Flask-based web application** designed to assist users in identifying maize diseases, providing solutions, and offering an AI powered chatbot for maize-related queries. It uses a pre-trained deep learning model to classify diseases and integrates a chatbot powered by OpenAI GPT-3.5 Turbo for additional support.

---

## Features

- **Maize Disease Detection**: Upload an image of maize leaves to identify diseases such as:
  - Northern Leaf Blight
  - Cercospora Gray Leaf Spot
  - Common Rust
  - Healthy maize
  
- **Interactive Chatbot**: Engage with the **MAIZE_ASSISTANT**, a specialized chatbot for maize-related questions.

- **Data Insights**: View a downloadable CSV file tracking the count of detected diseases.

- **Admin Dashboard**: Login-protected area to access additional resources and insights.

---
Some screenshots of the application in action:

Dashboard 
![dash](https://github.com/user-attachments/assets/5fd7cdc4-9da4-48d3-9135-0055289081ee)

Classification 
![classification](https://github.com/user-attachments/assets/709e71a1-83d7-49f1-a665-27286a45f532)

Chatbot Interface
![chatbot](https://github.com/user-attachments/assets/1fe48f09-3fca-4152-98c5-6490a613b695)

Error page
![error](https://github.com/user-attachments/assets/c2e2adc2-1f1e-4f77-b528-f492897600a1)

---
## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, Bootstrap
- **Machine Learning**: TensorFlow/Keras-based deep learning model
- **Database**: CSV for tracking disease counts
- **API Integration**: OpenAI GPT for chatbot functionality

---

## Prerequisites

Ensure you have the following installed on your system:

- **Python 3.7+**
- **pip** (Python package manager)
- **OpenCV**
- **TensorFlow**
- **Flask**
- **Pandas**
- **Keras**
- **OpenAI Python library**

---

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-repo/maize-assistant.git
   cd maize-assistant
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set OpenAI API Key**
   - In the Python code (`app.py`), locate the line:
     ```python
     openai.api_key = "API key here"
     ```
   - Replace `"API key here"` with your OpenAI API key.

4. **Prepare the Model**
   - Place your pre-trained Keras model (`maize.h5`) in the `model/` directory.

5. **Prepare Static Assets**
   - Ensure the `static/user uploaded/` directory exists for user uploads.
   - Place the `Count.csv` file in the `static/` directory with initial disease count data.

6. **Run the Application**
   ```bash
   python app.py
   ```

7. **Access the Application**
   - Open a web browser and navigate to: `http://127.0.0.1:801`

---

## Cross-Platform Deployment

This application is designed to run on **Windows**, **MacOS**, and **Linux**. Follow these additional steps for cross-platform deployment:

### Docker Deployment
1. Create a `Dockerfile`:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY . /app
   RUN pip install --no-cache-dir -r requirements.txt
   CMD ["python", "app.py"]
   ```

2. Build and run the Docker container:
   ```bash
   docker build -t maize-assistant .
   docker run -p 801:801 maize-assistant
   ```

3. Access the app at `http://localhost:801`.

### Cloud Deployment
- Deploy to platforms like **AWS**, **Azure**, **Google Cloud**, or **Heroku** by:
  - Packaging the app in a zip file or Docker container.
  - Configuring environment variables for the OpenAI API key and deployment settings.

---

## File Structure

```plaintext
maize-assistant/
│
├── app.py                  # Main application logic
├── model/
│   └── maize.h5            # Pre-trained Keras model
├── templates/
│   ├── indexx.html         # Home page
│   ├── chatbot.html        # Chatbot interface
│   └── [other templates]
├── static/
│   ├── user uploaded/      # Directory for user-uploaded images
│   ├── Count.csv           # CSV file tracking disease count
│   └── [assets, CSS, JS]
├── requirements.txt        # Python dependencies
└── README.md               # Documentation
```

---

## Notes

1. For production, consider setting `debug=False` in `app.py`.
2. Use environment variables to securely store sensitive keys like the OpenAI API key.
3. Regularly update the `Count.csv` file and back it up for data tracking.

---

## License

This project is licensed under the MIT License. Feel free to modify and use it as needed.

---

This **`README.md`** provides a comprehensive guide for your project and cross-platform deployment. Let me know if you'd like further refinements!
