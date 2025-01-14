#!/bin/bash
echo "Init and clear DB"
flask --app flaskr init-db  
sleep 1
echo "Run localhost server"
flask --app flaskr run --debug 