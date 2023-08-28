import numpy as np
import pandas as pd
from PIL import Image

import tensorflow as tf

import os

labels = ['Pepper__bell___Bacterial_spot',
          'Pepper__bell___healthy',
          'Potato___Early_blight',
          'Potato___Late_blight',
          'Potato___healthy',
          'Tomato_Bacterial_spot',
          'Tomato_Early_blight',
          'Tomato_Late_blight',
          'Tomato_Leaf_Mold',
          'Tomato_Septoria_leaf_spot',
          'Tomato_Spider_mites_Two_spotted_spider_mite',
          'Tomato__Target_Spot',
          'Tomato__Tomato_YellowLeaf__Curl_Virus',
          'Tomato__Tomato_mosaic_virus',
          'Tomato_healthy']


def preprocess_image(image_path):
    image = Image.open(image_path)
    image = image.resize((256, 256))  # Resize to match model's input size
    image_array = np.array(image)
    image_array = image_array / 255.0  # Normalize pixel values
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
    return image_array

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

model = tf.saved_model.load('my_model')

image_path = r'dataset\PlantVillage\Potato___healthy\0b3e5032-8ae8-49ac-8157-a1cac3df01dd___RS_HL 1817.JPG'

img = preprocess_image(image_path)
img = tf.convert_to_tensor(img, dtype=tf.float32)


predictions = model(img)
probabilities = tf.nn.softmax(predictions, axis=-1)

print('\n\n')
print('-----------------------------')
print('-----------------------------')
print('-----------------------------')

print('Prediction: ', labels[np.argmax(probabilities)])
print('Confidence: ', 100 * np.max(probabilities))
