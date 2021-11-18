terraform {
  backend "azurerm" {
    resource_group_name  = "OpenCohort1_SultanShaikh_ProjectExercise"
    storage_account_name = "tfstate007ss"
    container_name       = "tfstate007ss"
    key                  = "terraform.tfstate"
  }
}