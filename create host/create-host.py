#!/usr/bin/env python
# -*- coding: utf-8 -*-

from zabbix_api import ZabbixAPI
import csv, sys, json
from datetime import date
sys.tracebacklimit=0

data_atual = date.today()
arquivo = open(f"ATM-HOST{data_atual}.txt", "a")

with open('municipios.json', encoding="utf-8-sig") as f:
    data = json.load(f)
def lat_long(name):
    for i in data:
        if i['nome'].lower() != name:
            continue
        else:
            lat = i['latitude']
            lon = i['longitude']
            break
    return lat, lon


#FAZENDO LOGIN NA API

ZBX_URL = ""
ZBX_USER = ""
ZBX_PASSWORD = ""


try:
    zapi = ZabbixAPI(ZBX_URL, timeout=180, validate_certs=False)
    zapi.login(ZBX_USER, ZBX_PASSWORD)
    print(f"Conectado na API do Zabbix, {zapi.api_version()}")
except Exception as erro:
    print(f"Não foi possivel se Conectar na API {erro}")
    exit()


cidade = input("Digite o Nome da cidade:")
x = lat_long(cidade)
city = cidade.upper()
lat = x[0]
lon = x[1]

f = csv.reader(open('ARQUIVO CSV'), delimiter=',')
for [host,ip,community] in f:
    try:
        print ("Tentanto validar o cadrastro"), f.line_num
        hostgroup = zapi.host.create({
        "host": host,
        "proxy_hostid": "ID PROXY",
        "interfaces": [
            {
                "type": 2,
                "main": 1,
                "useip": 1,
                "ip": ip,
                "dns": "",
                "port": "161",
                "details": {
                    "version": 2,
                    "bulk": 1,
                    "community": "{$SNMP_COMMUNITY}"
                }
            }
        ],
        "groups": [
            {
                "groupid": "GROUP ID"
            },
        ],
               "tags": [
            {
                "tag": "POP",
                "value": city
            },
            {
                "tag": "NAME TAG",
                "value": "VALUE TAG"
            },
        ],
        "templates": [
            {
                "templateid": "TEMPLATE ID"
            }
        ],
           "macros": [
            {
                "macro": "{$SNMP_COMMUNITY}",
                "value": community
            }
        ],
        "inventory_mode": 1,
            "inventory": 
                {
                "location_lat": lat,
                "location_lon": lon
        }
        })
        print (f"host cadastrado com sucesso {host,ip,community}")
        arquivo.write(("Nome do Equipamento: " + host ) + (" IP do Equipamento: " + ip) + (" Community: " + community ) + "\n")
    except Exception as erro:
        print(print (f"host duplicado {erro}"))
        continue
arquivo.close()