VENV=.venv

.PHONY: run venv

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

venv:
	python -m venv $(VENV)
	$(VENV)\Scripts\pip.exe install -r requirements.txt
