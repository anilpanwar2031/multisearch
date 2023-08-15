import io
import os
from PIL import Image
import string,random
from pathlib import Path
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from azure.storage.blob import BlobServiceClient


def replace_strings(string, *args):
    return string % args

def format_string(input_string, val_dict):
    formatted_string = input_string.format(**val_dict)
    if "%s" in input_string and "!@" in input_string:
        clk, data = input_string.split('!@')[0], [input_string.split('!@')[1:]]
        formatted_string = replace_strings(clk, *[val_dict.get(x) for x in data[0]])
    return formatted_string


def upload_image_to_azure(image_path, container_name, connection_string):
    try:
        # Create BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Create BlobClient and upload the image
        random_=''.join(random.choices(string.ascii_uppercase +string.digits, k=10))
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=random_+image_path)

        with open(image_path, "rb") as data:
            blob_client.upload_blob(data)
 
        # Generate the URL for the uploaded image
        
        url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{random_}{image_path}"
        return url

    except Exception as e:
        print("An error occurred:", str(e))
        return None

def upload_pdf_to_azure(pdf_path, container_name, connection_string):
    random_=''.join(random.choices(string.ascii_uppercase +string.digits, k=10))
    try:
        file_name = f"{random_}/{Path(pdf_path).name}"
        # Create BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Create BlobClient and upload the image
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

        with open(pdf_path, "rb") as data:
            blob_client.upload_blob(data)
 
        # Generate the URL for the uploaded image
        
        url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{file_name}"
        return url, Path(pdf_path).name

    except Exception as e:
        print("An error occurred while uploading PDF to blob:", str(e))
        return None, None

def screenshot(driver):
    mewo =[]
    screenshot = driver.get_screenshot_as_png()
    mewo.append(screenshot)
    innerHeight =driver.execute_script("return window.innerHeight;")
    scroll =innerHeight
    scrollHeight =driver.execute_script("return document.body.scrollHeight;")
    print(innerHeight,"inner")
    print(scrollHeight,"scrool")

    while True:
        if scrollHeight <= innerHeight:
            break
        driver.execute_script(f"window.scrollTo(0, {innerHeight})")
        print(scroll)
        screenshot = driver.get_screenshot_as_png()
        print(type(screenshot))
        mewo.append(screenshot)
        innerHeight = innerHeight + scroll
        
    image1 =Image.open(io.BytesIO(mewo[0]))
    width1, height1 = image1.size
    new_image = Image.new('RGB', (width1, height1 * len(mewo)), (255, 255, 255))
    driver.execute_script("window.scrollTo(0,0);")

    y_offset = 0
    for filename in mewo:
        image = Image.open(io.BytesIO(filename))
        new_image.paste(image, (0, y_offset))
        y_offset += image.size[1]
    new_image.save( 'combined_image.png')
def screenshot_pagewise(driver):
    mewo =[]
    screenshot = driver.get_screenshot_as_png()
    mewo.append(screenshot)
    innerHeight =driver.execute_script("return window.innerHeight;")
    scroll =innerHeight
    scrollHeight =driver.execute_script("return document.body.scrollHeight;")
    print(innerHeight,"inner")
    print(scrollHeight,"scrool")
    print("mewo35")
    while True:
        print("im loppp")
        if scrollHeight <= innerHeight:
            break
        driver.execute_script(f"window.scrollTo(0, {innerHeight})")
        print(scroll)
        screenshot = driver.get_screenshot_as_png()
        print(type(screenshot))
        mewo.append(screenshot)
        innerHeight = innerHeight + scroll
    driver.execute_script("window.scrollTo(0,0);")        
    
    return mewo
def ElementSCreenhot(driver,xpath):
 #   driver.execute_script("try{document.evaluate(arguments[0],document,null,XPathResult.FIRST_ORDERED_NODE_TYPE,null).singleNodeValue.scrollIntoView(false);return true;}catch(err){return false;}", xpath)
    wait  =WebDriverWait(driver,7)
    print(xpath)
    element =None
    try:
        element =wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    except:
        print(xpath,"not found")    

    if element:
        data =element.screenshot_as_png
        return data 


       
    
    