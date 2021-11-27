.PHONY: requirements run

requirements: ## install local environment requirements
	pip install -qr requirements.txt --exists-action w

run: ## Runs the mapping script every 5 mints.
	python3 mapping/main.py