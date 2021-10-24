python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python preparing/preprocessing.py
python preparing/creating_isohrones.py
python preparing/parsing_cian.py