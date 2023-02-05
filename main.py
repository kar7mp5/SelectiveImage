from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import urllib.request
import tkinter as tk
import time, os, sys, csv


import numpy as np
import tensorflow as tf
from PIL import Image


"""Title : SelectiveImage"""
class SelectiveImage:
    def __init__(self):
        self.requested_image_name : str = "" # Requested Image Name
        self.requested_image_number : str = "" # Requested Image Number
        self.first_download_image : int = 50 # 1st Downlaod Image
        self.test_image_path : str = f"{os.getcwd()}/train_data/test_image/"
        self.chrome_driver_path : str = f"{os.getcwd()}/driver/chromedriver.exe" # Chrome Driver Path


    def first_cralwing(self):
        """Basic Setting"""
        window = tk.Tk()
        window.title("ImageDownloader") # Window's Title
        window.geometry("300x150+1000+100") # Window's Location
        window.resizable(False, False)
        window.columnconfigure(0, weight=1) # Configure the grid
        window.columnconfigure(1, weight=3) # Configure the grid
        """Get Data from User"""
        def get_text(): # Get Text from User
            self.requested_image_name = requested_image_name_entry.get() # Requested Image Name
            self.requested_image_number = requested_image_number_entry.get() # Requested Image Number
            window.destroy()
        # Get Image Name
        requested_image_name_label = tk.Label(window, text="Insert Image Name:") # Text : Request Image Name
        requested_image_name_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        requested_image_name_entry = tk.Entry(window) # InputBox
        requested_image_name_entry.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)
        # Get Image Number
        requested_image_number_label = tk.Label(window, text="Insert Image Number:") # Text : Request Image Number
        requested_image_number_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        requested_image_number_entry = tk.Entry(window) # InputBox
        requested_image_number_entry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)
        # get text button
        login_button = tk.Button(window, text="Download", command=get_text) # command : get_text
        login_button.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)

        window.mainloop()

        if self.requested_image_name == "" or self.requested_image_number == "": # requested_image_name && requested_image_number == null --> Exit Program
            sys.exit()
        """Search Image"""
        driver = webdriver.Chrome(self.chrome_driver_path)
        driver.implicitly_wait(10)
        driver.get("https://www.google.com/imghp?hl=ko&tab=8i") # Open Google Photo
        search_box = driver.find_element(By.CLASS_NAME, "gLFyf")
        search_box.send_keys(self.requested_image_name) ; search_box.send_keys(Keys.RETURN) # Insert Requested Image Name
        last_height = driver.execute_script("return document.body.scrollHeight") # Scroll Down to End

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                try:
                    driver.find_element(By.CSS_SELECTOR, "input.mye4qd").click()
                except:
                    break
            last_height = new_height
        """Download Image"""
        image_list = driver.find_elements(By.CSS_SELECTOR, "img.rg_i.Q4LuWd")
        INDEX : int = 0
        saved_image_path : str = ""
        for image in image_list:
            if INDEX == int(self.first_download_image): # As All Images are Downloaded
                break
            try:
                driver.implicitly_wait(2)
                image.click()
                image_link = str(driver.find_element(By.CSS_SELECTOR, "img.n3VNCb.KAlRDb").get_attribute("src"))
                """Distribute File's Format"""
                if ".jpg" in image_link : saved_image_path = f"{self.test_image_path}{INDEX}.jpg" # .jpg
                elif ".jpeg" in image_link : saved_image_path = f"{self.test_image_path}{INDEX}.jpeg" # .jpeg
                elif ".png" in image_link : saved_image_path = f"{self.test_image_path}{INDEX}.png" # .png
                else : print("Error : Out of the Style") ; continue # Error : Out of the Style
                urllib.request.urlretrieve(str(image_link), str(saved_image_path)) # Download Selected Image
                INDEX += 1
            except: print("Error : Blocked by Website") ; pass # Error : Blocked by Website

        driver.close()


    def train_model(self):
        label : dict = {0: "가위", 1: "보"}
        IMAGE_SIZE : int = 50
        TRAIN_EPOCH : int = 100
        IMAGE_NUMBER : int = 50


        image_list : list = []

        for i in range(IMAGE_NUMBER):
            try:
                image_list.append(Image.open(f"{self.test_image_path}{i}.jpg").convert("L"))
            except:
                try:
                    image_list.append(Image.open(f"{self.test_image_path}{i}.jpeg").convert("L"))
                except:
                    image_list.append(Image.open(f"{self.test_image_path}{i}.png").convert("L"))


        resized_image_list : list = []


        for i in range(IMAGE_NUMBER):
            resized_image_list.append(np.array(image_list[i].resize((IMAGE_SIZE, IMAGE_SIZE))).reshape(1, -1)[0]/255.)

        X = np.array(resized_image_list)

        y_list : list = []

        for i in range(IMAGE_NUMBER):
            y_list.append(0)

        Y = np.array(y_list)

        # Load Train Model
        model = tf.keras.Sequential([
            tf.keras.layers.InputLayer(input_shape=[IMAGE_SIZE**2,]),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dense(10, activation="softmax")
        ])
        # Compile Model
        model.compile(  
                        optimizer="adam",
                        loss="sparse_categorical_crossentropy",
                        metrics=["accuracy"]
                     )
        # Train Model
        model.fit(
                    X, Y,
                    epochs=TRAIN_EPOCH,
                    batch_size= 10,
                    validation_split=0.25
                 )

        model.save("rocksissorpaper.h5") # Save Model


        new_model = tf.keras.models.load_model("rocksissorpaper.h5")


        # predict private image
        test_img = Image.open(f"{self.test_image_path}/50.jpg").convert("L")
        img = np.array(test_img.resize((IMAGE_SIZE, IMAGE_SIZE))).reshape(1, -1)[0]/255.


        print(label[new_model.predict(np.array([img])).argmax()]) # show what object is
        print(label[new_model.predict(np.array([img])).argmax()]=="가위")


if __name__=="__main__":
    selective_image = SelectiveImage()
    # selective_image.first_cralwing()
    selective_image.train_model()