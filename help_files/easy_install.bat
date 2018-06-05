cd ..
python -m venv env
call env\Scripts\activate
pip install -r requirements.txt
cd data_science_app
md migrations
cd migrations
REM. > __init__.py
cd ..\..
python manage.py makemigrations
python manage.py migrate