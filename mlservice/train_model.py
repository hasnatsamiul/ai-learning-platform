import tensorflow as tf
import numpy as np
from tensorflow.keras import layers

# -----------------------
# Training data
# -----------------------
texts = np.array([
    "how to start python", "python loops", "python functions", "install python",
    "machine learning basics", "data analysis with pandas", "statistics for ml", "what is data science",
    "build website with react", "node js backend", "frontend development", "learn web development"
], dtype=object)

labels = np.array([
    "Python", "Python", "Python", "Python",
    "Data Science", "Data Science", "Data Science", "Data Science",
    "Web Development", "Web Development", "Web Development", "Web Development"
], dtype=object)

categories = ["Python", "Data Science", "Web Development"]
label_map = {c: i for i, c in enumerate(categories)}
y = np.array([label_map[l] for l in labels], dtype=np.int32)

# -----------------------
# Vectorizer (replaces Tokenizer + pickle)
# -----------------------
MAX_TOKENS = 2000
SEQ_LEN = 20

vectorizer = layers.TextVectorization(
    max_tokens=MAX_TOKENS,
    output_mode="int",
    output_sequence_length=SEQ_LEN,
    standardize="lower_and_strip_punctuation",
)
vectorizer.adapt(texts)

# -----------------------
# Model (better than GlobalAveragePooling)
# -----------------------
inputs = tf.keras.Input(shape=(1,), dtype=tf.string)
x = vectorizer(inputs)
x = layers.Embedding(MAX_TOKENS, 64)(x)
x = layers.Bidirectional(layers.LSTM(64, dropout=0.2, recurrent_dropout=0.0))(x)
x = layers.Dense(64, activation="relu")(x)
x = layers.Dropout(0.3)(x)
outputs = layers.Dense(len(categories), activation="softmax")(x)

model = tf.keras.Model(inputs, outputs)

model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-3),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

# -----------------------
# Train
# -----------------------
callbacks = [
    tf.keras.callbacks.EarlyStopping(monitor="loss", patience=5, restore_best_weights=True)
]
model.fit(texts, y, epochs=50, batch_size=4, verbose=1, callbacks=callbacks)

# -----------------------
# Save (single artifact, no tokenizer.pkl needed)
# -----------------------
model.save("text_model_saved")  # SavedModel folder
print(" SavedModel exported to: text_model_saved/")
