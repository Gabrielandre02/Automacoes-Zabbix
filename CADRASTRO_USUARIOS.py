#!/usr/bin/env python
# -*- coding: utf-8 -*-
from zabbix_api import ZabbixAPI

ZBX_URL = "http://zabbix-frontend.zabbixsummit.local"
ZBX_USER = "Admin"
ZBX_PASSWORD = "zabbix"

#FAZENDO LOGIN NA API
try:
    zapi = ZabbixAPI(ZBX_URL, timeout=180, validate_certs=False)
    zapi.login(ZBX_USER, ZBX_PASSWORD)
    print(f"Conectado na API do Zabbix, {zapi.api_version()}")
except Exception as erro:
    print(f"Não foi possivel se Conectar na API {erro}")
    exit()

# VERIFICA OS GRUPOS NO ZABBIX
def valida_group(name):
    try:
        hostgroup = zapi.usergroup.get(
        {
        "method": "usergroup.get",
        "params": {
            "output": "sortfield",
            "status": 0
        },
        })
        try:
            for i in hostgroup:
                valida = name
                id = i["usrgrpid"]
                nome = i["name"]
                if nome in valida:
                    return id
                    break
        except:
            print(f"Error!{i}")
    except:
        print("ERROR O SE CONECTAR NA API DO ZABBIX")

#VERIFICA A ROLE NO ZABBIX
def valida_role(name):
    try:
        hostgroup = zapi.role.get({
        "output": "extend"})
        try:
            for i in hostgroup:
                    valida = name
                    id = i["roleid"]
                    nome = i["name"]
                    if nome in valida:
                        return id
                        break
        except:
            print("ERROR")
    except:
        print(F"ERROR {hostgroup}")



user = input("Digite o nome do usuario? : ")
grupo = input("Qual grupo do zabbix? : ")
role = input("Qual Role no Zabbix? : ")
passwd = input("Qual senha do usuario? :")

# VARIAVEL QUE RECEBE O NOME DO GRUPO E A ROLE PARA FAZER O CADRASTRO NA API
idgrupo = valida_group(grupo)
idrole = valida_role(role)

#FAZENDO O CADRASTRO NA API
print ("Validando o Cadrastro")
try:
    hostgroup = zapi.user.create({
        "username": user,
        "passwd": passwd,
        "roleid": idrole,
        "usrgrps": [
            {
                "usrgrpid": idgrupo
            }
        ]
    })
    print(f"USUARIO CADRASTRADO COM SUCESSO {hostgroup}")
except:
    print(f"Error {hostgroup}")