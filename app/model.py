import os
import pickle
import cv2
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model.pkl")


def load_model():
    """Loads and returns the pretrained model."""
    model = pickle.load(open(MODEL_PATH, 'rb'))
    print("Model loaded")
    return model

def prepare_image(image):
    """Prepares the image for prediction by resizing it."""

    # Redimensionner l'image
    img = cv2.resize(image, (224, 224)) / 255.0

    # Ajouter une dimension
    img = np.expand_dims(img, axis=0)

    return img

def predict(image, model):
    """Predicts the class of the image and returns the result."""
    img = prepare_image(image)  # Utiliser la fonction prepare_image

    # Faire une prédiction avec le modèle
    prediction = model.predict(img)
    score = float(round(prediction[0][0], 3))

    # Créer un dictionnaire de réponse
    response = {
        "class": 1 if prediction[0][0] > 0.5 else 0,
        "score": score,
        "probability": score
    }
    
    print(response)
    return response
