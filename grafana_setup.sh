#!/bin/bash

URL="http://admin:admin@localhost:3000"
KEY_NAME="install_key"
TOKEN="Authorization: Bearer "
CONTENT="Content-Type: application/json"
ACCEPT="Accept: application/json"

#GET, POST, DELETE
KEY="/api/auth/keys"
DATASOURCES="/api/datasources"
DASHBOARD="/api/dashboards/db"

SOURCES=(
"grafana_data_mysql.json"
)
DASHES=(
"grafana_dash_current.json"
"grafana_dash_historical.json"
)

create_token(){
  curl -X POST -H "Content-Type: application/json" -d '{"name":"$KEY_NAME", "role": "Admin"}' $URL | json_pp
}

create_datasource(){
  apiurl="$URL$DATASOURCES"
  for d in "${SOURCES[@]}"; do
  curl -X POST $apiurl -H "$CONTENT" -d @"$d"
  done
}

create_dashboard(){
  apiurl="$URL$DASHBOARD"
  for d in "${DASHES[@]}"; do
  curl -X POST $apiurl -H "$CONTENT" -d @"$d"
  done
}

create_datasource
create_dashboard

