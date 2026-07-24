import cv2 
import glob
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

#Training arrays
train_images = []
test_array = []
train_labels = np.asarray(test_array)
filtered_train_images = []

#Validation arrays
val_images = []
val_labels = []
val_array = []

input_size = (224, 224, 3)


#Kernel for Image sharpening:
kernel = np.array([ [0, -1, 0], 
                    [-1, 5, -1], 
                    [0, -1, 0]], dtype=np.float32)

class TrainingSet:
    @staticmethod
    def import_train_images():
        for file in glob.glob('C:/Users/sachi/Downloads/detection_model/breast_mri_dataset/train/Malignant/*.jpg'):
            if file is not None:
                train_images.append(cv2.imread(file))
                test_array.append(1)

        for file in glob.glob('C:/Users/sachi/Downloads/detection_model/breast_mri_dataset/train/Benign/*.jpg'):
            if file is not None:
                train_images.append(cv2.imread(file))
                test_array.append(0)

    @staticmethod
    def train_image_sharpening():
        for i in range(len(train_images)):
            train_images[i] = cv2.filter2D(
                train_images[i], 
                ddepth=-1, 
                kernel=kernel, 
                anchor=(-1, -1), 
                delta=0, 
                borderType=cv2.BORDER_DEFAULT
            )
            filtered_train_images.append(train_images[i])

TrainingSet.import_train_images()
TrainingSet.train_image_sharpening()
#Final Training sets passed to model
X_train = np.asarray(filtered_train_images) 
train_labels = np.asarray(test_array)
Y_train = train_labels


if train_images and test_array:
    print('Both arrays have been fiiled.')
    print(f'Length of trainset: {len(train_images)}')
    print(f'Length of trainlabels: {len(test_array)}')

class ValidationSet:
    @staticmethod
    def import_val_images():
        for file in glob.glob('C:/Users/sachi/Downloads/detection_model/breast_mri_dataset/val/Malignant/*.jpg'):
            if file is not None:
                val_images.append(cv2.imread(file))
                val_labels.append(1)

        for file in glob.glob('C:/Users/sachi/Downloads/detection_model/breast_mri_dataset/val/Benign/*.jpg'):
            if file is not None:
                val_images.append(cv2.imread(file))
                val_labels.append(0)

    @staticmethod
    def val_image_sharpening():
        for i in range(len(val_images)):
            val_images[i] = cv2.filter2D(
                val_images[i], 
                ddepth=-1, 
                kernel=kernel, 
                anchor=(-1, -1), 
                delta=0, 
                borderType=cv2.BORDER_DEFAULT
            )
            val_array.append(val_images[i])

ValidationSet.import_val_images()
ValidationSet.val_image_sharpening()
#Final Validation sets passed to model
X_val = np.asarray(val_array)
Y_val = np.asarray(val_labels)

if val_images and val_labels:
    print('Both arrays have been fiiled.')
    print(f'Length of trainset: {len(val_images)}')
    print(f'Length of trainlabels: {len(val_labels)}')

print(f'length of X_train: {len(X_train)}')
print(f'length of Y_train: {len(Y_train)}')

class Model:

    @staticmethod
    def neural_network():
        model = tf.keras.Sequential([
    
        #Convolution Layers
        tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=input_size),
        tf.keras.layers.MaxPooling2D(pool_size=(2,2)), 

        tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
        tf.keras.layers.MaxPooling2D(pool_size=(2,2)), 
        tf.keras.layers.Dropout(0.2), 

        tf.keras.layers.Conv2D(128, (3,3), activation='relu'), 
        tf.keras.layers.MaxPooling2D(pool_size=(2,2)), 

        #Flatten Extraction for Dense Layers
        tf.keras.layers.Flatten(),

        #Dense Layers
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.25),
        tf.keras.layers.Dense(64, activation='relu'),

        #Ouput Layer => Outputs Binary Classification 0 or 1.
        tf.keras.layers.Dense(1, activation='sigmoid')
])
        return model
    
    @staticmethod
    def model_fit(model):
        model.compile(optimizer='adam', 
              loss= tf.keras.losses.BinaryCrossentropy(from_logits=False), 
              metrics=['accuracy'])
        early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=4, restore_best_weights=True)

        model.fit(
            X_train, Y_train, 
            validation_data=(X_val, Y_val), 
            batch_size= 25,
            callbacks=[early_stop]
        )
        return model
model = Model.neural_network()
final_model = Model.model_fit(model)
final_model.save("C:/Users/sachi/Downloads/detection_model/app/final_trained_model.h5")