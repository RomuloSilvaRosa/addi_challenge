
# ifndef VERBOSE
# MAKEFLAGS += --no-print-directory -s
# endif
ECR_NAME=orchestrator/lambda
FUNCTION_NAME=addi-challenge-orchestrator

lint: ## Remove unused imports and variables/Format using black
	@echo "---- Refactorying ----"
	@autoflake --remove-all-unused-imports --remove-duplicate-keys --remove-unused-variables --in-place --exclude globs -r src/
	@python3 -m black *.py
	@python3 -m isort src/
	@python3 -m pyflakes src/

# .PHONY: clean
clean: ## Delete All pyc and pycache files
	@echo "-- [$(NAME)] clean --"
	@find . -name '*.pyc' -delete
	@find . -name '*__pycache__*' -delete

.PHONY: test
test: ## Run tests
	@python3 -m unittest discover -v tests

.PHONY: filter_test
filter_test: ## PATTERN=<any_pattern> Run tests with filtering
	@echo Running test w pattern ${PATTERN}
	@python3 -m unittest -k ${PATTERN} -v

coverage: ## Run tests opening html coverage
	@coverage run --source=. -m unittest discover -v tests
	@coverage html --include=src/*
	@firefox htmlcov/index.html

dev: ## Install dev needed packages
	@pip3 install -r requirements.txt --upgrade
	@pip3 install -r requirements-dev.txt --upgrade

docker_build: docker_init
	@echo Building docker $(shell basename $(CURDIR))
	@docker build -t $(shell basename $(CURDIR)) -t ${ECR_URL}:${DOCKER_IMAGE_TAG} -t ${ECR_URL}:latest .

docker_run:  ## Run application in dev mode
	@echo Starting application $(shell basename $(CURDIR))
	@docker run --name $(shell basename $(CURDIR)) -it --rm -v $(pwd)/zippable:/var/task/zippable -p  9000:8080 

docker_init:
	$(eval export aws_account_id=$(shell aws --output text --query Account sts get-caller-identity))
	$(eval export ECR_URL=$(shell echo ${aws_account_id}.dkr.ecr.us-east-1.amazonaws.com/${ECR_NAME}))
	$(eval export DOCKER_IMAGE_TAG=$(shell git rev-parse HEAD))


docker_push: docker_init
	
	aws ecr get-login-password | docker login --username AWS --password-stdin "$(ECR_URL)"
	@docker push ${ECR_URL}:${DOCKER_IMAGE_TAG}
	@docker push ${ECR_URL}:latest

deploy: docker_build docker_push update_function

update_function: docker_init
	@aws lambda update-function-code --function-name ${FUNCTION_NAME} --image-uri ${ECR_URL}:${DOCKER_IMAGE_TAG} > /dev/null 2>&1

help: ## Show some help
	@echo
	@echo '  Usage:'
	@echo '    make <target>'
	@echo
	@echo '  Targets:'
	@egrep '^(.+)\:\ ##\ (.+)' ${MAKEFILE_LIST} | column -t -c 2 -s ':#'
	@echo
