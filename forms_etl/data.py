#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 17:20:34 2024

@author: root

Aims to update our database
"""
import psycopg2 ## Postgres
import pandas as pd

# get the data updated
concs = pd.read_excel('C:/Users/Mucho/Work/mac/Target/Pickles/reports/conc_ssss.xlsx')
#concs = concs.query("`Porque não efetuamos o Pedido?` != 'vazio'")
# set the columns that matters for the WhatsApp
cols  = ['Nome do Representante',
        'CLIENTE',
        'Telefone (Whatsapp)',
        'Prazo', 
        'Porque não efetuamos o Pedido?',
        'Observação']

# get connected
conn = psycopg2.connect(
                host="localhost",
                database="mucho",
                user="postgres",
                password="1728",
                )

# cursor to execute SQL
curr = conn.cursor()

# update the database
for i in range(118):
    curr.execute("""INSERT INTO public.forms (nome_repr,cliente,telefone,prazo,motivo,obs) VALUES (%s, %s, %s, %s,%s, %s);""", (
    concs.loc[i,cols[0]],#[0],
    concs.loc[i,cols[1]],#[0],
    concs.loc[i,cols[2]],#[0]
    concs.loc[i,cols[3]],
    concs.loc[i,cols[4]],#[0]
    concs.loc[i,cols[5]],
))

conn.commit()