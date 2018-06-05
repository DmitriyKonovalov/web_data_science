call ..\env\Scripts\activate
http POST http://localhost:8000/api/v1/analyses/ name="Analysis1" ws="WS_1" wd="WD_1" wd_start=100 wd_stop=200 wd_step=10 ws_start=5 ws_stop=15 Authorization:"Token {TOK}"
http POST http://localhost:8000/api/v1/analyses/1/load_file_data/ file_path={file_path} Authorization:"Token {TOK}"

http POST http://localhost:8000/api/v1/analyses/ name="Analysis2" ws="WS_1" wd="WD_1" wd_start=100 wd_stop=200 wd_step=10 ws_start=5 ws_stop=15 Authorization:"Token {TOK}"
http POST http://localhost:8000/api/v1/analyses/2/load_file_data/ file_path={file_path} Authorization:"Token {TOK}"

http POST http://localhost:8000/api/v1/analyses/ name="Analysis3" ws="WS_1" wd="WD_1" wd_start=100 wd_stop=200 wd_step=10 ws_start=5 ws_stop=15 Authorization:"Token {TOK}"
http POST http://localhost:8000/api/v1/analyses/3/load_file_data/ file_path={file_path} Authorization:"Token {TOK}"

http POST http://localhost:8000/api/v1/analyses/ name="Analysis4" ws="WS_1" wd="WD_1" wd_start=100 wd_stop=200 wd_step=10 ws_start=5 ws_stop=15 Authorization:"Token {TOK}"
http POST http://localhost:8000/api/v1/analyses/4/load_file_data/ file_path={file_path} Authorization:"Token {TOK}"

http POST http://localhost:8000/api/v1/analyses/ name="Analysis5" ws="WS_1" wd="WD_1" wd_start=100 wd_stop=200 wd_step=10 ws_start=5 ws_stop=15 Authorization:"Token {TOK}"
http POST http://localhost:8000/api/v1/analyses/5/load_file_data/ file_path={file_path} Authorization:"Token {TOK}"


http POST http://localhost:8000/api/v1/analyses/1/execute/ Authorization:"Token {TOK}"
http POST http://localhost:8000/api/v1/analyses/2/execute/ Authorization:"Token {TOK}"
http POST http://localhost:8000/api/v1/analyses/3/execute/ Authorization:"Token {TOK}"
http POST http://localhost:8000/api/v1/analyses/4/execute/ Authorization:"Token {TOK}"
http POST http://localhost:8000/api/v1/analyses/5/execute/ Authorization:"Token {TOK}"

http http://127.0.0.1:8000/api/v1/analyses/ Authorization:"Token {TOK}" >> log.txt