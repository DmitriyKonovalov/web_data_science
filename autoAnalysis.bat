call env\Scripts\activate
http --auth admin:adminadmin POST http://localhost:8000/api/v1/analyses/ name="AutoAnalysis5" ws="WS_1" wd="WD_1" wd_start=100 wd_stop=200 wd_step=10 ws_start=5 ws_stop=15
http --auth admin:adminadmin POST http://localhost:8000/api/v1/analyses/5/load_file_data/ file_path="C:\data.csv"
http --auth admin:adminadmin http://localhost:8000/api/v1/analyses/5/execute/
http --auth admin:adminadmin http://localhost:8000/api/v1/analyses/5/download/