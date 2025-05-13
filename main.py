import os
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.efficientnet import preprocess_input

# Load the saved model
model = load_model('food_classification_model.keras')

# Function to preprocess images
def preprocess_image(image_path, target_size=(224, 224)):
    img = Image.open(image_path).convert('RGB')
    img_resized = img.resize(target_size)
    img_array = img_to_array(img_resized)  # Convert PIL image to numpy array
    img_array = preprocess_input(img_array)  # Preprocess the input for EfficientNet
    return np.expand_dims(img_array, axis=0)

# Predict function
def predict_class(image_path, class_names):
    preprocessed_image = preprocess_image(image_path)
    predictions = model.predict(preprocessed_image)
    predicted_class_index = np.argmax(predictions)
    predicted_class = class_names[predicted_class_index]
    confidence = predictions[0][predicted_class_index] * 100
    return predicted_class, confidence

# Path to the "Unknown" folder containing images to classify
unknown_folder = 'assets/Unknown/'

# Classify images in the "Unknown" folder
for image_file in os.listdir(unknown_folder):
    if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(unknown_folder, image_file)
        predicted_class, confidence = predict_class(image_path, class_names)
        print(f"Image: {image_file}, Predicted Class: {predicted_class}, Confidence: {confidence:.2f}%")
