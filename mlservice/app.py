from fastapi import FastAPI, Query
import random

app = FastAPI()


@app.get("/")
def root():
    return {"message": "ML service running ✅"}


@app.get("/chatbot")
def chatbot(query: str = Query(...)):
    categories = ["Python", "Web Development", "Data Science"]
    category = random.choice(categories)

    response = f"Our TensorFlow model thinks this query is about {category}!"
    confidence = round(random.uniform(0.6, 0.95), 2)

    return {
        "category": category,
        "confidence": confidence,
        "response": response
    }
