# DevOps Apprenticeship: Project Exercise

## System Requirements
---
This project uses docker to create isolated environments and manage package dependencies using poetry. To prepare your system, ensure you have an official Docker Desktop install.
[Docker Download](https://www.docker.com/products/docker-desktop) -- [for instructions](https://docs.docker.com/desktop/)

>## Dependencies

  + You'll also need to clone a new `.env` file from the `.env.template` to store local configuration &nbsp;&nbsp;options. This is a one-time operation on first setup:


  + <mark> $ cp .env.template .env  # (first time only) </mark>


  + The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY]
) variable which is used to encrypt the flask session cookie. [instruction for creating SECRET_KEY (https://flask.palletsprojects.com/en/1.1.x/config/)]

>### Trello Setup
1. Logon to Trello https://trello.com/ and Create a Board.
2. Confirm, within your newly created board there should be three lists:
     a. To Do
     b. Doing
     c. Done
3. Add following variables to `.env` file.
    1. TRELLO_API_KEY={YOUR API KEY}
    2. TRELLO_API_SECRET={YOUR API SECRET} 
    3. TRELLO_BOARD_NAME={YOUR TRELLO BOARD NAME}
    4. PROJECT_FOLDER={LOCATION TO PROJECT FOLDER} 

---
>## Running Production Docker Instance
  + Clone git repo using command <mark> $ git clone https://github.com/sultanshaikh-devops/DevOps-Course-Starter.git </mark>

  + After downloading git repo, change directory to location where docker files resides (replace folder path to match yours).
    <mark> $ cd C:\Work\Module_1_Project\DevOps-Course-Starter\ </mark>

  + Start production build using command <mark> $ docker-compose -f docker-compose-prod.yml up -d --build</mark>

>[STOP!] **Stop your production instance before running development instances**

>## Running Development Docker Instance
  + clone git repo using command <mark> $ git clone https://github.com/sultanshaikh-devops/DevOps-Course-Starter.git </mark> Step not required, if you already performed this step under 'running production docker instance'

  + Start development build using command <mark> $ docker-compose -f docker-compose-dev.yml up -d --build</mark> This wil start two instances 'dev' and 'uat'.
  + To access app under dev container using url http://127.0.0.1:5000/

  | ***Please note:*** UAT container runs continuous unit, integration and end-to-end tests whenever it detects a change to the source files (*.py, *.html, *.txt). To view output, open a new terminal and type <mark>docker logs todo-app-test --tail 50 -f</mark> 

  + Useful docker commands for clean up
    + docker stop todo-app-dev || docker stop todo-app-test || docker stop todo-app-prod
    + docker rm todo-app-dev || docker rm todo-app-test || docker rm todo-app-prod
    + docker rmi todo-app-test:latest || docker rmi todo-app-dev:latest || docker rmi todo-app-prod:latest
  
---

>## Running App Without VirtualBox

  + Update file poetry.toml
    change in-project to in-project = true

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

>## Running Pytest

  + Make sure you have firefox browser install, for Windows Guest https://www.mozilla.org/en-GB/firefox/download/thanks/ 
  
  + $ poetry install
  + Download geckodriver.exe and place into root of 'DEVOPS-COURSE-STARTER' folder, https://github.com/mozilla/geckodriver/releases
  + To run all pytest  
    <mark>$ poetry run pytest </mark>

  + To run only unit and integration tests  
  <mark>$poetry run pytest tests</mark> 

  + To run only end to end tests  
  <mark>$poetry run pytest tests_e2e</mark>


>## Running App Inside VirtualBox

  + git clone repo https://github.com/sultanshaikh-devops/DevOps-Course-Starter.git
  + Ensure in-project set to in-project = true inside file poetry.toml 
  + Install VirtualBox on your local PC https://www.virtualbox.org/wiki/Downloads.
  + Change your directory to where Vagrantfile is located. 
  + Type vagrant up and wait until installation completes
  + Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.
  + Type vagrant destroy (Destroys the VM. It will be fully recreated the next time you run vagrant up.)

---
## Contributors

- Sultan Shaikh <sultan.shaikh@gmx.com>

---
## License & Copyright
 (c) Sultan Shaikh, DevOps Apprentice