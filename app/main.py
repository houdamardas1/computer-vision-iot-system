from pydantic import BaseModel
from io import BytesIO
from typing import List
import cv2
import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile
from model import load_model, predict
import numpy as np

app = FastAPI()

model = load_model()

# Define the response JSON
class Prediction(BaseModel):
    filename: str
    content_type: str
    predictions: dict

@app.post("/predict", response_model=Prediction)
async def prediction(file: UploadFile = File(...)):
    # Assurez-vous que le fichier est une image
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    content = await file.read()
    img_array = np.frombuffer(content, np.uint8)  # Convertir le contenu en tableau NumPy
    image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # Charger l'image avec OpenCV

    # Vérifier si l'image a été chargée correctement
    if image is None:
        raise HTTPException(status_code=400, detail="L'image n'a pas pu être chargée.")

    # Prédire à partir de l'image
    response = predict(image, model)

    # Retourner la réponse sous forme de JSON
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "predictions": response,
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000)
