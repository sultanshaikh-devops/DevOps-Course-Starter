variable "location" {
  type        = string
  description = "The Azure location where all resources in this  deployment should be created"
}

variable "LOGIN_DISABLED" {
  type        = bool
  description = "The Azure location where all resources in this  deployment should be created"
  default     = false
}
variable "DOCKER_REGISTRY_SERVER_URL" {
  type        = string
  description = "The docker url"
  default     = "https://index.docker.io/v1"
}

variable "DOCKER_REGISTRY_SERVER_PASSWORD" {
  type        = string
  description = "docker password"
  sensitive   = true
}

variable "LOG_LEVEL" {
  type        = string
  description = "Set logging level"
  default     = "ERROR"
  sensitive   = false
}

variable "LOGGLY_TOKEN" {
  type        = string
  description = "External logging api key"
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

variable "MONGODB_COLLECTION_NAME" {
  type        = string
  description = "Mongo collection name"
}

variable "SECRET_KEY" {
  type        = string
  description = "Flask application secret key"
  sensitive   = true

}

variable "linux_fx_version" {
  description = "Docker image to pull"
  default     = "DOCKER|sultanshaikh50/todo-app-prod:latest"
}

variable "RESOURCE_GROUP_NAME" {
  type        = string
  description = "The Azure resource name where all resources in this deployment should be created"

}

