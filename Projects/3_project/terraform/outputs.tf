output "project_name" {
  description = "Name used to identify this infrastructure project."
  value       = var.project_name
}

output "vm_plan" {
  description = "Credential-free description of the intended Linux VM."
  value       = terraform_data.infrastructure_plan.output.vm
}

output "firewall_rules" {
  description = "Inbound TCP rules intended for the future cloud firewall."
  value       = terraform_data.infrastructure_plan.output.firewall.inbound_rules
}

output "public_ip" {
  description = "Placeholder public IP. Replace this value with the selected provider resource attribute."
  value       = terraform_data.infrastructure_plan.output.vm.public_ip.address
}

output "project_tags" {
  description = "Names and tags intended for all provider resources."
  value       = terraform_data.infrastructure_plan.output.tags
}
