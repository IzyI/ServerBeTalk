#JSON запросы в сокеты

###Запросы серверу чата
1. Первый   конект к чату  
    * {"action":"first_connect","type":"user","name":"admin","login":"examp_name","password":"examp_password"} 
    * {"action":"first_connect","type":"protocol","name":"telegram","account":"780035553555","data":[{'id_user': 232968181, 'nickname': 'RSocks Support team', 'info': {'username': 'rsocks'}, 'status': False}]}  
2. Получить информацию по подключенным клиентам и протоколам  
    * {"action": "get_connect_list", "type": "console_client", "name": name,"password": "фиауа3й4рпайцзу7амфывСВ%;ччв5634у"}
