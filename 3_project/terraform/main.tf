locals {
  resource_name = "${var.project_name}-${var.environment}"

  project_tags = merge(var.tags, {
    project     = var.project_name
    environment = var.environment
  })
}

# This built-in resource records the intended infrastructure without contacting
# a cloud API. Replace it with provider-specific VM and firewall resources when
# selecting AWS, DigitalOcean, or Hetzner.
resource "terraform_data" "infrastructure_plan" {
  input = {
    vm = {
      count            = 1
      name             = "${local.resource_name}-vm"
      operating_system = var.linux_image
      size             = var.vm_size

      ssh = {
        enabled         = true
        public_key_path = var.ssh_public_key_path
      }

      public_ip = {
        requested = true
        address   = null
      }
    }

    firewall = {
      name = "${local.resource_name}-firewall"
      inbound_rules = [
        for rule in var.firewall_rules : merge(rule, {
          protocol = "tcp"
        })
      ]
    }

    tags = local.project_tags
  }
}
