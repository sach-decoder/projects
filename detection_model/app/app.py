from flask import Flask, request, jsonify
from flask_cors import CORS 
import tensorflow as tf
import numpy as np

app = Flask(__name__)
CORS(app)
from PIL import Image

model_path = "C:/Users/sachi/Downloads/detection_model/app/final_trained_model.h5"

@app.route('/', methods=['POST'])
def modelPredict():

    user_image = request.files['image']

    img = Image.open(user_image.stream).convert('RGB')
    img = img.resize((224, 224))

    final_image = np.array(img)
    final_image = np.expand_dims(final_image, axis=0)
    
    model = tf.keras.models.load_model(model_path)
    prediction = model.predict(final_image)
    model_prediction = prediction.astype(float).tolist()

    return jsonify(model_prediction)
    # return prediction.tolist()
    # if prediction > 0.5:
    #     maligant_pred = prediction.astype('int32')
    #     return jsonify(maligant_pred)
    
    # elif prediction < 0.5:
    #     benign_pred = prediction.astype('int32')
    #     return jsonify(benign_pred)