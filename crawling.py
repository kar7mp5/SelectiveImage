from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import urllib.request
import tkinter as tk
import time
import os
import sys


"""Title : SelectiveImage"""

class SelectiveImage:
    def __init__(self):
        self.requested_image_name : str = "" # Requested Image Name
        self.requested_image_number : str = "" # Requested Image Number
        self.chrome_driver_path : str = f"{os.getcwd()}/driver/chromedriver.exe" # Chrome Driver Path
        self.main()

    def read_data_from_csv(self):
        pass

    def train_model(self):
        pass

    def save_model(self): # Convert .h5 format to .dp
        pass

    def distribute_image(self):
        pass


    def main(self):
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
        INDEX = 0
        saved_image_path: str = ""
        for image in image_list:
            if INDEX == int(self.requested_image_number): # As All Images are Downloaded
                break
            try:
                driver.implicitly_wait(2)
                image.click()
                image_link = str(driver.find_element(By.CSS_SELECTOR, "img.n3VNCb.KAlRDb").get_attribute("src"))
                """Distribute File's Format"""
                if ".jpg" in image_link : saved_image_path = f"img/{INDEX}.jpg" # .jpg
                elif ".jpeg" in image_link : saved_image_path = f"img/{INDEX}.jpeg" # .jpeg
                elif ".png" in image_link : saved_image_path = f"img/{INDEX}.png" # .png
                else : print("Error : Out of the Style") ; continue # Error : Out of the Style
                urllib.request.urlretrieve(str(image_link), str(saved_image_path)) # Download Selected Image
                INDEX += 1
            except : print("Error : Blocked by Website") ; pass # Error : Blocked by Website

        driver.close()


if __name__=="__main__":
    SelectiveImage()