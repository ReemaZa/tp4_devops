terraform {
  required_providers {
    kubernetes = {
      source = "hashicorp/kubernetes"
    }
  }
}

provider "kubernetes" {
  config_path = "/root/.kube/config"
  insecure    = true # Pour ignorer l'erreur TLS qu'on a vue
}

resource "kubernetes_namespace" "flask_ns" {
  metadata {
    name = "flask-prod"
  }
}