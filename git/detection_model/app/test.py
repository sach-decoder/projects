import tensorflow as tf
import glob 
import matplotlib.pyplot as plt
import matplotlib.image as mpimg 
import numpy as np
import keras 

image = glob.glob('C:/Users/sachi/OneDrive/testImage/*.jpg') 
image2 = ""

for img_path in image:
    # INCORRECT: plt.imshow(img_path) 
    
    # CORRECT: Read the image data first
    image_data = mpimg.imread(img_path) 
    plt.imshow(image_data)
    plt.show()
    image2 = image_data
    print(image2)

model_path = "C:/Users/sachi/Downloads/detection_model/app/final_trained_model.h5"
model = tf.keras.models.load_model(model_path)

prediction = model.predict(np.expand_dims(image2, axis=0))
print(prediction.tolist())