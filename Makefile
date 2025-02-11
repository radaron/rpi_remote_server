ACTIVATE = . .venv/bin/activate

.venv:
	python3.9 -m venv .venv

virtualenv: .venv

pip: virtualenv
	@$(ACTIVATE) && pip install --upgrade pip pip-tools

reqs-prod: pip
	@$(ACTIVATE) && pip install --no-deps -r requirements.txt

reqs-dev: pip
	@$(ACTIVATE) && pip install --no-deps -r requirements-dev.txt

install: virtualenv reqs-prod

install-dev: virtualenv reqs-dev install-fe

install-fe:
	cd frontend && pnpm install

lint: reqs-dev
	@$(ACTIVATE) && PYTHONPATH=. pylint rpi_remote_server

lock: pip
	@$(ACTIVATE) && pip-compile --upgrade --generate-hashes --no-emit-index-url --output-file=requirements.txt \
		--resolver=backtracking --strip-extras pyproject.toml
	@$(ACTIVATE) && pip-compile --upgrade --generate-hashes --no-emit-index-url --output-file=requirements-dev.txt \
		--resolver=backtracking --extra dev --strip-extras pyproject.toml

build-frontend:
	cd frontend && pnpm build
	rm -rf rpi_remote_server/templates rpi_remote_server/static
	mkdir -p rpi_remote_server/templates rpi_remote_server/static
	cp frontend/build/index.html rpi_remote_server/templates/index.html
	cp -r frontend/build/static/* rpi_remote_server/static/.
	sed -i'.bak' -e 's/\/static/\/static/g' rpi_remote_server/templates/index.html
	sed -i'.bak' -e 's/\/favicon.ico/\/favicon.ico/g' rpi_remote_server/templates/index.html

docker-compose: build-frontend
	docker compose up --build
