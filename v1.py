# https://imgur.com/gallery/aPjMhcR

# scrape name from link to get name for new directory [x]
# create directory in the same place code is run [x]
# allow path to specified if not the current one [x]
# automate downloading of images on a page []

from bs4 import BeautifulSoup
import requests
import os

# get url information using requests using http requests
request = requests.get("https://imgur.com/gallery/OToFZd4")

page = BeautifulSoup(request.text, features="html.parser")
# title created by formatting and removing all spaces
title = " ".join(page.title.text.split())

directory_choice = input("Would you like to use the current directory? Y/N")

if directory_choice.lower == "y":
    new_directory = os.getcwd() + "/" + title
    try:
        os.mkdir(new_directory)
    except OSError:
        print("unable to create directory with web page's name")
    else:
        print("success")
elif directory_choice.lower == "n":
    path = input("Please input a new absolute path to the directory you want the folder created in.")
    new_directory = path + "/" + title
    try:
        os.mkdir(new_directory)
    except OSError:
        print("unable to create directory with web page's name")
    else:
        print("success")
else:
    print("Please input a valid choice")

