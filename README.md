# My Next Jam

You can view my live edition of this app at [https://favartists.herokuapp.com/](https://favartists.herokuapp.com/)

The following are instructions to implement this app for yourself.

## Notes

These instructions assume use of a Linux machine (can be a VM or WSL distribution). Procedure and commands may vary somewhat for other operating systems.

This app uses the Spotify Developer API to pull its information, Flask with Jinja to convert said information into a webpage, and Heroku to deploy the webpage onto a web URL accessible to other users.

## Clone this Repository

1. Go to [https://github.com/new](https://github.com/new) and create a new repository. The name can be anything, but for this example, let's say it's named `musicapp`.
2. In your command terminal, use `cd` to go to the folder where you want to have this app's files.
3. `git clone https://github.com/cedwards57/favartists.git`
4. `cd` into the newly created repository, and you should see the new files.
5. Connect this to your github repo using `git remote set-url origin https://github.com/{yourusername}/musicapp`. Replace {yourusername} with your username, *without* curly braces.
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
4. Click "Generate Access Token".
5. Add a variable called `GENIUS_TOKEN` in `.env` in the same manner as before, using the generated access token as the value. You don't need to worry about the Client ID or Secret here.
6. In your terminal, run the command `python3 -c 'import os; print(os.urandom(16))'` and add the output to `.env` with the variable name `SECRET_KEY`.

## Install Requirements

If you haven't already installed everything in the requirements.txt, run `pip install -r requirements.txt`

## Deploy to Heroku

1. Install Heroku CLI: `sudo snap install --classic heroku`
2. Create a [Heroku Account](https://signup.heroku.com/login) (it's free)
3. Log in to Heroku: `heroku login -i`
4. Create an app: `heroku create {appname}`. Replace {appname} with your desired app name, which must be unique from all other heroku URLs. You can leave it off entirely (just using `heroku create`) for an auto-generated app name.
5. Create a database for your app to use: `heroku addons:create heroku-postgresql:hobby-dev`
6. Push your code to Heroku: `git push heroku main`.
7. Go to [your apps](https://dashboard.heroku.com/apps) on Heroku, select **your app**, go to **Settings**, and click **Reveal Config Vars**. Create variables called `CLIENT_ID`, `CLIENT_SECRET`, `GENIUS_TOKEN`, and `SECRET_KEY` with the corresponding values from your spotify dev app, like in your `.env` file.
8. In the same place, find the `DATABASE_URL` varable. Copy it into a new variable called `DATABASE_URL_QL`, and change the `postgres://` at the start to `postgresql://`. Add `DATABASE_URL_QL` to your `.env` file as well, for local testing.
9. Run `heroku open` in the terminal to view the app.