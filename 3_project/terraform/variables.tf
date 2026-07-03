variable "project_name" {
  description = "Short name used for cloud resources and tags."
  type        = string
  default     = "cloudops-lab"

  validation {
    condition     = length(trimspace(var.project_name)) > 0
    error_message = "project_name must not be empty."
  }
}

variable "environment" {
  description = "Environment name added to resource names and tags."
  type        = string
  default     = "lab"
}

variable "linux_image" {
  description = "Provider-specific Linux image name or ID to use later."
  type        = string
  default     = "ubuntu-24.04"
}

variable "vm_size" {
  description = "Provider-specific size for a small Linux VM."
  type        = string
  default     = "small"
}

variable "ssh_public_key_path" {
  description = "Path to a local SSH public key. This skeleton records the path but does not read the file."
  type        = string
  default     = "~/.ssh/id_ed25519.pub"
}

variable "firewall_rules" {
  description = "Inbound TCP rules intended for the future cloud firewall. Replace example management CIDRs before deployment."
  type = list(object({
    port         = number
    description  = string
    source_cidrs = list(string)
  }))

  default = [
    {
      port         = 22
      description  = "SSH administration"
      source_cidrs = ["203.0.113.10/32"]
    },
    {
      port         = 80
      description  = "HTTP"
      source_cidrs = ["0.0.0.0/0"]
    },
    {
      port         = 443
      description  = "HTTPS"
      source_cidrs = ["0.0.0.0/0"]
    },
    {
      port         = 9090
      description  = "Prometheus UI"
      source_cidrs = ["203.0.113.10/32"]
    },
    {
      port         = 3000
      description  = "Grafana UI"
      source_cidrs = ["203.0.113.10/32"]
    }
  ]

  validation {
    condition = alltrue([
      for rule in var.firewall_rules : rule.port >= 1 && rule.port <= 65535
    ])
    error_message = "Every firewall port must be between 1 and 65535."
  }

  validation {
    condition = alltrue([
      for required_port in [22, 80, 443, 9090, 3000] :
      contains([for rule in var.firewall_rules : rule.port], required_port)
    ])
    error_message = "firewall_rules must include ports 22, 80, 443, 9090, and 3000."
  }
}

variable "tags" {
  description = "Additional project tags to apply to future cloud resources."
  type        = map(string)
  default = {
    managed_by = "terraform"
    purpose    = "portfolio"
  }
}
