variable "prefix" {
  description = "The prefix used for all resources in this environment"
  default     = "sstf"
}

variable "location" {
  description = "The Azure location where all resources in this  deployment should be created"
  default     = "uksouth"
}

variable "resource" {
  description = "The Azure resource name where all resources in this deployment should be created"
  default     = "OpenCohort1_SultanShaikh_ProjectExercise"
}

variable "storage" {
  type = object({
    storage_account_name = string
    container_name       = string
    key                  = string

  })

  default = {
    storage_account_name = "tfstate007ss"
    container_name       = "tfstate007ss"
    key                  = "terraform.tfstate"
  }

}



variable "storageaccount" {
  description = "The Azure storage accout name used to store tfstate"
  default     = "tfstate007ss"
}


variable "linux_fx_version" {
  description = "Docker image to pull"
  default     = "DOCKER|sultanshaikh50/todo-app-prod:latest"
}

variable "appsettings" {
  type = object({
    DOCKER_REGISTRY_SERVER_PASSWORD = string
    DOCKER_REGISTRY_SERVER_URL      = string
    DOCKER_REGISTRY_SERVER_USERNAME = string
    GITHUB_CLIENT_ID                = string
    GITHUB_CLIENT_SECRET            = string
    MONGODB_COLLECTIONNAME          = string
    SECRET_KEY                      = string
    description                     = string

  })

  default = {
    description                     = "holds web settings for azure web app"
    DOCKER_REGISTRY_SERVER_URL      = "https://index.docker.io/v1"
    DOCKER_REGISTRY_SERVER_PASSWORD = "Farzana@1982"
    DOCKER_REGISTRY_SERVER_USERNAME = "sultanshaikh50"
    GITHUB_CLIENT_ID                = "e13109163ea99f547b55"
    GITHUB_CLIENT_SECRET            = "0014e01ba4f6cc4f40d8b0db67bb3692b8004d9e"
    MONGODB_COLLECTIONNAME          = "lists"
    SECRET_KEY                      = "P@ssword2018"
  }

  sensitive = true
}


