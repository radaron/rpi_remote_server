ACTIVATE = . .venv/bin/activate

.venv:
	python3.9 -m venv .venv

virtualenv: .venv

pip: virtualenv
	$(ACTIVATE) && pip install --upgrade pip pip-tools

reqs-prod: pip
	@$(ACTIVATE) && pip install -r requirements.txt

reqs-dev: pip
	@$(ACTIVATE) && pip install -r requirements-dev.txt

quickstart: virtualenv reqs-dev

lint: reqs-dev
	@$(ACTIVATE) && pylint *.py

lock: pip
	@$(ACTIVATE) && pip-compile --generate-hashes --no-emit-index-url --output-file=requirements.txt \
		--resolver=backtracking pyproject.toml
	@$(ACTIVATE) && pip-compile --generate-hashes --no-emit-index-url --output-file=requirements-dev.txt \
		--resolver=backtracking --extra dev pyproject.toml

add-user:
	@$(ACTIVATE) && python -m tools.add_user

forward:
	@$(ACTIVATE) && python -m tools.forward --name $(NAME) --port $(PORT) 

generate-secret:
	@$(ACTIVATE) && python -m tools.generate_secret

start-backend:
	@$(ACTIVATE) && python -m main
