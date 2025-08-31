#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 11:47:21 2024

@author: root
"""

import pandas as pd
from tools import objToStr, save_pkl, load_pkl
import sqlite3 as s

con = s.connect('C:/Users/Mucho/Work/mac/Target/forms_etl/db_tubozan.db')



path = "C:/Users/Mucho/Downloads/"

no  = pd.read_excel(path + "Tubozan Expansão Nordeste(1-16).xlsx")
sul = pd.read_excel(path + "Tubozan Expansão SUL(1-49).xlsx")
mg  = pd.read_excel(path + "Tubozan Expansão(1-48).xlsx")
co  = pd.read_excel(path + "Tubozan Expansão Centro Oeste (1).xlsx")

forms = [no,sul,mg,co]

#-------- minas gerais ---------#
mg    = forms[2]
mg    = mg.fillna('vazio').copy()
mg    = mg.rename(columns={'Lojaas EF Carvalho': 'Lojas EF Carvalho', 'Numero do Telefone (Whatsapp)':'Telefone (Whatsapp)', 'Estado do Representante':'Regional do Representante'}).copy()
lojas = mg.columns[mg.columns.str.contains('Lojas')]

id_lojas_to_stack = mg.loc[:,lojas]
id_lojas_to_stack.loc[:,'ID'] =  mg.loc[:,'ID']

lojas_stacked = id_lojas_to_stack.set_index('ID').stack()
lojas_stacked = lojas_stacked.loc[~lojas_stacked.str.contains('vazio')].copy()
lojas_stacked = lojas_stacked.to_frame().reset_index()
lojas_stacked = lojas_stacked.rename(columns={'level_1':'Lojas_1', 0:'Lojas_2'}).copy()

the_rest = list(set(mg.columns) - set(lojas))
therest  = pd.Series(the_rest)


new_mg                  = mg.loc[:,therest]
new_mg.loc[:,'Lojas_1'] = lojas_stacked.loc[:,'Lojas_1']
new_mg.loc[:,'Lojas_2'] = lojas_stacked.loc[:,'Lojas_2']

idx = new_mg.loc[new_mg.loc[:,'Nome do Representante (Interior de Minas)'].str.contains('vazio'),'ID'].index

new_mg.loc[idx,'Nome do Representante (Interior de Minas)'] = new_mg.loc[idx,'Nome do Representante (RMBH)']
new_mg = new_mg.rename(columns={'Nome do Representante (Interior de Minas)':'Nome do Representante'}).copy()
new_mg.drop(columns='Nome do Representante (RMBH)', inplace=True)


new_mg.loc[:,'forms_name'] = 'Minas'

new_mg_1 = objToStr(new_mg).copy()

#-------- no ---------#

mg    = forms[0]
mg    = mg.rename(columns={'Estado do Representante':'Regional do Representante'}).copy()

mg    = mg.fillna('vazio').copy()
lojas = mg.columns[mg.columns.str.contains('Lojas')]


id_lojas_to_stack = mg.loc[:,lojas]
id_lojas_to_stack.loc[:,'ID'] =  mg.loc[:,'ID']

lojas_stacked = id_lojas_to_stack.set_index('ID').stack()
lojas_stacked = lojas_stacked.loc[~lojas_stacked.str.contains('vazio')].copy()
lojas_stacked = lojas_stacked.to_frame().reset_index()
lojas_stacked = lojas_stacked.rename(columns={'level_1':'Lojas_1', 0:'Lojas_2'}).copy()

the_rest = list(set(mg.columns) - set(lojas))
therest  = pd.Series(the_rest)
#therest  = therest[list(range(28))]

new_mg                  = mg.loc[:,therest]
new_mg.loc[:,'Lojas_1'] = lojas_stacked.loc[:,'Lojas_1']
new_mg.loc[:,'Lojas_2'] = lojas_stacked.loc[:,'Lojas_2']

cols_with_names = new_mg.columns.str.contains('Nome do Representante')
see             = new_mg.loc[:,cols_with_names]
see.loc[:,'ID'] = new_mg.loc[:,'ID'].copy()
names_stacked = see.set_index('ID').stack()
names_stacked = names_stacked.loc[~names_stacked.str.contains('vazio')]
names_stacked = names_stacked.to_frame().reset_index()
names_stacked = names_stacked.rename(columns={'level_1':'Regional por Estado',0:'Nome do Representante'})

new_mg.drop(columns=new_mg.loc[:,cols_with_names].columns, inplace=True)


new_mg.loc[:,'Nome do Representante'] = names_stacked.loc[:,'Nome do Representante']

new_mg.loc[:,'forms_name'] = 'Nordeste'

new_mg_2 = objToStr(new_mg).copy()


#-------- sul ---------#

mg    = forms[1]

mg    = mg.rename(columns={'Numero do Telefone (Whatsapp)':'Telefone (Whatsapp)', 'Estado do Representante':'Regional do Representante'}).copy()


mg    = mg.fillna('vazio').copy()
be    = mg.columns.get_loc('Nome do Representante (PR)')
tween = mg.columns.get_loc('Loja Existe')
lojas = mg.columns[be+1:tween]


id_lojas_to_stack = mg.loc[:,lojas]
id_lojas_to_stack.loc[:,'ID'] =  mg.loc[:,'ID']

lojas_stacked = id_lojas_to_stack.set_index('ID').stack()
lojas_stacked = lojas_stacked.loc[~lojas_stacked.str.contains('vazio')].copy()
lojas_stacked = lojas_stacked.to_frame().reset_index()
lojas_stacked = lojas_stacked.rename(columns={'level_1':'Lojas_1', 0:'Lojas_2'}).copy()

the_rest = list(set(mg.columns) - set(lojas))
therest  = pd.Series(the_rest)
#therest  = therest[list(range(28))]

new_mg                  = mg.loc[:,therest]
new_mg.loc[:,'Lojas_1'] = lojas_stacked.loc[:,'Lojas_1']
new_mg.loc[:,'Lojas_2'] = lojas_stacked.loc[:,'Lojas_2']

cols_with_names = new_mg.columns.str.contains('Nome do Representante')
see             = new_mg.loc[:,cols_with_names]
see.loc[:,'ID'] = new_mg.loc[:,'ID'].copy()
names_stacked = see.set_index('ID').stack()
names_stacked = names_stacked.loc[~names_stacked.str.contains('vazio')]
names_stacked = names_stacked.to_frame().reset_index()
names_stacked = names_stacked.rename(columns={'level_1':'Regional por Estado',0:'Nome do Representante'})

new_mg.drop(columns=new_mg.loc[:,cols_with_names].columns, inplace=True)


new_mg.loc[:,'Nome do Representante'] = names_stacked.loc[:,'Nome do Representante']

new_mg.loc[:,'forms_name'] = 'Sul'


new_mg_3 = objToStr(new_mg).copy()



#-------- co ---------#

mg    = forms[3]

mg    = mg.rename(columns={'Numero do Telefone (Whatsapp)':'Telefone (Whatsapp)', 'Estado do Representante':'Regional do Representante'}).copy()


mg    = mg.fillna('vazio').copy()
be    = mg.columns.get_loc('Nome do Representante (Centro Oeste)')
tween = mg.columns.get_loc('Loja Existe')
lojas = mg.columns[be+1:tween]


id_lojas_to_stack = mg.loc[:,lojas]
id_lojas_to_stack.loc[:,'ID'] =  mg.loc[:,'ID']

lojas_stacked = id_lojas_to_stack.set_index('ID').stack()
lojas_stacked = lojas_stacked.loc[~lojas_stacked.str.contains('vazio')].copy()
lojas_stacked = lojas_stacked.to_frame().reset_index()
lojas_stacked = lojas_stacked.rename(columns={'level_1':'Lojas_1', 0:'Lojas_2'}).copy()

the_rest = list(set(mg.columns) - set(lojas))
therest  = pd.Series(the_rest)
#therest  = therest[list(range(28))]

new_mg                  = mg.loc[:,therest]
new_mg.loc[:,'Lojas_1'] = lojas_stacked.loc[:,'Lojas_1']
new_mg.loc[:,'Lojas_2'] = lojas_stacked.loc[:,'Lojas_2']

cols_with_names = new_mg.columns.str.contains('Nome do Representante')
see             = new_mg.loc[:,cols_with_names]
see.loc[:,'ID'] = new_mg.loc[:,'ID'].copy()
names_stacked = see.set_index('ID').stack()
names_stacked = names_stacked.loc[~names_stacked.str.contains('vazio')]
names_stacked = names_stacked.to_frame().reset_index()
names_stacked = names_stacked.rename(columns={'level_1':'Regional por Estado',0:'Nome do Representante'})

new_mg.drop(columns=new_mg.loc[:,cols_with_names].columns, inplace=True)


new_mg.loc[:,'Nome do Representante'] = names_stacked.loc[:,'Nome do Representante']

new_mg.loc[:,'forms_name'] = 'Centro Oeste'


new_mg_4 = objToStr(new_mg).copy()

# ---------------- finess --------------- #

def fine(con_c):
    
    con_c = objToStr(con_c).copy()

    for col in con_c.columns:
        if con_c[col].dtype == 'string':
            con_c.loc[:,col] = con_c.loc[:,col].str.strip()
            con_c.loc[:,col] = con_c.loc[:,col].str.title()  
        else:
            continue
    return con_c


# ---------------- yet --------------- #

cnpjotas = load_pkl('cnpjotas')


# ---------------- finally --------------- #


conc = pd.concat([new_mg_1,new_mg_2,new_mg_3, new_mg_4])
conc = conc.rename(columns={'Já compou da TUBOZAN':'Já comprou da TUBOZAN'})
conc = objToStr(conc).copy()
conc.loc[:,'Lojas_2'] = conc.loc[:,'Lojas_2'].str.strip()
conc.loc[:,'Lojas_2'] = conc.loc[:,'Lojas_2'].str.upper()
conc.rename(columns={'Lojas_2':'CLIENTE'}, inplace=True)

save_pkl(conc,'conc_2')
conc.to_sql('forms_conc',con,if_exists='replace')
conc.to_excel('C:/Users/Mucho/Work/mac/Target/Pickles/reports/Forms_concat.xlsx')
con.commit()

