
.venv:
	virtualenv .venv

install_deps: .venv
	pip install -r requirements.txt

test:
	export PYTHONPATH="." && pytest ./tests

clean:
	rm -rf .venv

.PHONY: test install_deps clean

