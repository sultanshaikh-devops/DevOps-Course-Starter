#!/bin/bash
# docker pull $dockerUsername/todo-app-prod:latest
# docker tag $dockerUsername/todo-app-prod:latest registry.heroku.com/ss-todo-app/web
# echo "$HEROKU_API_KEY" | docker login --username="$HEROKU_USERNAME" --password-stdin registry.heroku.com
# docker push registry.heroku.com/ss-todo-app/web
# heroku container:login
# heroku container:release web --app ss-todo-app
# curl -dH -X POST "$(terraform output -raw cd_webhook)"

terraform init
terraform apply -var "prefix=prod" -var "location=uksouth" -var "resource_group_name=OpenCohort1_SultanShaikh_ProjectExercise" -var "DOCKER_REGISTRY_SERVER_USERNAME='$dockerUsername'" -var "DOCKER_REGISTRY_SERVER_PASSWORD='$dockerPassword'" -var "GITHUB_CLIENT_ID=fe94565315d9adc854ab" -var "GITHUB_CLIENT_SECRET=efb0157b6eeacc62488467835f4d3c95995c4f3b" -var "MONGODB_COLLECTIONNAME='$MONGODB_COLLECTIONNAME'" -var "SECRET_KEY='$SECRET_KEY'" -auto-approve
export MONGO_CONNECTION_STRING="$(terraform output -raw cosmos_connection_string)"
echo "$MONGO_CONNECTION_STRING"
docker run -e MONGO_CONNECTION_STRING -e MONGODB_COLLECTIONNAME -e SECRET_KEY -e GITHUB_CLIENT_ID -e GITHUB_CLIENT_SECRET --entrypoint poetry todo-app-test:latest run pytest tests_e2e
