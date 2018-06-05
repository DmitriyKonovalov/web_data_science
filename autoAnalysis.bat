call env\Scripts\activate
http POST http://localhost:8000/api/v1/analyses/ name="AutoAnalysis6" ws="WS_1" wd="WD_1" wd_start=100 wd_stop=200 wd_step=10 ws_start=5 ws_stop=15 Authorization:"Token b04ffd7cc10af4ffd068622d95578ed434029109"
http POST http://localhost:8000/api/v1/analyses/6/load_file_data/ file_path="C:\data.csv" Authorization:"Token b04ffd7cc10af4ffd068622d95578ed434029109"
http POST http://localhost:8000/api/v1/analyses/6/execute/ Authorization:"Token b04ffd7cc10af4ffd068622d95578ed434029109"
http POST http://localhost:8000/api/v1/analyses/6/download/ Authorization:"Token b04ffd7cc10af4ffd068622d95578ed434029109"