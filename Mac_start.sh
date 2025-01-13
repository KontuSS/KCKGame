#!/bin/bash
echo "Init and clear DB"
flask --app flaskr init-db  
echo "Run localhost server"
python3 -m flask --app flaskr run --debug 