terraform {
  #   required_version = ">= 1.0.0"

  required_providers {
    kind = {
      source  = "tehcyx/kind"
      version = "0.0.12"
    }

    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "2.10.0"
    }

    helm = {
      source  = "hashicorp/helm"
      version = "2.5.1"
    }

    null = {
      source  = "hashicorp/null"
      version = "3.1.1"
    }
  }
}
