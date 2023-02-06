#! /usr/bin/env python
import requests
from time import sleep
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
import urllib.request

#Base 64 String of clientid:clientsecret
base_64 = ""
#Client ID from an application from the spotify developer dashboard
client_id = ""
#The redirect uri set inside of an application from the spotify developer dashboard
redirect_uri = ""


#Spotify Authentication
def getKeyUrl():
    return f"https://accounts.spotify.com/authorize?client_id={client_id}&scope=user-read-playback-state user-read-currently-playing&response_type=code&redirect_uri={redirect_uri}"

def getAuthToken(code, returnkeyonly=bool):
    authHeader = {}
    authHeader["Authorization"] = "Basic " + base_64

    url = "https://accounts.spotify.com/api/token"
    form = {
        "code":code,
        "redirect_uri":redirect_uri,
        "grant_type":"authorization_code"
    }
    headers = {
        "Authorization":"Basic " + base_64,
        "Content-Type":"application/x-www-form-urlencoded"
    }
    req = requests.post(url=url, headers=headers, data=form)

    req_json = req.json()
    if returnkeyonly == True:
        return req_json["refresh_token"]
    else:
        return req_json

def refreshAuthToken(refresh_token):
    url = "https://accounts.spotify.com/api/token"
    form = {
        "grant_type": "refresh_token",
        "refresh_token":refresh_token
    }
    headers = {
        "Authorization":"Basic " + base_64,
        "Content-Type":"application/x-www-form-urlencoded"
    }

    res = requests.post(url=url, headers=headers, data=form)
    file = res.json()

    return file["access_token"]


#Spotify request current playback
def requestPlayback(auth_token):
    req = requests.get(
        'https://api.spotify.com/v1/me/player',
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )
    
    if req.status_code == 401:
        print("token expired")
        return False
    
    try:
        resp_json = req.json()
    except:
        return False
        
    track_id = resp_json['item']['id']
    track_name = resp_json['item']['name']
    names = []
    for i in range(0, len(resp_json['item']['artists'])):
        names.append(resp_json['item']['artists'][i]["name"])
    track_artist = ", ".join(names)
    link = resp_json['item']['external_urls']['spotify']
    album_art = resp_json["item"]["album"]["images"][2]["url"]
    playing = resp_json["is_playing"]
    track_data = {
        "id":track_id,
        "name":track_name,
        "artists":track_artist,
        "link":link,
        "art":album_art,
        "playing":playing
    }
    
    return track_data





# Configuration for matrix
options = RGBMatrixOptions()
options.rows = 64   #Must be changed for different matrix dimensions
options.cols = 64
options.chain_length = 1
options.hardware_mapping = 'adafruit-hat'  # For Adafruit HAT: 'adafruit-hat', other matricies will require different hardware-mappings.

matrix = RGBMatrix(options = options)

#Displaying images on RGB matrix.
def getImage(link, imagetype="web"):
    if imagetype == "web":
        urllib.request.urlretrieve(
        link, "image.png")

        image = Image.open("image.png")
    else:
        image = Image.open(link)

    image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)

    matrix.SetImage(image.convert('RGB'))


#Main program.
prev_track = ''
track_playing = True

print(getKeyUrl())
refresh_token = getAuthToken(code=input("Please enter Auth code.\n"), returnkeyonly=True)

while True:
    try:
        track_data = requestPlayback(refreshAuthToken(refresh_token))
    except:
        track_data = "nothing"


    if track_data == "nothing" and track_playing == True:
        print("No Song Playing")
        track_playing == False

    elif track_data["playing"] == "False" or track_data["playing"] == False:
        getImage("black.png", imagetype="local")
        prev_track = 0
        track_playing = True
            
    else:
        track_playing = True

        if track_data["name"] == prev_track:
            pass

        else:
            print(f'{track_data["name"]}, {track_data["art"]}')
            prev_track = track_data["name"]
            getImage(track_data["art"])
            
    sleep(1) # How often the progran refreshes.
