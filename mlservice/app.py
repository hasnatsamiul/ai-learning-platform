from fastapi import FastAPI, Query
import tensorflow as tf
import numpy as np

app = FastAPI()

categories = ["Python", "Data Science", "Web Development"]
model = tf.keras.models.load_model("text_model_saved")

@app.get("/")
def root():
    return {"message": "ML service running", "model": "TF BiLSTM + TextVectorization"}

@app.get("/chatbot")
def chatbot(query: str = Query(..., min_length=1, max_length=500)):
    probs = model.predict(np.array([query]), verbose=0)[0]
    idx = int(np.argmax(probs))
    confidence = float(probs[idx])

    return {
        "category": categories[idx],
        "confidence": round(confidence, 2),
        "response": f"The TensorFlow model predicts this query is about {categories[idx]}."
    }
