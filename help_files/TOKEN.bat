call ..\env\Scripts\activate 
http POST http://127.0.0.1:8000/api/v1/auth/api-token-auth/ username="admin" password="adminadmin" >> TOKEN.txt