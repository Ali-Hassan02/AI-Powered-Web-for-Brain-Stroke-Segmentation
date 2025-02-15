# import os 
# from keras.models import load_model

# model_path_unet = '/Users/alihassan/Desktop/Brain/backend/models/2d_Unet_model.keras'
# if not os.path.exists(model_path_unet):
#     print(f"Model file does not exist at {model_path_unet}")
# else:
#     print(f"Model file found at {model_path_unet}")



# try:
#     model = load_model(model_path_unet)
#     print("Model loaded successfully!")
# except Exception as e:
#     print(f"Error loading model: {e}")    import h5py
# import h5py
# model_path_unet = '/Users/alihassan/Desktop/Brain/backend/models/2d_Unet_model.keras'

# try:
#     with h5py.File(model_path_unet, 'r') as f:
#         print("This is a valid HDF5 file.")
# except Exception as e:
#     print(f"Error: {e}")
import os
from tensorflow.keras.models import load_model
import tensorflow as tf 


import numpy as np
import tensorflow as tf
from tensorflow.keras import backend as K

smooth = 1e-15
def dice_coef(y_true, y_pred):
    y_true = tf.keras.layers.Flatten()(y_true)
    y_pred = tf.keras.layers.Flatten()(y_pred)
    intersection = tf.reduce_sum(y_true * y_pred)
    return (2. * intersection + smooth) / (tf.reduce_sum(y_true) + tf.reduce_sum(y_pred) + smooth)

def dice_loss(y_true, y_pred):
    return 1.0 - dice_coef(y_true, y_pred)


model_path_unet = '/Users/alihassan/Desktop/Brain/backend/models/2d_Unet_model.h5'


# Check if the model exists
if not os.path.exists(model_path_unet):
    print(f"Model file does not exist at {model_path_unet}")
else:
    print(f"Model file found at {model_path_unet}")

try:
    # Attempt to load the model
    model = tf.keras.models.load_model(
        model_path_unet, 
        custom_objects={"dice_loss": dice_loss, "dice_coef": dice_coef}  # Replace with your custom loss/metric
    )
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
