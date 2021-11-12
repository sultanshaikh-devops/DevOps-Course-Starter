import json, os, requests
 
from flask import Flask, redirect, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
    UserMixin,
)
from oauthlib.oauth2 import WebApplicationClient


client_id = "ed0279ca8d6b0e1bb25f"
client_secret = "3086ee2da1aeff99e63d69f9b6b51e3bba71785d"
#base_url="https://api.github.com"
authorization_url="https://github.com/login/oauth/authorize"
#token_url="https://github.com/login/oauth/access_token"


app = Flask(__name__)
app.secret_key = os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)

class UserToLogin (UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))

client = WebApplicationClient(client_id)

@login_manager.user_loader
def load_user(user_id):
    return UserToLogin(user_id)


@app.route("/")
def index():
    if current_user.is_authenticated:
        return "You are logged in as {}.".format(current_user.id), 200
    else:
        return redirect(url_for('login'))


@app.route("/login")
def login():
    # Find out what URL to hit for Google login
 
    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_url,
        redirect_uri=request.base_url + "/callback",
        scope=None,
    )
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
 
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user

    token_endpoint = "https://github.com/login/oauth/access_token"
 
    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )

    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(client_id, client_secret),
    )

    json_data = token_response.content.decode('utf8').replace("'", '"')
    
    # Parse the tokens!
    client.parse_request_body_response(json_data)
 
    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = "https://api.github.com/user"
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    if userinfo_response.ok:
        account_info_json = userinfo_response.json()
        currentUserName = str(account_info_json['login'])
    #if not current_user.get_id:                
        login_user(UserToLogin(currentUserName))
        print(currentUserName)

 
    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    # if userinfo_response.json().get("email_verified"):
    #     unique_id = userinfo_response.json()["sub"]
    #     users_email = userinfo_response.json()["email"]
    #     picture = userinfo_response.json()["picture"]
    #     users_name = userinfo_response.json()["given_name"]
    # else:
    #     return "User email not available or not verified by Google.", 400
 
    # # Create a user in our db with the information provided
    # # by Google
    # user = User(
    #     id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    # )
 
    # # Doesn't exist? Add to database
    # if not User.get(unique_id):
    #     User.create(unique_id, users_name, users_email, picture)
 
    # # Begin user session by logging the user in
    # login_user(user)
 
    # Send user back to homepage
    return redirect(url_for('index'))
 
 
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
 
 



if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

  
    app.run(debug=True)