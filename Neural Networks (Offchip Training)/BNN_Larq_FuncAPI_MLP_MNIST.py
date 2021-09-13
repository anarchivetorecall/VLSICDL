import os
import tensorflow as tf
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from keras.layers import Input
from keras.models import Model
import larq 

# Import MNIST dataset
(train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()
train_images = train_images.reshape((60000, 28, 28))
test_images = test_images.reshape((10000, 28, 28))

# Normalize pixel values to be between -1 and +1, and binarize it to -1 and +1
train_images, test_images = train_images / 127.5 -1, test_images / 127.5 -1
train_images_binary = np.where(train_images > 0, 1, -1)
test_images_binary = np.where(test_images > 0, 1, -1)

# Returns input tensor
nonflat_input_layer = Input(shape=(28, 28, 1))
input_layer = keras.layers.Flatten()(nonflat_input_layer)

# It is possible to callback intermediate activations
hidden1 = larq.layers.QuantDense(
    512,
    kernel_quantizer= "ste_sign",
    kernel_constraint= "weight_clip",
    name = "first_hidden_layer")(input_layer)
batchnorm1 = tf.keras.layers.BatchNormalization(momentum = 0.99, scale=False)(hidden1)
quantize1 = larq.quantizers.SteSign()(batchnorm1)
hidden2 = larq.layers.QuantDense(
    512,
    kernel_quantizer= "ste_sign",
    kernel_constraint= "weight_clip",
    name = "second_hidden_layer")(quantize1)
batchnorm2 = tf.keras.layers.BatchNormalization(momentum= 0.99, scale=False)(hidden2)
quantize2 = larq.quantizers.SteSign()(batchnorm2)
hidden3 = larq.layers.QuantDense(
    512,
    kernel_quantizer= "ste_sign",
    kernel_constraint= "weight_clip",
    name = "third_hidden_layer")(quantize2)
batchnorm3 = tf.keras.layers.BatchNormalization(momentum= 0.99, scale=False)(hidden3)
quantize3 = larq.quantizers.SteSign()(batchnorm3)
output_layer = larq.layers.QuantDense(
    10,
    activation= "softmax",
    kernel_quantizer= "ste_sign",
    kernel_constraint="weight_clip",
    name = "output_layer")(quantize3)

# Implementing a model based on given functional API codes
model = Model(inputs= nonflat_input_layer, outputs= output_layer)

# Compile & Train the model
model.compile(
    optimizer = 'adam',
    loss = 'sparse_categorical_crossentropy',
    metrics = ['accuracy'])


with larq.context.quantized_scope(True):
    model.save("Larq_Binary_MLP_functionalAPI_version.h5")
    func_api_weights = model.get_weights()
    features_list = [layer.output for layer in model.layers]
    feat_extraction_model = keras.Model(inputs = model.input, outputs = features_list)
    activations = feat_extraction_model(test_images_binary)
    act_1 = activations[4].numpy()
    act_2 = activations[7].numpy()
    act_3 = activations[10].numpy()
    output = activations[11].numpy()
    batchnorm_val1 = activations[3].numpy()
    batchnorm_val2 = activations[6].numpy()
    batchnorm_val3 = activations[9].numpy()
    before_act_1 = activations[2].numpy()
    before_act_2 = activations[5].numpy()
    before_act_3 = activations[8].numpy()


model.fit(train_images_binary, train_labels, batch_size = 300, epochs = 30)

test_loss, test_acc = model.evaluate(test_images_binary, test_labels)

print(f"Test accuracy {test_acc * 100:.2f} %")
