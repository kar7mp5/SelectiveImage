import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from PIL import Image


label: dict = {0: "가위", 1: "보"} # object's name
img_size: int = 50
train_times: int = 100
img_number: int = 50


img_list = []

img_path = "train_data/test_image"

for i in range(img_number):
    try:
        img_list.append(Image.open(f"{img_path}/{i}.jpg").convert("L"))
    except:
        try:
            img_list.append(Image.open(f"{img_path}/{i}.jpeg").convert("L"))
        except:
            img_list.append(Image.open(f"{img_path}/{i}.png").convert("L"))


resized_img_list = []

for i in range(img_number):
    resized_img_list.append(np.array(img_list[i].resize((img_size, img_size))).reshape(1, -1)[0]/255.)

X = np.array(resized_img_list)
### ###
y_list = []

for i in range(20):
    y_list.append(0)
for j in range(30):
    y_list.append(1)

Y = np.array(y_list)


"""model"""
model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=[img_size**2,]),
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dense(10, activation="softmax")
])

model.compile(optimizer="adam",
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"]
              )

model.summary()

model.fit(X, Y,
          epochs=train_times,
          batch_size= 10,
          validation_split=0.25)

model.save("rocksissorpaper.h5")
new_model = tf.keras.models.load_model("rocksissorpaper.h5")

# predict private image
test_img = Image.open(f"{img_path}/5.jpg").convert("L")
img = np.array(test_img.resize((img_size, img_size))).reshape(1, -1)[0]/255.

print(label[new_model.predict(np.array([img])).argmax()]) # show what object is
print(label[new_model.predict(np.array([img])).argmax()]=="가위")