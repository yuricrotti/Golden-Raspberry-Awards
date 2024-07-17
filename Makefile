# Variáveis
PYTHON = python3
PIP = pip3

# Comandos
install:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) main.py

test:
    # Teste all files test_*.py
	$(PYTHON) -m pytest -vv tests/ .
	
lint:
	pylint --disable=R,C *.py

format:
	black main.py
	black database/*.py
	black tests/*.py
	black schemas/*.py
	black repositories/*.py
	black models/*.py 


clean:
	rm -rf __pycache__ *.pyc

.PHONY: install run test lint format clean