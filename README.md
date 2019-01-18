# Cap-2-Drive

Screenshots saved to Google Drive.

The Python program uses a keyboard hook and uploads a screenshot to Google Drive every time the Print Screen key is pressed. Screenshots are saved in a folder called Cap-to-Drive and are named after the current date in YY-MM-DD format.

# Notes

Currently the project requires every user to create a [Google Cloud Project](https://console.cloud.google.com/projectcreate). After that is done, go [here](https://console.cloud.google.com/apis/credentials/wizard?api=drive.googleapis.com) and Select "Google Drive API" for the first dropdown, "Web Browser" for the second, and "User data" for the radio button option.
Give the client a valid name. Set the origins to "http://localhost:8080" and the redirect URI to "http://localhost:8080/". Download the credentials, move them into the same directory as the python script and rename them to "client_secrets.json".

If these libraries aren't already installed, it also requires pillow, pydrive and pyhook (get the [cp27 wheel](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyhook)).
