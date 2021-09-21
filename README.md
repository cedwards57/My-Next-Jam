# Project 1 - Spotify API Usage

## Notes

These instructions assume use of a Linux machine (can be a VM). Procedure and commands may vary somewhat for other operating systems.

This app uses the Spotify Developer API to pull its information, Flask with Jinja to convert said information into a webpage, and Heroku to deploy the webpage onto a web URL accessible to other users.

You can view my example edition of this app at [https://project1-cedwards57.herokuapp.com/](https://project1-cedwards57.herokuapp.com/)

## Clone this Repository

1. Go to [https://github.com/new](https://github.com/new) and create a new repository. The name can be anything, but for this example, let's say it's named `spotifyapp`.
2. In your command terminal, use `cd` to go to the folder where you want to have this app's files.
3. `git clone https://github.com/csc4350-f21/project1-cedwards57.git`
4. `cd` into the newly created repository, and you should see the new files.
5. Connect this to your github repo using `git remote set-url origin https://github.com/{yourusername}/spotifyapp`. Replace {yourusername} with your username, *without* curly braces.
6. `git push origin main` to have the cloned repo appear in your personal github repo.

## Spotify Developer Account & Setup
1. If you do not already have a Spotify account, you will need to create one. A free account is fine!
2. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and log in.
3. Click **Create An App**, enter the necessary information, then click **Create**.
4. From the app's screen, you can find the Client ID and Client Secret. If you want to test your app locally, create a file called **.env** with these contents:

> export CLIENT_ID="yourclientid"<br>
> export CLIENT_SECRET="yourclientsecret"

replacing **yourclientid** and **yourclientsecret** with the corresponding information.

**NOTE: Keep your ID and Secret secure. The .env file is intentionally listed in the .gitignore file.**

5. When you fork this repository, place **.env** in the root in your own machine. This will enable Spotify's data retrieval to work if you test this outside of Heroku.

## Genius API Setup

1. If you haven't already, [create a Genius account](https://genius.com/signup) or log in.

2. Go to the [Genius API client management page](https://genius.com/api-clients).

3. Click "New API Client".

3. Click "Generate Access Token".

4. Add a variable called `GENIUS_TOKEN` in `.env` in the same manner as before, using the generated access token as the value. You don't need to worry about the Client ID or Secret here.

## Install Requirements

If you haven't already installed them, run these commands:
`pip install python-dotenv`
`pip install requests`

## Deploy to Heroku

1. Install Heroku CLI: `sudo snap install --classic heroku`
2. Create a [Heroku Account](https://signup.heroku.com/login) (it's free)
3. Log in to Heroku: `heroku login -i`
4. Create an app: `heroku create {appname}`. Replace {appname} with your desired app name, which must be unique from all other heroku URLs. You can leave it off entirely (just using `heroku create`) for an auto-generated app name.
5. Push your code to Heroku: `git push heroku main`.
6. Go to [your apps](https://dashboard.heroku.com/apps) on Heroku, select **your app**, go to **Settings**, and click **Reveal Config Vars**. Create variables called `CLIENT_ID`, `CLIENT_SECRET`, and `GENIUS_TOKEN` with the corresponding values from your spotify dev app, like in your `.env` file.
7. Run `heroku open` in the terminal to view the app.

WIP. to add:

- detail all technologies, frameworks, libraries, and APIs you used for this project, and explain how someone who forks the repository would be able to get set up on the project (installations, secret files)

## Question Responses

**A. What are at least 3 technical issues you encountered with your project? How did you fix them?**
1. For a while I couldn't get the app to appear correctly on Heroku, but it turned out I had a problem in `sptfy.py` where I was trying to access list values out of a dictionary without specifying the key.
2. I had trouble with getting Spotify to properly authenticate, but once I learned how to do the base64 authentication and convert it to usable format, it worked fine. I also had troublr where I thought for a while that the `params` items should be in `headers`, and couldn't figure out why it wasn't recognizing my given parameters until that was fixed.
3. Kept finding that my artists were turning up albums like "Indie Pop 101" or whatever, which are generalized playlists with tons of artists, not actual albums.
4. Had a problem where Genius would glitch on Heroku only, which turned out to be because I forgot to include that API key on Heroku.

**B. What are known problems (still existing), if any, with your project?**
Genius has a flaw where it rarely returns the correct song from the exact title, though this was listed in the specs as fine (although I'll probably try to fix it later anyway.) I'll likely fix this by adding more into the Genius query parameter, like writing the song's name and artist both in the query. I'll need to experiment some with it.

Additionally, I've never had a song successfully return a preview URL, regardless of market region or anything else. (As in, there's literally no link returned in the track information, even when it should be.) I'd like to work on implementing a music player instead, to circumvent this.

**C. What would you do to improve your project in the future?**
I'd probably want to fiddle more with `sptfy.py` to make it pass less redundant parameters throughout. I'd also want to display more songs at once, and add in search functionality. Maybe add a thing where you can search for an artist, then that artist gets added to a list of checkboxes, then you can use those checkboxes to choose what selection of artists you get a random song from?

I also might work on making the Genius lyrics more accurate, and if possible, pulling the lyrics out and listing them somewhere, like to the side. Additionally,
