#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

mssql = {'host': '185.161.10.160',
         'user': 'motion_motion',
         'passwd': 'Lotion.webcup',
         'db': 'motion_db'}

postgresql = {'host': 'localhost',
         'user': 'postgres',
         'passwd': 'postgres',
         'db': 'motion_db'}

mysql = {
    'host': '185.161.10.160',
    'user': 'motion_motion',
    'passwd': 'Lotion.webcup',
    'db': 'motion_db'
}


mssqlConfig = "mssql+pyodbc://{}:{}@{}:1433/{}?driver=SQL+Server+Native+Client+10.0".format(mssql['user'], mssql['passwd'], mssql['host'], mssql['db'])
postgresqlConfig = "postgresql+psycopg2://{}:{}@{}/{}".format(postgresql['user'], postgresql['passwd'], postgresql['host'], postgresql['db'])
mysqlConfig = "mysql+pymysql://{}:{}@{}/{}".format(mysql['user'], mysql['passwd'], mysql['host'], mysql['db'])

