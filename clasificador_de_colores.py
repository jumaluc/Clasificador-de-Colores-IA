
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np


datagen = ImageDataGenerator(
    rescale= 1. /255,
    rotation_range =10,
    width_shift_range=0.15,
    height_shift_range=0.15,
    shear_range=5,
    zoom_range = [0.7, 1.3],
    validation_split = 0.2
)
data_gen_entrenamiento = datagen.flow_from_directory("/content/dataset", target_size=(224,224), batch_size=32, shuffle=True, subset="training")
data_gen_pruebas = datagen.flow_from_directory("/content/dataset", target_size=(224,224), batch_size=32, shuffle=True, subset="validation")



import matplotlib.pyplot as plt

for imagenes,etiquetas in data_gen_entrenamiento:
  for i in range(10):
    plt.subplot(2,5, i+1)
    plt.imshow(imagenes[i])

  break
plt.show()

modelo = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), input_shape=(224,224,3), activation="relu"),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(units=100, activation="relu"),
    tf.keras.layers.Dense(4, activation="softmax")
])
modelo.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)



import math
entrenamiento = modelo.fit(
    data_gen_entrenamiento,
    steps_per_epoch=20,
    validation_data=data_gen_pruebas,
    validation_steps=10,
    epochs=10
)

from PIL import Image
import cv2

def categorizar(ruta):
  img = Image.open(ruta)
  img = img.convert("RGB")
  img = np.array(img).astype(float)/255

  img = cv2.resize(img, (224, 224))
  prediccion = modelo.predict(img.reshape(-1,224,224,3))

  return np.argmax(prediccion[0], axis=-1)

#INGRESAR LA IMAGEN PARA TESTEAR :
ruta = "sangre.jpg"
prediccion = categorizar(ruta)
if prediccion == 0 :
  print("El color es AMARILLO")
elif prediccion == 1:
  print("El color es AZUL")
elif prediccion == 2:
  print("El color es ROJO")
elif prediccion == 3:
  print("El color es VERDE")