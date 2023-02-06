# SpotifyAlbumArtDisplay
Display the currently playing track from Spotify on an Raspberry Pi LED Matrix.

This project does not utilise the spotipy library, instead it sends HTTP requests to the Spotify API directly.

To start you must input to the python program the following, (all of which can be obtained from --> https://developer.spotify.com/dashboard/applications ):
  Your Client ID
  Your Client ID and Client Secret, seperated with a : which has been base64 encoded, which can be done here --> https://www.base64encode.org/
  Your Redirect URI
  
The matrix dimensions and type will also need to be set up for your specific model.

When the program is run, the program will output a url to visit. 
This url will ask you to sign in and authorize your Spotify Applcation for access to your account.
It will then redirect you to the set Redirect URI, but inside of the URL query there will be ?code= which will need to be copied after the = sign and pasted into the terminal.

Once done, the program should run forever and be able to display any album art when a song is playing on Spotify.
