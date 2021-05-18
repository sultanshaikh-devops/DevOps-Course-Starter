# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

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
    run 'poetry install'
    download geckodriver.exe and place in root of 'DEVOPS-COURSE-STARTER' folder    

  to all tests same time 
    poetry run pytest

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

