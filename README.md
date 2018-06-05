web_data_science
Порядок установки: 
1) git clone https://github.com/DmitriyKonovalov/web_data_science;
2) python -m venv env;
3) call env\Scripts\activate;
4) pip install -r requirements.txt;
5) python manage.py makemigrations;
6) python manage.py migrate;
7) python manage.py createsuperuser 
... Указываем <username, password, email>;
8) python manage.py runserver

Note: шаги 2-6 можно запустить в автоматическом режиме (help_files\easy_install.bat)

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