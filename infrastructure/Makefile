
# ifndef VERBOSE
# MAKEFLAGS += --no-print-directory -s
# endif

clean:
	@sudo rm -r .terraform*

init:
	@terraform init

apply: init
	@terraform apply -auto-approve
destroy: init
	@terraform destroy -auto-approve

plan: init
	@terraform plan -auto-approve
help: ## Show some help
	@echo
	@echo '  Usage:'
	@echo '    make <target>'
	@echo
	@echo '  Targets:'
	@egrep '^(.+)\:\ ##\ (.+)' ${MAKEFILE_LIST} | column -t -c 2 -s ':#'
	@echo
