
# DevOps Apprenticeship: Project Exercise

[![Build Status](https://travis-ci.com/sultanshaikh-devops/DevOps-Course-Starter.svg?branch=master)](https://travis-ci.com/sultanshaikh-devops/DevOps-Course-Starter)
![GitHub](https://img.shields.io/github/license/sultanshaikh-devops/DevOps-Course-Starter)
![GitHub last commit](https://img.shields.io/github/last-commit/sultanshaikh-devops/DevOps-Course-Starter)

## Module 9
---
In this application has been switch from using TRELLO to MongoDb.
For this exercise we are going to use a service called MongoDB Atlas (https://www.mongodb.com/atlas/database). This will let us create a 
MongoDB cluster that our application can use. There is a free tier, which is suitable for our 
purposes. If you choose the "I'm learning MongoDB" option at sign-up then the set-up 
instructions are very intuitive. Start the sign-up process.

## Travis CI
#### Update Travis CI variables
  * MONGODB_COLLECTIONNAME
  * MONGO_CONNECTION_STRING
  * SECRET_KEY
  * dockerPassword
  * dockerUsername
  * HEROKU_API_KEY
  * HEROKU_USERNAME

Note: 

## Module 8
---
## Travis CI
#### Set up Travis CI for your repository
Travis CI is set up to work well with GitHub but for it to work you need to enable it for any repository you want to use it for.

* Go to [`Travis-ci.com`](Travis-ci.com) and Sign in with GitHub credentials.
* Accept the Authorization of Travis CI. You’ll be redirected to GitHub.
* Click on your profile picture in the top right of your Travis Dashboard, click Settings and then the green Activate button, and select the project repository to use with Travis CI
* We now want to add a .travis.yml file which defines how to perform docker build and execute tests on Travis server.
* When we push .travis.yml to the repository, Travis server will pick this up and starts executing the instructions that are defined in the .travis.yml file.

## Heroku Deployment - Continuous Deployment
#### Step 1: Create & Configure Heroku App

First, create a new Heroku app either using the web interface or CLI. You should already have a Heroku account from this Module's workshop. If not, set one up now - it's free. Make a note of the app's name.
Once you've created an app, you'll need to provide it with the production environment variables your code needs to run. That will include your trello API credentials, and the board ID you want to use.
You can set config values via the Heroku CLI; for example, the following snippet uploads the TRELLO_API_KEY stored in your .env file:
```bash 
$ heroku config:set `cat .env | grep API_KEY`
```
Repeat the above for API_TOKEN and Board ID as well.

More information on Heroku capabilities can be found in [`https://devcenter.heroku.com/articles/container-registry-and-runtime#dockerfile-commands-and-runtime`](https://devcenter.heroku.com/articles/container-registry-and-runtime#dockerfile-commands-and-runtime)

####Step 2: Push an Image to Heroku
Heroku can't deploy images from Docker Hub directly, but instead uses its own (private) Docker registry. You need to push your image there, then tell Heroku to deploy it.
```bash
# Get the latest image from Docker Hub (built by your CI pipeline)
docker pull sultanshaikh50/todo-app-prod:latest
# Tag it for Heroku
docker tag sultanshaikh50/todo-app-prod:latest registry.heroku.com/ss-todo-app/web
# Login to Heruku Registry
echo "$HEROKU_API_KEY" | docker login --username="$HEROKU_USERNAME" --password-stdin registry.heroku.com
# Push it to Heroku registry
docker push registry.heroku.com/ss-todo-app/web
```

####Step 3: Release it to Heroku

```bash
heroku container:login
heroku container:release web --app ss-todo-app
```
#### Things to watch out for
* Note that Heroku requires your app to listen on a port defined by the $PORT environment variable in your .env file and Adjust your Dockerfile's ENTRYPOINT to execute a shell script which can read the $PORT value from your .env file.
* To authorise interaction with Heroku's API (such as heroku container:release web --app ss-todo-app ), set a HEROKU_API_KEY environment variable in Travis.

## Module 7
---
To validate Module 7 project work, follow the steps below:
  + Make a Fork out of branch
  + Ensure you have setup free account with travis CI (https://travis-ci.com/) and linked your GITHUB account.
  + Ensure you have your own personal slack account and to create required webhook
    Please review documentation here[1] to setup slack notifications for your build. 
    For Travis CLI login, please use your GitHub Token[2] i.e. travis login --github-token <Your GitHub Token> --pro 
    example: You can then use travis encrypt "<MY_DOMAIN>:<MY_TOKEN>" --add notifications.slack -r sultanshaikh-devops/DevOps-Course-Starter --pro  at the root of your project directory to add slack token to your .travis.yml file.
    [1] https://docs.travis-ci.com/user/notifications/#configuring-slack-notifications
    [2] https://github.com/settings/tokens

  + Create following environment variables from repository settings 
    ```bash
    TRELLO_API_KEY=
    SECRET_KEY=
    TRELLO_API_SECRET=
    ```
  + Good to go!


## System Requirements
---
This project uses docker to create isolated environments and manage package dependencies using poetry. To prepare your system, ensure you have an official Docker Desktop install.
[Docker Download](https://www.docker.com/products/docker-desktop) -- [for instructions](https://docs.docker.com/desktop/)

## Dependencies

  + You'll also need to clone a new `.env` file from the `.env.template` to store local configuration &nbsp;&nbsp;options. This is a one-time operation on first setup:
    ```bash
    $ cp .env.template .env  # (first time only) </mark>
    ```

  + The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY]
) variable which is used to encrypt the flask session cookie. [instruction for creating SECRET_KEY (https://flask.palletsprojects.com/en/1.1.x/config/)]

### Trello Setup
  + Logon to Trello https://trello.com/ and Create a Board.
  + Confirm, within your newly created board there should be three lists:
     a. To Do
     b. Doing
     c. Done
  + Add following variables to `.env` file.
    ```
    1. TRELLO_API_KEY={YOUR API KEY}
    2. TRELLO_API_SECRET={YOUR API SECRET} 
    3. TRELLO_BOARD_NAME={YOUR TRELLO BOARD NAME} 
    ```

---
## Running Production Docker Instance
  + Clone git repo using command
    ```bash
    $ git clone https://github.com/sultanshaikh-devops/DevOps-Course-Starter.git #for code review use the Pull Request url provided.
    ```

  + After downloading git repo, change directory to location where docker files resides (replace folder path to match yours).
    ```bash 
    $ cd C:\Work\Module_1_Project\DevOps-Course-Starter\
    ```

  + Start production build using command
    ```bash
    $ docker-compose -f docker-compose-prod.yml up -d --build
    ```

**[STOP!] Stop your production docker container instance before running development build**

## Running Development Docker Instance
  + clone git repo using command
    ```bash
    $ git clone https://github.com/sultanshaikh-devops/DevOps-Course-Starter.git  #Step not required, if you already performed this step under 'running production docker instance'
    ```
  
  + Start development build using command
    ```bash
    $ docker-compose -f docker-compose-dev.yml up -d --build #This wil start two instances 'dev' and 'uat'.
    ```
  + To access app under dev container using url http://127.0.0.1:5000/

    | ***Please note:*** UAT container runs continuous unit, integration and end-to-end tests whenever it detects a change to the source files (*.py, *.html, *.txt). To view output, open a new terminal and type
    ```bash
    $ docker logs todo-app-test --tail 50 -f
    ```

  + Useful docker commands for clean up
    ```bash
    $ docker stop todo-app-dev #to stop docker container (todo-app-test, todo-app-prod)
    $ docker rm todo-app-dev #to delete docker container (todo-app-test, todo-app-prod) 
    $ docker rmi todo-app-test:latest #to delete docker image (todo-app-dev:latest, todo-app-prod:latest)
    ```
  
---

## Running App Without VirtualBox

  + Update file poetry.toml
    ```bash 
    in-project = true
    ``` 

Once the all dependencies have been installed and configured, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

---
## Running Pytest

  + Make sure you have firefox browser install, for [Windows Guest]( https://www.mozilla.org/en-GB/firefox/download/thanks/) 
  + Run below command
    ```bash 
    $ poetry install
    ```
  + Download [geckodriver.exe](https://github.com/mozilla/geckodriver/releases) and place into root of 'DEVOPS-COURSE-STARTER' folder, 
  + To run all pytest  
    ```bash 
    $ poetry run pytest  
    ```

  + To run only unit and integration tests  
    ```bash
    $ poetry run pytest tests 
    ```

  + To run only end to end tests
    ```bash  
    $ poetry run pytest tests_e2e
    ```

---
## Running App Inside VirtualBox

  + git clone repo https://github.com/sultanshaikh-devops/DevOps-Course-Starter.git
  + Update poetry.toml
    ```bash 
    in-project = true
    ``` 
  + Install VirtualBox on your local PC https://www.virtualbox.org/wiki/Downloads.
  + Change your directory to where Vagrantfile is located. 
  + Type command below and wait until installation completes
    ```bash 
    $ vagrant up
    ``` 
  + Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.
  + Cleanup
    ```bash  
    $ vagrant destroy # destroy VM but it will be fully recreated next time vagrant up command used.)
    ```
---
## Contributors

- Sultan Shaikh <sultan.shaikh@gmx.com>

---
## License & Copyright
 (c) Sultan Shaikh, DevOps Apprentice