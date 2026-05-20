.PHONY: run test dashboard install

install:
	pip install -r requirements.txt

run:
	python run_pipeline.py

test:
	pytest tests/

dashboard:
	cd dashboard && streamlit run app.py