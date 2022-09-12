provider "aws" {
  region = "us-east-1"
}

terraform {
  backend "s3" {
    bucket = "addi-challenge-tf-states"
    key    = "states/model_feature_evaluation_store/terraform.tfstate"
    region = "sa-east-1"
  }
}