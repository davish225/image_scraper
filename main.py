# https://imgur.com/gallery/aPjMhcR

from bs4 import BeautifulSoup
import requests
import configparser
from imgurpython import ImgurClient
import urllib
import os
import shutil


url = "https://imgur.com/gallery/OToFZd4"
# get url information using requests using http requests
request = requests.get(url)

page = BeautifulSoup(request.text, features="html.parser")
# title created by formatting and removing all spaces
title = page.title.text.strip()


def path_creation():
    directory_choice = input("Would you like to use the current directory? Y/N: ")
    directories = os.listdir()
    if directory_choice.lower() == "y":

        new_directory = os.getcwd() + "\\" + title

        if os.path.isdir(new_directory):
                return new_directory
        else:
            try:
                os.mkdir(new_directory)
            except OSError:
                print("unable to create directory with web page's name")
            else:
                return new_directory
    elif directory_choice.lower() == "n":
        path = input("Please input a new absolute path to the directory you want the folder created in.")
        new_directory = path + "\\" + title
        if new_directory in directories:
            return new_directory
        else:
            try:
                os.mkdir(new_directory)
            except OSError:
                print("unable to create directory with web page's name")
            else:
                return new_directory

def image_retrieval():
    '''
    Uses the Imgur API to retrieve the links of all the images in an album on a page
    :return: List: list of all URLs in album
    '''
    config = configparser.ConfigParser()  # Uses config parser to retrieve the authentication key located in the .ini
    config.read("auth_dev.ini")
    client_id = config.get('credentials', "client_id")
    client_secret = config.get('credentials', "client_secret")
    client = ImgurClient(client_id, client_secret)

    image_id = url[-7:]  # Imgur uses an alphanumeric combination to identify galleries

    images = client.get_album_images(image_id)  # API call to retrieve Image objects

    image_urls = []
    for img in images:  # Loop used to retrieve the links from the Image objects
        image_urls.append(img.link)
    return image_urls


def image_download():
    urls = image_retrieval()
    for image in urls[:1]:
        urllib.request.urlretrieve(image, image[-7:])


def directory_population():
    duplicate = 1
    source_path = os.getcwd()
    directory_list = os.listdir(source_path)

    destination_path = path_creation()
    destination_list = os.listdir(destination_path)

    for files in directory_list:
        if files.endswith('.jpg'):

            if files in destination_list:
                print("error")
                os.rename(files,files[:-4]+"-"+str(duplicate)+".jpg")
                duplicate += 1

                shutil.move(os.path.join(source_path, files), os.path.join(destination_path, files))
            else:
                shutil.move(os.path.join(source_path, files), os.path.join(destination_path, files))

image_download()
directory_population()
