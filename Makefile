include .env

VAGR_SSH := vagrant ssh
VM_MAKEFILE_PATH=/vagrant

help:
	@echo "Run one of these targets"
	@echo "  deploy_plugins_to_dev    "
	@echo "  deploy_hooks_to_dev      "

deploy_plugins_to_dev:
	$(VAGR_SSH) -c "sudo /vagrant/deploy_plugins.sh"

deploy_hooks_to_dev:
	$(VAGR_SSH) -c "sudo /vagrant/deploy_hooks.sh"
