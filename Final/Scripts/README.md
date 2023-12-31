# Credentials

- Please make sure to rename the variables according to the functions as needed for your code to work.

## Spotify Credentials
- id = "23a48114b46d41a99f93984d81c98c89"
- sec = "96e97ed005f44c34a4d078637f4d1ca7"

## Genius Credentials
- genius = "GsPk-0yhPoS9a8V43pLoZg3_ccW4YLgOHa7zVHGquJBtiJIWOtjxBLc8dAyvTfXJ"

# Condensed Installation Procedures
Detailed information can be found in our Documentation PDF.
1. git clone https://github.com/Henesys/CS410FinalProject.git
2. cd CS410FinalProject/Final/Scripts
3. pip3 install -r requirements.txt
4. python3 -m spacy download en_core_web_md
5. Create credentials.py and place the credentials shown above into the document. Rename 'id', 'sec', and 'genius' as shown in our presentation video.** Timestamp: Software Usage Tutorial Presentation 2:07

6. python3 dash_app.py

## List of Artists
Below are some artists that we've pre-run from the API to give faster results.
- Taylor Swift
- Lady Gaga
- Justin Bieber
- Harry Styles
- Kanye West

You may search for other artists but API limitations may increase run-time significantly.
Please make sure the spelling of the artist name is correct, or you may get default images.
More detailed limitations notes in Documentation.


### Other

**If the provided credentials do not work, to create your own:
- [Spotify](https://developer.spotify.com/dashboard): Create an account on the Spotify Link. Click on “Create app” and fill in the “Website” and “Redirect URI” fields as http://127.0.0.1:5000. Any app name and description is fine. Check “Web API” before saving. Go to settings for your new App. From there, you should be able to see your new "id" and "sec" respectively.
- [Genius](http://genius.com/api-clients): Create an account on the Genius link. Go to New API Client and fill in the URL fields as http://127.0.0.1:5000. (App Name/Icon URL can be anything.) Click on Generate Access Token to get your "genius" variable.