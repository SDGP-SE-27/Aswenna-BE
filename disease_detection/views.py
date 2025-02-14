from django.shortcuts import render
from fastapi import FastAPI, UploadFile, File, Form
from django.core.files.storage import default_storage
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os

app = FastAPI()

def preprocess_image(image: Image.Image):
    image = image.resize((224, 224))  # Resize to model input size
    image_array = np.array(image) / 255.0  # Normalize
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
    return image_array

@app.post("/api/predict/banana")
async def predict_banana(file: UploadFile = File(...)):
    model = tf.keras.models.load_model("models/banana_model.h5")
    disease_classes = ['Healthy', 'Panama Disease', 'Pestalotiopsis', 'Sigatoka Disease']

    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))
    processed_image = preprocess_image(image)

    predictions = model.predict(processed_image)
    confidence = float(np.max(predictions))

    if confidence < 0.5:
        return {"disease": "Unknown", "confidence": confidence, "message": "Disease not identified. Connect with an instructor."}

    predicted_class = disease_classes[np.argmax(predictions)]
    return {"disease": predicted_class, "confidence": confidence}

@app.post("/api/predict/mango")
async def predict_mango(file: UploadFile = File(...)):
    model = tf.keras.models.load_model("models/mango_model.h5")
    disease_classes = ['Anthracnose', 'Bacterial Canker', 'Cutting Weevil', 'Die Back', 'Gall Midge', 'Healthy', 'Powdery Mildew', 'Sooty Mould']

    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))
    processed_image = preprocess_image(image)

    predictions = model.predict(processed_image)
    confidence = float(np.max(predictions))

    if confidence < 0.5:
        return {"disease": "Unknown", "confidence": confidence, "message": "Disease not identified. Connect with an instructor."}

    predicted_class = disease_classes[np.argmax(predictions)]
    return {"disease": predicted_class, "confidence": confidence}

@app.post("/api/predict/papaya")
async def predict_papaya(file: UploadFile = File(...)):
    model = tf.keras.models.load_model("models/papaya_model.h5")
    disease_classes = ['Anthracnose', 'Bacterial Spot', 'Curl', 'Healthy', 'Mealybug', 'Mite Disease', 'Mosaic', 'Ringspot']

    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))
    processed_image = preprocess_image(image)

    predictions = model.predict(processed_image)
    confidence = float(np.max(predictions))

    if confidence < 0.5:
        return {"disease": "Unknown", "confidence": confidence, "message": "Disease not identified. Connect with an instructor."}

    predicted_class = disease_classes[np.argmax(predictions)]
    return {"disease": predicted_class, "confidence": confidence}

@app.post("/api/predict/snake_gourd")
async def predict_snake_gourd(file: UploadFile = File(...)):
    model = tf.keras.models.load_model("models/snake_gourd_model.h5")
    disease_classes = ['Healthy', 'Anthracnose', 'Yellow Leaf Disease']

    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))
    processed_image = preprocess_image(image)

    predictions = model.predict(processed_image)
    confidence = float(np.max(predictions))

    if confidence < 0.5:
        return {"disease": "Unknown", "confidence": confidence, "message": "Disease not identified. Connect with an instructor."}

    predicted_class = disease_classes[np.argmax(predictions)]
    return {"disease": predicted_class, "confidence": confidence}

@app.post("/api/predict/eggplant")
async def predict_eggplant(file: UploadFile = File(...)):
    model = tf.keras.models.load_model("models/eggplant_model.h5")
    disease_classes = ['Aphids', 'Cercospora Leaf Spot', 'Defect Eggplant', 'Flea Beetles', 'Fresh Eggplant', 'Fresh Eggplant Leaf', 'Leaf Wilt', 'Phytophthora Blight', 'Powdery Mildew', 'Tobacco Mosaic Virus', 'Yellow Disease']

    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))
    processed_image = preprocess_image(image)

    predictions = model.predict(processed_image)
    confidence = float(np.max(predictions))

    if confidence < 0.5:
        return {"disease": "Unknown", "confidence": confidence, "message": "Disease not identified. Connect with an instructor."}

    predicted_class = disease_classes[np.argmax(predictions)]
    return {"disease": predicted_class, "confidence": confidence}

@app.post("/api/predict/okra")
async def predict_okra(file: UploadFile = File(...)):
    model = tf.keras.models.load_model("models/okra_model.h5")
    disease_classes = ['Downy Mildew', 'Healthy', 'Leaf Curly Virus']

    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))
    processed_image = preprocess_image(image)

    predictions = model.predict(processed_image)
    confidence = float(np.max(predictions))

    if confidence < 0.5:
        return {"disease": "Unknown", "confidence": confidence, "message": "Disease not identified. Connect with an instructor."}

    predicted_class = disease_classes[np.argmax(predictions)]
    return {"disease": predicted_class, "confidence": confidence}

# Create your views here.

def home(request):
    return render(request, 'home.html')
