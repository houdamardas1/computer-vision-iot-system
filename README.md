# Computer Vision & IoT System: automatic bottle sorting

Academic team project (HESTIM, April 2024): a camera takes a picture of each bottle, a deep learning model detects whether it has a visual defect, and the result is used to sort the bottles automatically.

This repository contains the **image classification service** at the heart of the system: a MobileNet based model served through a REST API with FastAPI, packaged with Docker and covered by automated tests.

## Features

- **Bottle classification** with a convolutional neural network (MobileNet transfer learning, binary output)
- **REST API**: upload a photo to `POST /predict` and get the predicted class and its confidence score as JSON
- **Image preprocessing with OpenCV**: decoding, resizing to 224×224 and normalisation
- **Input validation**: non-image files and unreadable images are rejected with a clear `400` error
- **Docker image** for deployment on a server or an edge device
- **Automated tests** with pytest and FastAPI's `TestClient`

## Tech stack

Python · TensorFlow / Keras · OpenCV · NumPy · FastAPI · Uvicorn · Docker · pytest

The full team prototype also used YOLO, a Raspberry Pi with a camera, and MongoDB to store detection data. Those hardware and integration parts are not included in this repository.

## Architecture

```
 Camera / client
        │  image (JPEG/PNG)
        ▼
 ┌───────────────────────────────┐
 │ FastAPI  ·  POST /predict     │  app/main.py
 │  - checks the content type    │
 │  - decodes the image (OpenCV) │
 └──────────────┬────────────────┘
                ▼
 ┌───────────────────────────────┐
 │ Preprocessing + inference     │  app/model.py
 │  - resize 224×224, /255       │
 │  - MobileNet → Flatten →      │
 │    Dense(1, sigmoid)          │
 └──────────────┬────────────────┘
                ▼
   JSON { class, score, probability }
                │
                ▼
     Sorting step (IoT prototype)
```

### Model

| Layer | Output shape | Parameters |
|---|---|---|
| MobileNet 1.0 (224, pretrained backbone) | 7 × 7 × 1024 | 3.2 M |
| Flatten | 50 176 | 0 |
| Dense (sigmoid) | 1 | 50 k |

The trained model is shipped as `app/model.pkl` (about 40 MB). A score above `0.5` returns class `1`, otherwise class `0`.

## Project structure

```
.
├── app/
│   ├── main.py        # FastAPI application and /predict endpoint
│   ├── model.py       # model loading, preprocessing and prediction
│   └── model.pkl      # trained Keras model
├── tests/
│   ├── files/         # sample bottle photos and a text file for negative tests
│   ├── conftest.py
│   └── test_predict.py
├── Dockerfile
└── requirements.txt
```

## Getting started

### Run locally

Requires Python 3.10 to 3.12.

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cd app
python main.py                  # API on http://localhost:5000
```

Interactive API docs are available at `http://localhost:5000/docs`.

### Run with Docker

```bash
docker build -t bottle-classifier .
docker run -p 5000:5000 bottle-classifier
```

### Try it

```bash
curl -X POST http://localhost:5000/predict \
  -F "file=@tests/files/IMG_9585.jpeg;type=image/jpeg"
```

```json
{
  "filename": "IMG_9585.jpeg",
  "content_type": "image/jpeg",
  "predictions": { "class": 1, "score": 1.0, "probability": 1.0 }
}
```

### Run the tests

From the repository root:

```bash
pytest
```

## Status

Academic prototype built as a team at HESTIM, with full hardware and software integration on the physical prototype.
