#ANALISE DE DADOS EMPRESA DE VAREJO 

# Pipeline de codigos utilizados para a realização da limpeza dos dados:
'''''
#importando bibliotecas 

import pandas as pd
import datetime as dt

#carregando arquivos 

df = pd.read_csv('/Users/michaelthomazoniespiritosanto/Desktop/SCTEC/mini_projeto_vendas/Base Varejo.csv', sep=';', encoding='utf-8', low_memory=False)
print(f" -> Linhas iniciais: {df.shape[0]:,}")
print(f" -> Colunas iniciais: {df.shape[1]}")
print(df.head())
print(df.dtypes)
print(df.info())

# 1. Criando uma copia de segurança do dataframe
print("\n Criando cópia de segurança (df_copia) \n")
df_copia = df.copy()
print("Cópia de segurança criada com sucesso!")

# 2. Convertendo o campo data para o formato datetime 
df_copia['DATA'] = pd.to_datetime(df_copia['DATA'], format='%y/%m/%d', errors='coerce')
print('Datas convertidas para o tipo datetime.')
print(df_copia.dtypes)

# 3. Removendo colunas vazias desnecessárias (Unnamed)

print("\n Removendo colunas vazias desnecessárias \n")
colunas_antes = df_copia.shape[1]
df_copia = df_copia.loc[:, ~df_copia.columns.str.contains('^Unnamed')]
colunas_depois = df_copia.shape[1]
print(f" -> Colunas antes: {colunas_antes} | Colunas depois: {colunas_depois}")
print(df_copia.head())

# 4. Tratamento de valores '#N/D' na categoria de produtos

print("\n Tentativa para tratar produtos sem identificação (#N/D)\n")
df_validos = df_copia[df_copia['PR_CAT'] != '#N/D'].drop_duplicates(subset=['PR_ID'])
map_cat = dict(zip(df_validos['PR_ID'], df_validos['PR_CAT']))
map_nome = dict(zip(df_validos['PR_ID'], df_validos['PR_NOME']))

mask_nd = df_copia['PR_CAT'] == '#N/D'
df_copia.loc[mask_nd, 'PR_CAT'] = df_copia.loc[mask_nd, 'PR_ID'].map(map_cat)
df_copia.loc[mask_nd, 'PR_NOME'] = df_copia.loc[mask_nd, 'PR_ID'].map(map_nome)

recuperados = df_copia.loc[mask_nd, 'PR_CAT'].notna().sum()
print(f"Tentativa de preenchimento cruzado via PR_ID concluída ({recuperados} registros recuperados).")

# Como não teve possibilidade alterando #N/D por SEM_IDENTIFICACAO
print("\n Preenchendo valaores #N/D convertidos para NaN por SEM_IDENTIFICACAO\n")
df_copia['PR_CAT'] = df_copia['PR_CAT'].fillna('SEM_IDENTIFICACAO')
df_copia['PR_NOME'] = df_copia['PR_NOME'].fillna('SEM_IDENTIFICACAO')
print("Valores que preenchidos com sucesso.")

# 5. Remoção de linhas duplicadas exatas
print("\n Removendo linhas duplicadas exatas \n")
linhas_antes_dup = len(df_copia)
duplicadas_qtd = df_copia.duplicated().sum()
print(f"Linhas duplicadas encontradas: {duplicadas_qtd:,}")

df_copia = df_copia.drop_duplicates()
linhas_depois_dup = len(df_copia)
print(f" Linhas antes da remoção: {linhas_antes_dup:,}")
print(f" Linhas após a remoção de duplicatas: {linhas_depois_dup:,}")

# 6. Salvando a base tratada num novo arquivo CSV

print("\n Salvando base de dados já tratada\n")
df_copia.to_csv('/Users/michaelthomazoniespiritosanto/Desktop/SCTEC/mini_projeto_vendas/base_varejo_limpa.csv', sep=';', index=False, encoding='utf-8')
print(f" Arquivo salvo com sucesso! Dimensão final: {df_copia.shape[0]:,} linhas e {df_copia.shape[1]} colunas.")

'''''

#INICIO DA ANALISE DOS DADOS ÁPOS LIMPEZA

# Importando as bibliotecas necessárias: 

import pandas as pd
import numpy as np 


# Carregemento da base limpa e checagem inicial antes da analise:

df = pd.read_csv('base_varejo_limpa.csv', sep=';', encoding='utf-8',parse_dates=['DATA'])


#Informaçoes gerais da base de dadaos:

print('\n-- INFORMAÇÕES GERAIS DATAFRAME: --\n')
print(f" -> Número de linhas: {df.shape[0]:,}")
print(f" -> Número de colunas: {df.shape[1]}")
print(df.head())
print(df.dtypes)
print(df.info())


print("\n - INÍCIO DA ANALISES - \n")


# 1. Analises estattistas demograficas em relação aos filhos clientes:


clientes_filhos = df.groupby('CL_ID')['CL_FHL'].first()

# 2. Calcular as métricas estatísticas
soma = clientes_filhos.sum()
media = clientes_filhos.mean()
mediana = clientes_filhos.median()
desvio_padrao = clientes_filhos.std()
maximo = clientes_filhos.max()
minimo = clientes_filhos.min()
moda = clientes_filhos.mode()[0]


print("\n-Resumo estatisticos dos dados dos filhos clientes -\n")
print(f"Total de filhos registrados: {soma}")
print(f"Média de filhos por cliente: {media:.2f}")
print(f"Mediana dos dados analisados: {mediana:.2f}")
print(f"Desvio Padrão na qunatidade de filhos entre os clientes: {desvio_padrao:.2f}")
print(f"Máximo de filhos por cliente: {maximo}")
print(f"Mínimo de filhos por cliente: {minimo}")
print(f"Quantidade de filhos mais comum entre os clientes (moda): {moda}")

# 2.  Volume de venda categoria por ano
print("\n  - Volume venda categorias por ano - \n")
volume_venda = (
    df.groupby([df['DATA'].dt.year.rename('ANO'), 'PR_CAT'])
      .size()
      .unstack(level='ANO', fill_value=0)
)
ordem_vendas = df['PR_CAT'].value_counts().index
volume_vanda = volume_venda.loc[ordem_vendas]
volume_venda['TOTAL'] = volume_venda.sum(axis=1)
print(volume_venda)


# 3. Volume de Itens vendidos por categora e segmento 

print("\n - VOLUME TOTAL DE PRODUTOS VENDIDOS POR CATEGORIA E SEGMENTO - \n")

volume_prod = pd.pivot_table(
    df,
    values='PR_ID',
    index='PR_CAT',
    columns='CL_SEG',
    aggfunc=np.size, 
    fill_value=0,
    margins=True,
    margins_name='Total'
)

print(volume_prod)


# 4. Top 10 produtos o com maior volume de transações durante os anos

print("\n- TOP 10 PRODUTOS MAIS VENDIDOS POR ANO -\n")

top10_produtos_ano = (
    df.groupby([df['DATA'].dt.year.rename('ANO'), 'PR_NOME'])
      .size()
      .groupby('ANO', group_keys=False)
      .nlargest(10)
      .reset_index(name='Qtd_Vendida')
)

for ano in top10_produtos_ano['ANO'].unique():
    print(f"\n ANO: {ano}")
    sub_df = top10_produtos_ano[top10_produtos_ano['ANO'] == ano][['PR_NOME', 'Qtd_Vendida']]
    print(sub_df.to_string(index=False))


# 5. Pocentegem de quem compra mais por genero em cada categoria 

print('\n - GENERO QUE MAIS COMPRA POR CATEGORIA - \n')

porcentagens = pd.crosstab(df['PR_CAT'], df['CL_GENERO'], normalize='index') * 100
porcentagens.columns = ['% FEM', '% MASC']
porcentagens.index.name = 'CATEGORIA'

resultado = porcentagens.map(lambda x: f"{x:.2f}%".replace('.', ',')).reset_index()

print(resultado.to_string(index=False))


# 6. Dia da semana com mais volume de compras

print('\n - VOLUME DE COMPRAS DIAS DA SEMANA -\n ')

dias_map = {0:'Segunda', 1:'Terça', 2:'Quarta', 3:'Quinta', 4:'Sexta', 5:'Sábado', 6:'Domingo'}
df['DIA_SEMANA'] = df['DATA'].dt.dayofweek.map(dias_map)

compras_dia = (
    df.groupby('DIA_SEMANA')['CO_ID']
      .nunique()
      .reindex(dias_map.values())
      .sort_values(ascending=False)
      .reset_index(name='VOLUME DE COMPRAS')
)

print(compras_dia.to_string(index=False))
