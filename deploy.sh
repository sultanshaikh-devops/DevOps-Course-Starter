#!/bin/bash
docker pull $dockerUsername/todo-app-prod:latest
docker tag $dockerUsername/todo-app-prod:latest registry.heroku.com/ss-todo-app/web
echo "$HEROKU_API_KEY" | docker login --username="$HEROKU_USERNAME" --password-stdin registry.heroku.com
docker push registry.heroku.com/ss-todo-app/web
heroku container:login
heroku container:release web --app ss-todo-app

#e1f0ff8c-bbea-4cc3-bc63-3e978ec35cda
#sultan.shaikh@hotmail.co.uk