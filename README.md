web_data_science
Порядок установки: 
git clone https://github.com/DmitriyKonovalov/web_data_science;
python -m venv env;
call env\Scripts\activate;
pip install -r requirements.txt;
python manage.py makemigrations;
python manage.py migrate;
python manage.py createsuperuser 
... Указываем <username, password, email>;
python manage.py runserver

Сервер запущен!


Приложение Web Data Science:

Авторизация по username, password;
Регистрация нового пользователя;
Создание анализов, изменение, удаление;
Выполнение анализа, скачивание;
Приложение Api Web Data Science:


Функционал API:

Авторизацию по Token
Апи для анализов (создание, просмотр одного, просмотр списка, редактирование)
Апи для результатов (скачать).


Использование: 

Для получения ТОКЕНА измените файл TOKEN.bat(username=<> password=<>). 
После запуска bat файла, ТОКЕН на этого пользователя сохраниться в файле TOKEN.txt.

Папка "help_files" содержит тестовую базу данных, bat файлы для упрощения выполнения API запросов, 
и файл shortcuts.txt для просмотра возможных команд.
Для автоматического создания анализов измените файл autoAnalysis.bat таким образом, чтобы в строке запроса 
был ВАШ ТОКЕН и файл с анализом существовал по указанному пути.