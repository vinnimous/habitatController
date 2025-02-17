#!/bin/bash

URL="http://admin:admin@localhost:3000"
KEY_NAME="install_key"
TOKEN="Authorization: Bearer "
CONTENT="Content-Type: application/json"
ACCEPT="Accept: application/json"

DATASOURCES="grafana_datasources.yml"
DASHSOURCES="grafana_dashboards.yml"

LOCATION_DATASOURCES="/etc/grafana/provisioning/datasources/"
LOCATION_DASHBOARDS="/etc/grafana/provisioning/dashboards/"

DASHBOARDS=(
  "grafana_dash_current.json"
  "grafana_dash_historical.json"
)

create_datasource() {
  sudo cp $DATASOURCES $LOCATION_DATASOURCES
}

create_dashboard() {
  for d in "${DASHBOARDS[@]}"; do
    sudo cp "$d" $LOCATION_DASHBOARDS
  done
  sudo cp $DASHSOURCES $LOCATION_DASHBOARDS
}

create_datasource
create_dashboard
