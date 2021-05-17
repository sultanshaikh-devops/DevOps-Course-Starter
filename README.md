# DevOps Apprenticeship: Project Exercise

## System Requirements

This project uses docker to create isolated environments and manage package dependencies using poetry. To prepare your system, ensure you have an official Docker Desktop install.
[Docker Download](https://www.docker.com/products/docker-desktop) [instruction for Windows OS](https://docs.docker.com/docker-for-windows/install/)

## Dependencies

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY]
) variable which is used to encrypt the flask session cookie.

## Setting up for trello.com
1. Create a Board.
2. Within your newly created board there should be three lists:
     a. To Do
     b. Doing
     c. Done
3. Add following variables to `.env` file.
    1. TRELLO_API_KEY={YOUR API KEY}
    2. TRELLO_API_SECRET={YOUR API SECRET} 
    3. TRELLO_BOARD_NAME={YOUR TRELLO BOARD NAME}

## Running Production Docker Instance
After downloading git repo, change directory to location where Dockerfile resides.
[Docker Build Comnmand](docker build --target production --tag todo-app:prod .)

For command below replace "ROOT FOLDER LOCATION OF YOUR PROJECT REPO" (example: C:\Work\Module_1_Project\DevOps-Course-Starter\)
[Docker run command] (docker run -p 5000:5000 --env-file .env --mount type=bind,source=ROOT FOLDER LOCATION OF YOUR PROJECT REPO,target=/app todo-app:prod)


## Running Development Docker Instance
After downloading git repo, change directory to location where Dockerfile resides.
[Docker Build Comnmand](docker build --target development --tag todo-app:dev .)

For command below replace "ROOT FOLDER LOCATION OF YOUR PROJECT REPO" (example: C:\Work\Module_1_Project\DevOps-Course-Starter\)
[Docker run command] (docker run -p 5000:5000 --env-file .env --mount type=bind,source=ROOT FOLDER LOCATION OF YOUR PROJECT REPO,target=/app todo-app:dev)


###################################################################################################################
## Running the App on your local machine without virtualBox

Update file poetry.toml
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

## Running Pytest
    Make sure you have firefox browser install 
    poetry install
    poetry update
    download geckodriver.exe and place in root of 'DEVOPS-COURSE-STARTER' folder    

  for running unit and integration testing 
    poetry run pytest tests

  for running end_2_end testing 
    poetry run pytest tests_e2e

## Running the App on your virtualBox

ensure poetry.toml
  in-project set to in-project = true

1. Install VirtualBox on your local PC.
2. Change your directory to where Vagrantfile is located 
3. type vagrant up and wait until installation completes
4. Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.
6. type vagrant destroy (Destroys the VM. It will be fully recreated the next time you run vagrant up.)

