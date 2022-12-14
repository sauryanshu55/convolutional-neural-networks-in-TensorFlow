# -*- coding: utf-8 -*-
"""convolutional-neural-networks-and-computer-vision-in-TensorFlow.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-RCwoaimM_wp8w1ZvK9NsjLH0LTlysH1

# Convolutional neural networks and Computer Vision with TensorFlow

## Fetching the data
"""

import zipfile
!wget https://storage.googleapis.com/ztm_tf_course/food_vision/pizza_steak.zip
zip_ref=zipfile.ZipFile("pizza_steak.zip")
zip_ref.extractall()
zip_ref.close()

!ls pizza_steak/train/steak

# Walkthrough pizza_steak dir and list num of data
import os

for dirpath, dirnames, filenames in os.walk("pizza_steak"):
  print(f"Directories: {len(dirnames)}, Images: {len(filenames)} in directory: '{dirpath}'\n")

# Visualize images
# Define classes for the images

import pathlib
import numpy as np

data_dir=pathlib.Path("pizza_steak/train")
class_names=np.array(sorted([item.name for item in data_dir.glob("*")]))
class_names

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random

def view_random_image(target_dir, target_class):
  # Setup the target directory 
  target_folder = target_dir+target_class

  # Get a random image path
  random_image = random.sample(os.listdir(target_folder), 1)
  print(random_image)

  # Read in the image and plot it using matplotlib
  img = mpimg.imread(target_folder + "/" + random_image[0])
  plt.imshow(img)
  plt.title(target_class)
#   plt.axis("off");

  print(f"Image shape: {img.shape}") # show the shape of the image

  return img

# View a random image from the training data set
img=view_random_image(target_dir="pizza_steak/train/",
                      target_class="steak")

import tensorflow as tf
print(f"Image as a Tensor:\n {tf.constant(img)}")
print(f"Tensor Shape: {tf.constant(img).shape}")

"""## Building a Convolutional Neural Network (CNN) model"""

# CNN model

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Settting random seed
tf.random.set_seed(42)

# Preprocessing data by scaling/normalizing [pixel vals between 0-1]. Rescaling by 255 because max pixel val is 255
train_datagen=ImageDataGenerator(rescale=1./255)
valid_datagen=ImageDataGenerator(rescale=1./255)

# Setup path to data dir
train_dir="/content/pizza_steak/train"
test_dir="/content/pizza_steak/test"

# Import data from dirs and turn it into batches
train_data=train_datagen.flow_from_directory(directory=train_dir,
                                             batch_size=32,
                                             target_size=(224,224),
                                             class_mode="binary",
                                             seed=42,
)
valid_data=valid_datagen.flow_from_directory(directory=test_dir,
                                             batch_size=32,
                                             target_size=(224,224),
                                             class_mode="binary",
                                             seed=42,
)

# Build a CNN model (same as Tiny VGG neural network architecture)
model_1=tf.keras.models.Sequential([
                                    tf.keras.layers.Conv2D(filters=10,
                                                           kernel_size=3,
                                                           activation=tf.keras.activations.relu,
                                                           input_shape=(224,224,3)),
                                    tf.keras.layers.Conv2D(10,3, activation=tf.keras.activations.relu),
                                    tf.keras.layers.MaxPool2D(pool_size=2, padding="valid"),
                                    tf.keras.layers.Conv2D(10,3, activation="relu"),
                                    tf.keras.layers.Conv2D(10,3, activation="relu"),
                                    tf.keras.layers.MaxPool2D(2),
                                    tf.keras.layers.Flatten(),
                                    tf.keras.layers.Dense(1, activation=tf.keras.activations.relu)
])

# Compile our CNN
model_1.compile(loss=tf.keras.losses.BinaryCrossentropy(),
                optimizer=tf.keras.optimizers.Adam(),
                metrics=["accuracy"])

# Fit the CNN model
history_1=model_1.fit(train_data,
                  epochs=5,
                  steps_per_epoch=len(train_data),
                  validation_data=valid_data,
                  validation_steps=len(valid_data),
)

model_1.summary()

"""## Preprocess Data"""

# Define directory dataset path
train_dir="pizza_steak/train/"
test_dir="pizza_steak/test/"

# Check GPU
!nvidia-smi

# Create train and test data generators and rescale the data
from tensorflow.keras.preprocessing.image import ImageDataGenerator

trainn_datagen=ImageDataGenerator(rescale=1/255.)
test_datagen=ImageDataGenerator(rescale=1/255.)

# Load img data from directories and turn them into batches

train_data=train_datagen.flow_from_directory(directory=train_dir,
                                             target_size=(224,224),
                                             class_mode="binary",
                                             batch_size=32,) 

test_data=train_datagen.flow_from_directory(directory=test_dir,
                                             target_size=(224,224),
                                            class_mode="binary",
                                            batch_size=32,)

"""## Create the model"""

# Create a CNN model (start with a baseline)

from tensorflow.keras.optimizers import Adam 
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPool2D, Activation
from tensorflow.keras import Sequential

# Create a baseline one layer convolutional neural network

model_4=Sequential([
                    Conv2D(filters=10, 
                           kernel_size=3,
                           strides=1, 
                           padding="valid",
                           activation="relu",
                           input_shape=(224,224,3)), # Input layer, specifying input shape
                    
                    Conv2D(10,3,activation="relu"),

                    Conv2D(10,3,activation="relu"),

                    Flatten(),
                    Dense(1, activation="sigmoid") #Output layer, working with binary classificcation so 1
])

model_4.compile(loss="binary_crossentropy",
                optimizer=Adam(),
                metrics=["accuracy"])

model_4.summary()

"""## Fit the model"""

# Check the lengths of training and test data
len(train_data), len(test_data)
# Batch size=32

history_4=model_4.fit(
    train_data,
    epochs=5,
    steps_per_epoch=len(train_data),
    validation_data=test_data,
    validation_steps=len(test_data)
)

"""## Evaluating our model

"""

import pandas as pd

pd.DataFrame(history_4.history).plot(figsize=(10,7));

# Plot the validation and training curves separately

def plot_loss_curves(history):
  """
  Returns separate loss curves for training and validation metrics.
  """
  loss = history.history["loss"]
  val_loss = history.history["val_loss"]

  accuracy = history.history["accuracy"]
  val_accuracy = history.history["val_accuracy"]

  epochs = range(len(history.history["loss"])) # how many epochs did we run for?

  # Plot loss
  plt.plot(epochs, loss, label="training_loss")
  plt.plot(epochs, val_loss, label="val_loss")
  plt.title("loss")
  plt.xlabel("epochs")
  plt.legend()

  # Plot accuracy
  plt.figure()
  plt.plot(epochs, accuracy, label="training_accuracy")
  plt.plot(epochs, val_accuracy, label="val_accuracy")
  plt.title("accuracy")
  plt.xlabel("epochs")
  plt.legend();

plot_loss_curves(history_4)

# If validation loss starts to increase, then the model is overfitting. The graph shows validation data is increasing

"""## Adujusting model overfitting"""

# Creating a new baseline model
# REDUCING OVERFITTING BY ADDING MAXPOOL LAYER!

model_5=Sequential([
    Conv2D(10,3,activation='relu', input_shape=(224,224,3)),
    MaxPool2D(pool_size=2), # To reduce overfitting, maxpool finds the max of the kernel matrix, reducing the output shape
    Conv2D(10,3, activation='relu'),
    MaxPool2D(),
    Conv2D(10,3, activation='relu'),
    MaxPool2D(),
    Flatten(),
    Dense(1,activation='sigmoid' )
])

# Compile the model
model_5.compile(
    loss='binary_crossentropy',
    optimizer=Adam(),
    metrics='accuracy',
)

# Fit the model
history_5=model_5.fit(train_data,
                      epochs=5,
                      steps_per_epoch=len(train_data),
                      validation_data=test_data,
                      validation_steps=len(valid_data),
)

model_5.summary()

# Check loss & accuracy curves to check overfitting

plot_loss_curves(history_5)

## REDUCE OVERFITTING BY ADDING DATA AUGMENTATION! (aka Regularization)

# Create ImageDataGenerator training data with data augmentation

train_datagen_augmented = ImageDataGenerator(rescale=1/255.,
                                             rotation_range=0.2,                                             shear_range=0.2, # how much do you want to shear an image?
                                             zoom_range=0.2, 
                                             width_shift_range=0.2,                                              height_shift_range=0.2, # move your image around on the y-axis
                                             horizontal_flip=True,
                                             )  

# Create ImageDataGenerator without data augmentation
train_datagen = ImageDataGenerator(rescale=1/255.)

# Create ImageDataGenerator without data augmentation for the test dataset
test_datagen = ImageDataGenerator(rescale=1/255.)

# Import data and augment it from training directory
print("Augmented training data:")
train_data_augmented = train_datagen_augmented.flow_from_directory(train_dir,
                                                                   target_size=(224, 224),
                                                                   batch_size=32,
                                                                   class_mode="binary",
                                                                   shuffle=False) 

# Create non-augmented train data batches
print("Non-augmented training data:")
train_data = train_datagen.flow_from_directory(train_dir,
                                               target_size=(224, 224),
                                               batch_size=32,
                                               class_mode="binary",
                                               shuffle=False)

IMG_SIZE = (224, 224)
# Create non-augmented test data batches
print("Non-augmented test data:")
test_data = test_datagen.flow_from_directory(test_dir,
                                             target_size=IMG_SIZE,
                                             batch_size=32,
                                             class_mode="binary")

# Get sample data batches
images, labels = train_data.next()
augmented_images, augmented_labels = train_data_augmented.next()

# Show original image and augmented image
import random
random_number = random.randint(0, 32) # our batch sizes are 32...
print(f"showing image number: {random_number}")
plt.imshow(images[random_number])
plt.title(f"Original image")
plt.axis(False)
plt.figure()
plt.imshow(augmented_images[random_number])
plt.title(f"Augmented image")
plt.axis(False);

model_6 = Sequential([
  Conv2D(10, 3, activation="relu"),
  MaxPool2D(pool_size=2),
  Conv2D(10, 3, activation="relu"),
  MaxPool2D(),
  Conv2D(10, 3, activation="relu"),
  MaxPool2D(),
  Flatten(),
  Dense(1, activation="sigmoid")                      
])

# Compile the model
model_6.compile(loss="binary_crossentropy",
                optimizer=Adam(),
                metrics=["accuracy"])

# Fit the model_6 on augmented training data
history_6 = model_6.fit(train_data_augmented,
                        epochs=5,
                        steps_per_epoch=len(train_data_augmented),
                        validation_data=test_data,
                        validation_steps=len(test_data))

# Check training curves
plot_loss_curves(history_6)

# Shuffling data to improve model accuracy

train_data_augmented_shuffled = train_datagen_augmented.flow_from_directory(train_dir,
                                                                            target_size=(224, 224),
                                                                            class_mode="binary",
                                                                            batch_size=32,
                                                                            shuffle=True)

model_7 = Sequential([
  Conv2D(10, 3, activation="relu", input_shape=(224, 224, 3)),
  MaxPool2D(),
  Conv2D(10, 3, activation="relu"),
  MaxPool2D(),
  Conv2D(10, 3, activation="relu"),
  MaxPool2D(),
  Flatten(),
  Dense(1, activation="sigmoid")                     
])

# Compile the model
model_7.compile(loss="binary_crossentropy",
                optimizer=Adam(), 
                metrics=["accuracy"])

# Fit the model
history_7 = model_7.fit(train_data_augmented_shuffled,
                        epochs=5,
                        steps_per_epoch=len(train_data_augmented_shuffled),
                        validation_data=test_data,
                        validation_steps=len(test_data))

plot_loss_curves(history_7)

"""## Make predictions on custom image"""

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
!wget https://raw.githubusercontent.com/mrdbourke/tensorflow-deep-learning/main/images/03-steak.jpeg
steak=mpimg.imread('03-steak.jpeg')
plt.imshow(steak)
# plt.axis(False)

# Check shape of image before fitting it to model
print(f"Shape={steak.shape}")

"""## Preprocess custom data"""

# Create method to import image and resize to use it in model

def load_and_prep_image(filename, img_shape=224):
    """Reads immage from filename, turns into tensor, 
    and reshapes to (img_shape, img_shape, color_channels)"""

    # Read the image
    img=tf.io.read_file(filename)

    # Decode the read file into a tensor
    img=tf.image.decode_image(img)

    # Resize the image
    img=tf.image.resize(img, size=[img_shape, img_shape])

    # Rescale the image
    img=img/255.

    return img

# Load and pre-process custom images
steak=load_and_prep_image('03-steak.jpeg')
print(steak)
print(f"\n\nShape={steak.shape}")

# Getting image predictions
pred=model_7.predict(tf.expand_dims(steak, axis=0))
pred

# Converting prediction probabilities to class names
class_names

pred_class=class_names[int(tf.round(pred))]
pred_class

def pred_and_plot(model, filename, class_names=class_names):
    img=load_and_prep_image(filename)
    pred=model.predict(tf.expand_dims(img, axis=0))
    # pred_confidence=pred[0]
    pred_class=class_names[int(tf.round(pred))]
    plt.imshow(img)
    plt.title(f'Prediction: {pred_class}')
    plt.axis(False);

pred_and_plot(
    model=model_7,
    filename='03-steak.jpeg'
)

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
!wget https://raw.githubusercontent.com/mrdbourke/tensorflow-deep-learning/main/images/03-pizza-dad.jpeg
pred_and_plot(model_7, '03-pizza-dad.jpeg')

"""# Multiclass image classification

## Fetching the data
"""

# Import data

import zipfile
!wget https://storage.googleapis.com/ztm_tf_course/food_vision/10_food_classes_all_data.zip
zip_ref=zipfile.ZipFile('10_food_classes_all_data.zip')
zip_ref.extractall()
zip_ref.close()

import os
for dirpath,dirnames,filenames in os.walk('10_food_classes_all_data'):
    print(f'Directories: {len(dirnames)} Files: {len(filenames)} in {dirpath}')
# there could be .DS_Store file as well10_food_classes_all_data.zip

# Setup train and test directories

train_dir='10_food_classes_all_data/train/'
test_dir='10_food_classes_all_data/test/'

# Class names
import pathlib
import numpy as np

data_dir=pathlib.Path(train_dir)
class_names=np.array(sorted([item.name for item in data_dir.glob('*')]))
print(class_names)

# Visualize data
import random

img=view_random_image(target_dir=train_dir,
                      target_class=random.choice(class_names))

"""## Preprocessing the data"""

from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Rescale/ Normalize
train_datagen = ImageDataGenerator(rescale=1/255.)
test_datagen = ImageDataGenerator(rescale=1/255.)

# Load data and turn it into batches

IMG_SIZE=(224,224)
train_data = train_datagen.flow_from_directory(train_dir,
                                               target_size=IMG_SIZE,
                                               batch_size=32,
                                               class_mode="categorical")

test_data = test_datagen.flow_from_directory(test_dir,
                                             target_size=IMG_SIZE,
                                             batch_size=32,
                                             class_mode="categorical")

"""##  Create the model"""

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPool2D, Flatten, Dense, Activation

model_8=Sequential([
    Conv2D(10,3, input_shape=(224,224,3)),
    Activation(activation='relu'),

    Conv2D(10,3, activation='relu'),
    MaxPool2D(),

    Conv2D(10,3, activation='relu'),
    Conv2D(10,3,activation='relu'),
    MaxPool2D(),

    Flatten(),
    Dense(10, activation='softmax')
])

model_8.compile(loss='categorical_crossentropy',
                optimizer=tf.keras.optimizers.Adam(),
                metrics=['accuracy'])

"""## Fit the model"""

history_8=model_8.fit(train_data, # This has 10 classes now
                      epochs=5,
                      steps_per_epoch=len(train_data),
                      validation_data=test_data,
                      validation_steps=len(test_data),
                      )

# Check out the loss curves of model_9
plot_loss_curves(history_8)

"""The model is overfitting the training set. It does well on the training data but fails to generalize and perfoms poorly on test data

## Adjust the model hyperparameters to beat the baseline/ reduce overfitting
+ Data augmentation
+ Simplify the model: Reduce # of layers and reduce # hiffen layers
+ Transfer learning
+ More data
"""

# Simplify the model
model_8.summary()

# Remove 2 convolutional layers
model_9=Sequential([
    Conv2D(10,3, input_shape=(224,224,3)),
    Activation(activation='relu'),

    Conv2D(10,3, activation='relu'),
    MaxPool2D(),

    Flatten(),
    Dense(10, activation='softmax')
])

model_9.compile(loss='categorical_crossentropy',
                optimizer=tf.keras.optimizers.Adam(),
                metrics=['accuracy'])

model_9.summary()

# Fit the model
history_9=model_9.fit(train_data, # This has 10 classes now
                      epochs=5,
                      steps_per_epoch=len(train_data),
                      validation_data=test_data,
                      validation_steps=len(test_data),
                      )

plot_loss_curves(history=history_9)

"""## Using data augmentation to try to improve overfitting"""

# Create an augmented data generator instance
train_datagen_augmented = ImageDataGenerator(rescale=1/255.,
                                             rotation_range=0.2,
                                             width_shift_range=0.2,
                                             height_shift_range=0.2,
                                             zoom_range=0.2,
                                             horizontal_flip=True)

train_data_augmented = train_datagen_augmented.flow_from_directory(train_dir,
                                                                   target_size=(224, 224),
                                                                   batch_size=32,
                                                                   class_mode="categorical")

# Clone and fit the model
model_10=tf.keras.models.clone_model(model_8)

# compile
model_10.compile(loss='categorical_crossentropy',
                 optimizer=tf.keras.optimizers.Adam(),
                 metrics=['accuracy'])

history_10=model_10.fit(
    train_data,
    epochs=5,
    steps_per_epoch=len(train_data_augmented),
    validation_data=test_data,
    validation_steps=len(test_data)
)

model_10.evaluate(test_data)

plot_loss_curves(history=history_10)

"""## Making a prediction on the trained model"""

class_names

# Download custom images
!wget https://raw.githubusercontent.com/mrdbourke/tensorflow-deep-learning/main/images/03-pizza-dad.jpeg
!wget https://raw.githubusercontent.com/mrdbourke/tensorflow-deep-learning/main/images/03-hamburger.jpeg
!wget https://raw.githubusercontent.com/mrdbourke/tensorflow-deep-learning/main/images/03-sushi.jpeg
!wget https://raw.githubusercontent.com/mrdbourke/tensorflow-deep-learning/main/images/03-steak.jpeg

# Reconfig pred_and_plot function to work with multi-class images
def pred_and_plot(model, filename, class_names=class_names):
  """
  Imports an image located at filename, makes a prediction with model
  and plots the image with the predicted class as the title.
  """
  # Import the target image and preprocess it
  img = load_and_prep_image(filename)

  # Make a prediction
  pred = model.predict(tf.expand_dims(img, axis=0))

  # Add in logic for multi-class & get pred_class name
  if len(pred[0]) > 1:
    pred_class = class_names[tf.argmax(pred[0])]
  else:
    pred_class = class_names[int(tf.round(pred[0]))]

  # Plot the image and predicted class
  plt.imshow(img)
  plt.title(f"Prediction: {pred_class}")
  plt.axis(False);

pred_and_plot(model=model_10,
              filename="03-steak.jpeg",
              class_names=class_names)

pred_and_plot(model=model_10,
              filename="03-pizza-dad.jpeg",
              class_names=class_names)

pred_and_plot(model=model_10,
              filename="03-hamburger.jpeg",
              class_names=class_names)

pred_and_plot(model=model_10,
              filename="03-sushi.jpeg",
              class_names=class_names)

## Saving the model
model_10.save('saved_trained_model_10')