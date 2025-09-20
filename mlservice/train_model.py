import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, GlobalAveragePooling1D, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pickle

# === Training Data ===
texts = [
    "how to start python", "python loops", "python functions", "install python",
    "machine learning basics", "data analysis with pandas", "statistics for ml", "what is data science",
    "build website with react", "node js backend", "frontend development", "learn web development"
]
labels = [
    "Python", "Python", "Python", "Python",
    "Data Science", "Data Science", "Data Science", "Data Science",
    "Web Development", "Web Development", "Web Development", "Web Development"
]

categories = ["Python", "Data Science", "Web Development"]
label_map = {c: i for i, c in enumerate(categories)}
y = np.array([label_map[label] for label in labels])

# === Tokenize ===
tokenizer = Tokenizer(num_words=1000, oov_token="<OOV>")
tokenizer.fit_on_texts(texts)
X = tokenizer.texts_to_sequences(texts)
X = pad_sequences(X, maxlen=20)

# === Model ===
model = Sequential([
    Embedding(1000, 16, input_length=20),
    GlobalAveragePooling1D(),
    Dense(16, activation="relu"),
    Dense(len(categories), activation="softmax")
])

model.compile(loss="sparse_categorical_crossentropy",
              optimizer="adam",
              metrics=["accuracy"])

# === Train ===
model.fit(X, y, epochs=30, verbose=1)

# === Save model & tokenizer ===
model.save("text_model.h5")
with open("tokenizer.pkl", "wb") as f:
    pickle.dump(tokenizer, f)

print("✅ Model and tokenizer saved!")
