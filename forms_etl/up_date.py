# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 08:01:24 2024

@author: Mucho
"""


import pandas  as pd
from   tools   import objToStr, save_pkl, load_pkl
import sqlite3 as s
import re


# Catch the files
path = "C:/Users/Mucho/Downloads/"

no  = pd.read_excel(path + "Tubozan Expansão Nordeste(1-16).xlsx")
sul = pd.read_excel(path + "Tubozan Expansão SUL(1-50) (1).xlsx")
m_g = pd.read_excel(path + "Tubozan Expansão(1-48).xlsx")
co  = pd.read_excel(path + "Tubozan Expansão Centro Oeste (2).xlsx")

forms = [no,sul,m_g,co]


def fix_prospect(new_mg):
    
    cols_with_names = new_mg.columns.str.contains('Nome do Representante')
    see             = new_mg.loc[:,cols_with_names]
    see.loc[:,'ID'] = new_mg.loc[:,'ID'].copy()
    names_stacked   = see.set_index('ID').stack()
    names_stacked   = names_stacked.loc[~names_stacked.str.contains('vazio')]
    names_stacked   = names_stacked.to_frame().reset_index()
    names_stacked   = names_stacked.rename(columns={'level_1':'Regional por Estado',0:'Nome do Representante'})

    new_mg.drop(columns=new_mg.loc[:,cols_with_names].columns, inplace=True)

    new_mg.loc[:,'Nome do Representante'] = names_stacked.loc[:,'Nome do Representante']
    return new_mg


def s_tack(mg,lojas):
      
     id_lojas_to_stack             = mg.loc[:,lojas]
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
     
     return  new_mg



def set_state(idx):
    
    #-------- no ---------#
    if idx == 0:
        mg    = forms[idx]
        mg    = mg.rename(columns={'Estado do Representante':'Regional do Representante'}).copy()
        mg    = mg.fillna('vazio').copy()
        lojas = mg.columns[mg.columns.str.contains('Lojas')]
        mg.loc[:,'forms_name'] = 'Nordeste'
        return mg, lojas
    
    #-------- sul ---------#
    elif idx == 1:
        mg    = forms[idx]
        mg    = mg.rename(columns={'Numero do Telefone (Whatsapp)':'Telefone (Whatsapp)', 'Estado do Representante':'Regional do Representante'}).copy()
        mg    = mg.fillna('vazio').copy()
        be    = mg.columns.get_loc('Nome do Representante (PR)')
        tween = mg.columns.get_loc('Loja Existe')
        lojas = mg.columns[be+1:tween]
        mg.loc[:,'forms_name'] = 'Sul'
        return mg, lojas
    
    #-------- minas gerais ---------#
    elif idx == 2:
        mg    = forms[2]
        mg    = mg.fillna('vazio').copy()
        mg    = mg.rename(columns={'Lojaas EF Carvalho': 'Lojas EF Carvalho', 'Numero do Telefone (Whatsapp)':'Telefone (Whatsapp)', 'Estado do Representante':'Regional do Representante'}).copy()
        lojas = mg.columns[mg.columns.str.contains('Lojas')]
        mg.loc[:,'forms_name'] = 'Minas'
        return mg, lojas
    
    #-------- co ---------#
    elif idx == 3:
        mg    = forms[idx]
        mg    = mg.rename(columns={'Numero do Telefone (Whatsapp)':'Telefone (Whatsapp)', 'Estado do Representante':'Regional do Representante'}).copy()
        mg    = mg.fillna('vazio').copy()
        be    = mg.columns.get_loc('Nome do Representante (Centro Oeste)')
        tween = mg.columns.get_loc('Loja Existe')
        lojas = mg.columns[be+1:tween]
        mg.loc[:,'forms_name'] = 'Centro Oeste'
        return mg, lojas
    

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


def cnp_jotas(conc):
    
    to_adjust = ['CLIENTE','CIDADE','UF']
    to_concs  = pd.read_excel('C:/Users/Mucho/Work/mac/Target/Pickles/reports/to_concat_2.xlsx')
    mm = objToStr(to_concs)
    for column in to_adjust:
        mm.loc[:,column] = mm.loc[:,column].str.strip()
        mm.loc[:,column] = mm.loc[:,column].str.upper()
    
    conc = objToStr(conc)
    for column in ['CLIENTE','Nome do Representante']:
        conc.loc[:,column] = conc.loc[:,column].str.strip()
        conc.loc[:,column] = conc.loc[:,column].str.upper()
        
    conc.loc[:,'ID'] = [i for i in range(len(conc))]
    conc_merge       = conc.merge(mm, on='CLIENTE', how='left') 
    conc_merge       = conc_merge.astype({'CNPJ':'string'})
    conc             = conc_merge.replace({'UF':{'vazio':'MG'}}) 
    conc.drop([56,57,108], inplace=True) 
    conc.loc[:,'CNPJ'] = conc.loc[:,'CNPJ'].str.split('.', expand=True)[0]     
    
    return conc


def ac_tions(see):
    
    action = pd.read_excel('C:/Users/Mucho/Work/mac/Target/Pickles/reports/Ações.xlsx')
    
    data = {
    'Sector': ['Gerência Comercial', 'Gerência Comercial', 'Gerência Comercial', 'Gerência Comercial', 'Marketing', 'Marketing', 'Marketing','Vazio'],
    'Porque não efetuamos o Pedido?': ['Preço', 'Atendimento', 'Fidelidade com concorrente', 'Prazo de entrega', 
              'Inicio de Relacionamento', 'Variedade de produtos', 'Qualidade do produto','vazio']
    }
    datas = pd.DataFrame(data)
    dicts = datas.set_index('Porque não efetuamos o Pedido?').to_dict()
    see.loc[:,'Ação'] = see.loc[:,'Porque não efetuamos o Pedido?'].apply(lambda x: dicts['Sector'].get(x,'vazio'))
    
    conc = see
    conc["Prazo"] = conc['Hora de conclusão']
    for issue in set(action["Issue"]):
        see_1 = conc.loc[conc['Porque não efetuamos o Pedido?'].str.contains(issue),'Prazo'].index
        dd    = action.loc[action['Issue'].str.contains(issue),'Prazo [d]']
        conc.loc[see_1,"Prazo"] = conc.loc[see_1,'Hora de conclusão'] - pd.Timedelta(days=dd.iloc[0])
    
    return see

def dat_es(conc):
    
    def date_s(opp, col):
        dates      = opp[col]
        opp['Date']= dates.dt.date
        opp['Ano'] = dates.dt.year
        opp['Mês'] = dates.dt.month
        opp['Dia'] = dates.dt.day
        return opp

    conc = date_s(conc,'Hora de conclusão')
    return conc


def zb_link(conc):
    
    see = [conc.loc[i,'UF'] + '-' + conc.loc[i,'CIDADE'] for i in conc.index]
    conc.loc[:,'CIDADE'] = see
    return conc    


def m_erge(concs):
    
    to_catch = pd.read_excel('C:/Users/Mucho/Work/mac/Target/Pickles/reports/to_catch.xlsx')
    for con_c in [concs,to_catch]:
        con_c = objToStr(con_c)
        con_c.columns = con_c.columns.str.strip() #ajusta o nome das colunas
        for col in con_c.columns: #padroniza as células 
            if con_c[col].dtype == 'string':
                con_c.loc[:,col] = con_c.loc[:,col].str.strip()
                con_c.loc[:,col] = con_c.loc[:,col].str.upper()  
            else:
                continue
   
    clientes = concs.merge(to_catch, on='CLIENTE')
    clientes_group = clientes.loc[:,['CLIENTE','REPRESENTACAO','Nome do Representante','CNPJ','CIDADE']] #tabela dicionário
    clientes_group.to_excel('C:/Users/Mucho/Work/mac/Target/Pickles/reports/clientes_groupp.xlsx')
    return concs

def tel_fix(concs):
    
    tel = concs['Telefone (Whatsapp)']
    tel = tel.astype('string')
    tels = tel.apply(lambda x : x.replace(' ','').replace('-','').replace('.','').replace('(','').replace(')',''))
    numbers = tels.apply(lambda x: re.findall('(\d+)',x))
    concs['Telefone (Whatsapp)'] = numbers
    return concs
    
# ---------------- finally --------------- #
#@fine
def c_onc(form_s):
    
    n = len(form_s)
    
    conc = pd.concat([ fix_prospect(s_tack(*set_state(i))) for i in range(n)])
    conc = conc.rename(columns={'Já compou da TUBOZAN':'Já comprou da TUBOZAN'})
    conc = objToStr(conc).copy()
    col = 'CLIENTE'
    conc.rename(columns={'Lojas_2':col}, inplace=True) 
    conc.loc[:,col] = conc.loc[:,col].str.strip()
    conc.loc[:,col] = conc.loc[:,col].str.upper()
    #conc.replace({'LOURIVAL RAUPP / EDUARDO': 'RAUPP REPRESENTAÇÕES COMERC.'}, inplace=True)
    #conc.replace({'HARRI JOHANN': 'HARRI JOHANN & CIA LTDA'}, inplace=True)
    
    return conc


def update(conc):
    
    #conc.drop('Unnamed: 0',axis=1,inplace=True)
    # Connect to a database
    con = s.connect('C:/Users/Mucho/Work/mac/Target/forms_etl/db_tubozan.db')
    
    save_pkl(conc,'conc_2sss')
    conc.to_sql('forms_concsss',con,if_exists='replace')
    conc.to_excel('C:/Users/Mucho/Work/mac/Target/Pickles/reports/conc_ssss.xlsx')
    con.commit()
    
    print('****************** GET UP AND DATE !!! ******************')
    return conc

def magic():

    m = dat_es(ac_tions(m_erge(c_onc(forms))))
    
    m = update(m)
    
    return m
    
        
work_ = magic() 
        

    
    
    
    
    
    
    
    
    
    