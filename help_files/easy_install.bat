cd ..
python -m venv env
call env\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate