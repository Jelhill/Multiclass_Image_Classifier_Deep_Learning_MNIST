from flask import Flask, request, jsonify , render_template, request , url_for , redirect
import requests
import traceback
import logging
import os
import pickle
import  numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt
import numpy as np
import cv2
import numpy as np
import pickle
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import sys
import tkinter

app = Flask(__name__)


UPLOAD_FOLDER = './upload'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route("/index")
@app.route("/")
def collabpage():

    return render_template("index.html")

@app.route("/mnist", methods=["POST"])
def mnist():

    try :

        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)
        image_read = Image.open(path);
        #     plt.imshow(image_read);

        # image_read = cv2.imread('7.png',0)
        original_image = np.asarray(image_read)
        width, height = 28, 28
        resize_image = np.zeros(shape=(width, height))

        for W in range(width):
            for H in range(height):
                new_width = int(W * original_image.shape[0] / width)
                new_height = int(H * original_image.shape[1] / height)
                resize_image[W][H] = original_image[new_width][new_height]
        x = resize_image.reshape(1, 28, 28, 1)
        #     print("Resized image size : " , resize_image.shape)
        filename = 'finalized_model.sav'
        loaded_model = pickle.load(open(filename, 'rb'))
        results = loaded_model.predict(x)
        result = np.argmax(results)
        print(result)
        result = str(result)


        # return jsonify({"the result of picture prediction is ": result}), 200
        return render_template("index.html", prediction_text=f"The result of our prediction is {result}")



    except Exception as p :
        return jsonify({"msgcode": 4, "status": "failed", "message": "Failed to Connect  {}".format(p)}), 401

    return render_template("index.html", prediction_text=f"The result of our prediction is {result}")



if __name__ == "__main__":
    app.run(debug=True)