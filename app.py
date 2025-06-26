from flask import Flask, render_template, request, jsonify
import numpy as np
import tensorflow as tf
from PIL import Image
import io
import base64

app = Flask(__name__)
model = tf.keras.models.load_model('model/mnist_model.h5')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json['image']  # Get base64 string
    image_data = base64.b64decode(data.split(',')[1])
    image = Image.open(io.BytesIO(image_data)).convert('L')  # Grayscale
    image = image.resize((28, 28))
    image_np = np.array(image)
    image_np = 255 - image_np  # Invert colors (black digit on white)
    image_np = image_np / 255.0
    image_np = image_np.reshape(1, 28, 28, 1)

    prediction = model.predict(image_np)
    digit = np.argmax(prediction)

    return jsonify({'prediction': int(digit)})

if __name__ == '__main__':
    app.run(debug=True)
