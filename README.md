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

5. In your terminal, run the command `python3 -c 'import os; print(os.urandom(16))'` and add the output to `.env` with the variable name `SECRET_KEY`.

## Install Requirements

If you haven't already installed them, run these commands:
<br>`pip install python-dotenv`
<br>`pip install requests`
<br>`sudo apt install postgresql`
<br>`pip install psycopg2-binary`
<br>`pip install Flask-SQLAlchemy==2.1`

## Deploy to Heroku

1. Install Heroku CLI: `sudo snap install --classic heroku`
2. Create a [Heroku Account](https://signup.heroku.com/login) (it's free)
3. Log in to Heroku: `heroku login -i`
4. Create an app: `heroku create {appname}`. Replace {appname} with your desired app name, which must be unique from all other heroku URLs. You can leave it off entirely (just using `heroku create`) for an auto-generated app name.
5. Create a database for your app to use: `heroku addons:create heroku-postgresql:hobby-dev`
6. Push your code to Heroku: `git push heroku main`.
7. Go to [your apps](https://dashboard.heroku.com/apps) on Heroku, select **your app**, go to **Settings**, and click **Reveal Config Vars**. Create variables called `CLIENT_ID`, `CLIENT_SECRET`, `GENIUS_TOKEN`, and `SECRET_KEY` with the corresponding values from your spotify dev app, like in your `.env` file.
8. In the same place, find the `DATABASE_URL` varable. Copy it into a new variable called `DATABASE_URL_QL`, and change the `postgres://` at the start to `postgresql://`. Add `DATABASE_URL_QL` to your `.env` file as well.
9. Run `heroku open` in the terminal to view the app.

WIP. to add:

- detail all technologies, frameworks, libraries, and APIs you used for this project, and explain how someone who forks the repository would be able to get set up on the project (installations, secret files)

## Question Responses

**A. What are at least 3 technical issues you encountered with your project? How did you fix them?**
1. For a while, I couldn't get the database commands to work at all. Some of this was syntax problems, but I was also missing some expected requirements, like having a `get_id()` function in my UserLogin class.
2. For the life of me I couldn't get the database additions to appear in the database, until it turned out I was just not establishing context (the stuff around the `db.create_all()` line).
3. I had problems with circular imports for a while. I solved this by establishing `db` inside the `models.py` file, and importing that into `app.py` (instead of the other way around), so that it'd be going in the same direction as the other imports from `models.py`.
4. No songs were returning preview URLs, no matter what I did. I solved this by just embedding Spotify's song player instead.
5. Genius wasn't returning the correct songs a lot of the time; I updated its function to include the artist name along with the title in the search.

**B. What are known problems (still existing), if any, with your project?**
I'd like to make the front-end design a little more elegant, and divide up the modules on the back-end a little more.

There's an error I've seen crop up once with parsing the initial JSON (the Spotify Auth one, I think?), but I haven't been able to replicate it, so I'm going to leave it. If it comes up again, I'll see if I can do a fix.

Genius... still doesn't actually return the correct song a lot of the time. I have no idea what's going on in the backend for its Search API to return results with not even a single word in common with the song that was searched for. But it does return the correct song more often than it used to!

**C. What would you do to improve your project in the future?**
I'd like to create functionality where the list of artists has checkboxes, and you can click the checkbox by certain artists in order to only include songs from those artists in the shuffle.

I'd also like to add in a selection of the lyrics from the given random song, should the Genius API allow it.
