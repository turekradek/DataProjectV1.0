# DataProjectV1.0

Flask
http://localhost:5000/

Grafana 
http://localhost:3000/login

Prometheus
http://localhost:9090/query


Elastgicsearch
http://localhost:5601/app/integrations/browse


Kibana
http://localhost:9200/

Elasticvue
http://localhost:8080/welcome

UI for Apache Kafka
http://localhost:8081/

Flask
http://localhost:5000/filescsv
http://localhost:5000/filesjson/cars.json
http://localhost:5000/filescsv/test_data.csv




Usługa,Adres URL,Opis
Flask API,http://localhost:5000,Główna aplikacja i serwer danych
Airflow,http://localhost:8082,Orkiestracja zadań ETL (DAGs)
Kafka UI,http://localhost:8081,Interfejs do zarządzania klastrem Kafka
Grafana,http://localhost:3000,Dashboardy i wizualizacja metryk
Prometheus,http://localhost:9090,Silnik metryk i zapytań Time-Series
Kibana,http://localhost:5601,Eksploracja logów w Elasticsearch
Elasticvue,http://localhost:8080,Lekki przeglądarkowy klient Elasticsearch
Elasticsearch,http://localhost:9200,Silnik wyszukiwania (REST API)

podman exec -it flask_app flask routes