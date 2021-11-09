terraform {
  required_version = ">= 0.12"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 2.49"
    }
  }
}

data "azurerm_resource_group" "main" {
  name = var.resource_group_name
}

resource "azurerm_app_service_plan" "main" {
  name                = "${var.prefix}-terraformed-asp"
  location            = var.location
  resource_group_name = data.azurerm_resource_group.main.name
  kind                = "Linux"
  reserved            = true
  sku {
    tier = "Basic"
    size = "B1"
  }
}


data "azurerm_cosmosdb_account" "main" {
  name                = "${var.prefix}-cosmosdb-account"
  resource_group_name = data.azurerm_resource_group.main.name
#   depends_on = [
#     azurerm_cosmosdb_account.main,
#   ]
}


resource "azurerm_app_service" "main" {
  name                = "${var.prefix}-ss-todo-app"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  app_service_plan_id = azurerm_app_service_plan.main.id
  site_config {
    app_command_line = ""
    linux_fx_version = var.linux_fx_version
  }

  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL"          = var.DOCKER_REGISTRY_SERVER_URL
    "MONGO_CONNECTION_STRING"             = "mongodb://${data.azurerm_cosmosdb_account.main.name}:${data.azurerm_cosmosdb_account.main.primary_key}@${data.azurerm_cosmosdb_account.main.name}.mongo.cosmos.azure.com:10255/DefaultDatabase?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@${data.azurerm_cosmosdb_account.main.name}@"
    "DOCKER_REGISTRY_SERVER_PASSWORD"     = var.DOCKER_REGISTRY_SERVER_PASSWORD
    "DOCKER_REGISTRY_SERVER_USERNAME"     = var.DOCKER_REGISTRY_SERVER_USERNAME
    "GITHUB_CLIENT_ID"                    = var.GITHUB_CLIENT_ID
    "GITHUB_CLIENT_SECRET"                = var.GITHUB_CLIENT_SECRET
    "MONGODB_COLLECTIONNAME"              = var.MONGODB_COLLECTIONNAME
    "SECRET_KEY"                          = var.SECRET_KEY
    "OAUTHLIB_INSECURE_TRANSPORT"         = true
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = false

  }
  lifecycle { prevent_destroy = true }
}

