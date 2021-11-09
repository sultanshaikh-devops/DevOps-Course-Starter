variable "prefix" {
  type        = string
  description = "The prefix used for all resources in this environment"
}

variable "location" {
  type        = string
  description = "The Azure location where all resources in this  deployment should be created"
}

# variable "prevent_destroy" {
#   type        = bool
#   description = "Should cosmodb life cycle to prevent getting recreated every time terraform runs"
#   default = false
# }

variable "DOCKER_REGISTRY_SERVER_URL" {
  type        = string
  description = "The docker url"
}

variable "DOCKER_REGISTRY_SERVER_PASSWORD" {
  type        = string
  description = "docker password"
  sensitive   = true
}

variable "DOCKER_REGISTRY_SERVER_USERNAME" {
  type        = string
  description = "Docker user name"
  sensitive   = true
}

variable "GITHUB_CLIENT_ID" {
  type        = string
  description = "Github Client ID"
  sensitive   = true
}
variable "GITHUB_CLIENT_SECRET" {
  type        = string
  description = "Github client secret"
  sensitive   = true
}

variable "MONGODB_COLLECTIONNAME" {
  type        = string
  description = "Mongo collection name"
}

variable "SECRET_KEY" {
  type        = string
  description = "Flask application secret key"
  sensitive   = true

}



# variable "storage" {
#   type = object({
#     storage_account_name = string
#     container_name       = string
#     key                  = string

#   })

#   default = {
#     storage_account_name = "tfstate007ss"
#     container_name       = "tfstate007ss"
#     key                  = "terraform.tfstate"
#   }

# }

# variable "storageaccount" {
#   description = "The Azure storage accout name used to store tfstate"
#   default     = "tfstate007ss"
# }


# variable "linux_fx_version" {
#   description = "Docker image to pull"
#   default     = "DOCKER|sultanshaikh50/todo-app-prod:latest"
# }

# variable "appsettings" {
#   type = object({
#     DOCKER_REGISTRY_SERVER_PASSWORD = string
#     DOCKER_REGISTRY_SERVER_URL      = string
#     DOCKER_REGISTRY_SERVER_USERNAME = string
#     GITHUB_CLIENT_ID                = string
#     GITHUB_CLIENT_SECRET            = string
#     MONGODB_COLLECTIONNAME          = string
#     SECRET_KEY                      = string
#     description                     = string

#   })

#   default = {
#     description                     = "holds web settings for azure web app"
#     DOCKER_REGISTRY_SERVER_URL      = "https://index.docker.io/v1"
#     DOCKER_REGISTRY_SERVER_PASSWORD = ""
#     DOCKER_REGISTRY_SERVER_USERNAME = ""
#     GITHUB_CLIENT_ID                = ""
#     GITHUB_CLIENT_SECRET            = ""
#     MONGODB_COLLECTIONNAME          = ""
#     SECRET_KEY                      = ""
#   }

#   sensitive = true
# }


