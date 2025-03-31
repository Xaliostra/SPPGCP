import boto3
import openai
import os
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

rekognition = boto3.client(
    'rekognition',
    region_name='us-east-1',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

openai.api_key = OPENAI_API_KEY

def detect_food_labels(image_bytes):
    response = rekognition.detect_labels(
        Image={'Bytes': image_bytes},
        MaxLabels=10,
        MinConfidence=70
    )
    return [label['Name'] for label in response['Labels']]

def generate_recipe(ingredients):
    prompt = f"Create a simple recipe using: {', '.join(ingredients)}."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful chef."},
                  {"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/analyze", methods=["POST"])
def analyze_image():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    image = request.files["file"].read()
    
    food_items = detect_food_labels(image)
    if not food_items:
        return jsonify({"error": "No food items detected."}), 400
    
    recipe = generate_recipe(food_items)
    return jsonify({"ingredients": food_items, "recipe": recipe})

PORT = int(os.getenv("PORT", 8080))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
