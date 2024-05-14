from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

MODEL_PATH = 'mobilenetv2.h5'

model = load_model(MODEL_PATH)
print('Model loaded. check localhost')

class_dict = {
    'Arabica': 0,
    'Excela': 1,
    'Liberica': 2,
    'Robusta': 3
}

class_labels = list(class_dict.keys())

def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))

    # # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    x = np.expand_dims(x, axis=0)

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    # x = preprocess_input(x, mode='caffe')

    preds = model.predict(x)
    prob = np.max(preds[0])
    highest_prob = prob*100

    return [preds, highest_prob]

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        prediction = model_predict(file_path, model)
        preds = prediction[0]
        highest_prob = prediction[1]

        # Access label and Confidence Score
        p = np.argmax(preds, axis=1)
        predicted_label = class_labels[p[0]]

        # Get the actual label via filename
        filename = os.path.splitext(os.path.basename(file_path))[0]
        actual_label = re.sub(r'\d+', '', filename)

        result = f"{predicted_label} ({highest_prob:.2f}% Confidence)\n" \
        f"Actual Label: {actual_label}"

        # deletes the file after, can remove this if we want to have a history feature
        os.remove(file_path) 

        return result
    return None

if __name__ == '__main__':
    app.run(debug=True)