
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from PIL import Image
import gc
def build_unet(input_shape=(512, 512, 1)):
    '''
    Specifies the model's structure
    :param input_shape: shape of the input image (default is (512, 512, 1))
    '''
    def conv_block(x, filters):
        x = layers.Conv2D(filters, (3, 3), padding='same', activation='relu')(x)
        x = layers.Conv2D(filters, (3, 3), padding='same', activation='relu')(x)
        return x

    inputs = layers.Input(shape=input_shape)

    # Encoder
    c1 = conv_block(inputs, 32); p1 = layers.MaxPooling2D((2, 2))(c1)
    c2 = conv_block(p1, 64); p2 = layers.MaxPooling2D((2, 2))(c2)
    c3 = conv_block(p2, 128); p3 = layers.MaxPooling2D((2, 2))(c3)
    c4 = conv_block(p3, 256); p4 = layers.MaxPooling2D((2, 2))(c4)

    # Bottleneck
    c5 = conv_block(p4, 512)

    # Decoder
    u6 = layers.Conv2DTranspose(256, (2, 2), strides=(2, 2), padding='same')(c5)
    u6 = layers.concatenate([u6, c4])
    c6 = conv_block(u6, 256)

    u7 = layers.Conv2DTranspose(128, (2, 2), strides=(2, 2), padding='same')(c6)
    u7 = layers.concatenate([u7, c3])
    c7 = conv_block(u7, 128)

    u8 = layers.Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same')(c7)
    u8 = layers.concatenate([u8, c2])
    c8 = conv_block(u8, 64)

    u9 = layers.Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same')(c8)
    u9 = layers.concatenate([u9, c1])
    c9 = conv_block(u9, 32)

    outputs = layers.Conv2D(1, (1, 1), activation='sigmoid')(c9)

    return models.Model(inputs, outputs)

def unet_inference(input_image: Image.Image, model, save_path='predictions') -> Image.Image:
    '''
    Convert image to greyscale, resize, enhance using pretrained .h5 model.
    Save prediction and return enhanced image.
    :param input_image: PIL Image
    :param: model
    :param save_path: folder to save result
    :return: enhanced PIL image
    '''
    os.makedirs(save_path, exist_ok=True)
    
    # Convert to grayscale and resize
    image_gray = input_image.convert("L").resize((512, 512))

    # Prepare for model: [1, 512, 512, 1]
    image_array = np.array(image_gray) / 255.0
    image_array = np.expand_dims(image_array, axis=(0, -1))  # Shape: (1, 512, 512, 1)

    # Predict
    prediction = model.predict(image_array)[0, ..., 0]  # Shape: (512, 512)

    # Convert prediction to image (rescale to [0,255])
    prediction_img = Image.fromarray((prediction * 255).astype(np.uint8))

    # Save prediction
    # filename = "enhanced_image.png"
    # prediction_img.save(os.path.join(save_path, filename))
    tf.keras.backend.clear_session()  # Clear TensorFlow session
    gc.collect()  # Run garbage collection to free up memory
    return prediction_img