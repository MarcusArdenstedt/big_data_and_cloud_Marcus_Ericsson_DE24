terraform {
  backend "azurerm" {
    resource_group_name = "tfstates"
    storage_account_name = "tfstatescourse15"
    container_name = "tfstate-python-deploy"
    key = "dev.terraform.tfstate" 
  }
}