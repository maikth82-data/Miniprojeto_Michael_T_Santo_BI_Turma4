# MIMI PROJETO ANALISE DE DADOS VAREJO

Este projeto tem como objetivo realizar uma Analise de Dados de desempenho de vendas e comportamento do consumidor de uma empresa de varejo que comercializa diversos produtos em diferentes categorias.

**Como rodar o script para visualizar os indicadores usados no projeto**

Após clonar o repositório do Github <git clone (https://github.com/maikth82-data/Miniprojeto_Michael_T_Santo_BI_Turma4.git> siga os seguintes passos:

1. Abra o seu VScode ou programa da sua preferência, e abra a pasta onde está o arquivo **mini_projeto_Michael_T_E_Santo.py**
2. Se colocou o  arquivo **base_varejo_limpa.csv** na mesma pasta que o script, basta rodar o script para ver o resultado dos insights. 
3. Caso a base de dados esteja em pasta diferente, encontre a pasta onde esta o arquivo do projeto, copie o caminho exato de onde está o arquivo **base_varejo_limpa.csv** e cole no script onde indica o nome do arquivo.
Após um desses passos o script irá rodar normalmente!!


# 1. Análise inicial e limpeza de dados da base Varejo

Esta etapa do projeto de análise de dados voltada para uma empresa do setor de varejo, iniciando pela **exploração, diagnóstico e tratamento de qualidade de dados** utilizando Python e a biblioteca Pandas.

## Sobre a Base de Dados

A base original (`Base Varejo.csv`) mostra o comportamento de compras, contendo informações transacionais, demográficas e de catálogo de produtos ao longo dos anos.

* **Volume Inicial dos dados sem tratamento:** 830.000 registos e 14 colunas.  
* **Período das transações:** 04/01/2019 a 08/12/2022.  
* **Variáveis Principais:** Identificadores de compra (`CO_ID`), clientes (`CL_ID`), atributos demográficos (`CL_GENERO`, `CL_SEG`, `CL_FHL`, `CL_EC`), produtos (`PR_ID`, `PR_CAT`, `PR_NOME`) e datas de transação (`DATA`).

---

## Problemas Identificados na Base Original

Durante a análise inicial dos dados, foram detectados os seguintes problemas estruturais e de qualidade:

1. **Linhas Duplicadas:** Presença de 96.553 registos duplicados exatos que geram redundância e distorções estatísticas.  
2. **Valores Nulos Ocultos (`#N/D`):** Existência de 3.650 linhas onde as colunas de categoria e nome do produto vinham preenchidas incorretamente como `#N/D`.  
3. **Colunas Vazias Residuais:** Colunas fantasmas geradas por delimitadores no final das linhas de exportação.  
4. **Coluna com formato de codificação errado:** Coluna data com formato errado atrapalhando futuras análises.

---

## Processo de Tratamento (Python)

Foi desenvolvido uma série de códigos para garantir a limpeza de acordo com as etapadas abaixo:

1. **Carregamento:** Importação do ficheiro CSV delimitado por ponto e vírgula.  
2. **Cópia em Memória:** Criação da cópia de segurança (`df_copia = df.copy()`).  
3. **Limpeza:** Remoção de colunas vazias desnecessárias (`Unnamed`) para garantir que não haja erros na futuras análise e não comprometa o desempenho do dataframe com informações desnecessárias.  
4. **Tratamento de inconsistências:**  Tentativa de mapeamento e substituição de valores `#N/D` nas colunas categoria e nome produto com base no ID do produto (`PR_ID`), para resolver os casos de falta de informação para que fosse possível realizar análises com melhor desempenho sem dados faltantes.  
**Substituição dos valores `#N/D` por `SEM_INFORMACAO`:** Como através da substituição não houve a possibilidade de completar os dados faltantes nas categorias, eles foram substituídos por SEM_INFORMACAO
6. **Remoção de duplicados:** Remoção de linhas duplicadas exatas, reduzindo a base de 830.000 para 733.447 linhas limpas. Isto foi essencial para que nãp haja resultados errados nas análises de vendas e estatisticas básicas.  
7. **Padronização Temporal:** Conversão da coluna de data para o formato datetime do Pandas. Necessário para geração de análises temporais  
8. **Exportação:** Geração da base tratada e pronta para análise em `base_varejo_limpa.csv`.

---

## Códigos utilizados para limpeza dos dados

 
import pandas as pd
import datetime as dt

df = pd.read_csv('/Users/michaelthomazoniespiritosanto/Desktop/SCTEC/mini_projeto_vendas/Base Varejo.csv', sep=';', encoding='utf-8', low_memory=False)
print(f" -> Linhas iniciais: {df.shape[0]:,}")
print(f" -> Colunas iniciais: {df.shape[1]}")
print(df.head())
print(df.dtypes)
print(df.info())

print("\n Criando cópia de segurança (df_copia) \n")
df_copia = df.copy()
print("Cópia de segurança criada com sucesso!")

df_copia['DATA'] = pd.to_datetime(df_copia['DATA'], format='%y/%m/%d', errors='coerce')
print('Datas convertidas para o tipo datetime.')
print(df_copia.dtypes)

print("\n Removendo colunas vazias desnecessárias \n")
colunas_antes = df_copia.shape[1]
df_copia = df_copia.loc[:, ~df_copia.columns.str.contains('^Unnamed')]
colunas_depois = df_copia.shape[1]
print(f" -> Colunas antes: {colunas_antes} | Colunas depois: {colunas_depois}")
print(df_copia.head())

print("\n Tentativa para tratar produtos sem identificação (#N/D)\n")
df_validos = df_copia[df_copia['PR_CAT'] != '#N/D'].drop_duplicates(subset=['PR_ID'])
map_cat = dict(zip(df_validos['PR_ID'], df_validos['PR_CAT']))
map_nome = dict(zip(df_validos['PR_ID'], df_validos['PR_NOME']))

mask_nd = df_copia['PR_CAT'] == '#N/D'
df_copia.loc[mask_nd, 'PR_CAT'] = df_copia.loc[mask_nd, 'PR_ID'].map(map_cat)
df_copia.loc[mask_nd, 'PR_NOME'] = df_copia.loc[mask_nd, 'PR_ID'].map(map_nome)

recuperados = df_copia.loc[mask_nd, 'PR_CAT'].notna().sum()
print(f"Tentativa de preenchimento cruzado via PR_ID concluída ({recuperados} registros recuperados).")

print("\n Preenchendo valaores #N/D convertidos para NaN por SEM_IDENTIFICACAO\n")
df_copia['PR_CAT'] = df_copia['PR_CAT'].fillna('SEM_IDENTIFICACAO')
df_copia['PR_NOME'] = df_copia['PR_NOME'].fillna('SEM_IDENTIFICACAO')
print("Valores que preenchidos com sucesso.")

print("\n Removendo linhas duplicadas exatas \n")
linhas_antes_dup = len(df_copia)
duplicadas_qtd = df_copia.duplicated().sum()
print(f"Linhas duplicadas encontradas: {duplicadas_qtd:,}")

df_copia = df_copia.drop_duplicates()
linhas_depois_dup = len(df_copia)
print(f" Linhas antes da remoção: {linhas_antes_dup:,}")
print(f" Linhas após a remoção de duplicatas: {linhas_depois_dup:,}")

print("\n Salvando base de dados já tratada\n")
df_copia.to_csv('/Users/michaelthomazoniespiritosanto/Desktop/SCTEC/mini_projeto_vendas/base_varejo_limpa.csv', sep=';', index=False, encoding='utf-8')
print(f" Arquivo salvo com sucesso! Dimensão final: {df_copia.shape[0]:,} linhas e {df_copia.shape[1]} colunas.")

---

## 2. Relatório de Insights após análise de indicadores

Após a limpeza dados foram gerados indicadores para a analise dos dados onde foram encontrados os seguintes insigths de négocios conforme relatados abaixo: 

1. **Perfil demográfico clientes (número de filhos)**

A análise estatística indica uma quantidade considerável de dependentes com 1136 filhos cadastrados e uma certa variação no tamanho das famílias. O perfil da base apresenta uma média de 1.14 por cliente.Também foi possível observar clientes com até 4 filhos e clientes com 0 filhos. 

Investir em produtos de maior volume voltados para família e ações promocionais para datas comemorativas como Dia dos Pais e Dia das Mães, irão auxiliar na performance de vendas .

2. **Volume de venda por categoria por ano**

Em relação à análise de histórica por volume de vendas por categoria, a que mais vendeu ao longo de todos os anos foi a de alimentos com 384.197 produtos, seguido pelas categorias higiene e limpeza. 

3. **Volume de Vendas por Categoria/Segmento** 

No comportamento de consumo por segmento, o mais consumidor é o  B com mais de 486.500 itens comprados , logo após o segmento C e por último o segmento A. As categorias com maior consumo em relação ao segmentos são: 1° Alimentos, 2º Higiene e 3º limpeza.

O segmento B é quem mantém a operação, abrindo oportunidade para a criação de novos programas de fidelidade e benefícios.

4. **Top 10 produtos com o maior número de vendas por ano (2019 - 2022)**

Entre os 10 produtos mais vendidos pela empresa o líder absoluto em vendas é o presunto cozido que está presente em mais de 12.719 itens vendidos, permanecendo como um produto âncora para a compra do outros itens vendidos pelo varejo. 

Na sequência vem outros produtos que variam historicamente de posição.

Uma boa estratégia para aumentar as vendas,  seria realizar promoções casadas dos produtos com maior volume de vendas com produtos menos vendidos para aumentar o faturamento e aliviar o estoque. 

5. **Distribuição de compra por gênero e categoria**

Realizando uma análise geral da base, historicamente é possível reconhecer que o público absoluto é feminino, representando entre 51% e 53% das compras em todas as categorias. As categorias que mais se destacam no público feminino são acessórios 53,13% e limpeza 52,34%. e alimentos

Entre o público masculino que está entre 46% e 48% das vendas, se destacam nas categorias Bebidas 48,35% e Pet 48,14%.

Isto mostra uma grande oportunidade para aumentar as vendas em ambos os públicos nas categorias onde eles mais consomem, realizando ações de descontos, combos promocionais entre outros.

6. **Volume histórico de compras por dia da semana**

Realizando uma análise global de toda a base, foi possível entender que historicamente o dia de maior movimento é na quarta-feira com o maior número de transações (3.450 compras) o segundo dia com maior movimento é na sexta - feira(2.905 compras) e depois o domingo com (2984 compras).

Para aproveitar este movimento que acontece na loja é de importância priorizar realocação de pessoal em todos os setores para estes dias de maior movimento. Para melhorar o movimento em outros dias da semana, principalmente no sábado (dia de menor movimento), realizar promoções temáticas seria de grande importância como o "Sabádo das carnes e cervejas”. 

## 3. Considerações finais:

Nesta análise de dados foi possível visualizar que historicamente a empresa teve um volume de vendas com uma performance considerável ao longo dos anos . 

Mas também foi possível observar algumas lacunas de desempenho que poderiam ser ajustadas para aumentar a performance das vendas em suas categorias de produtos, como a realizando ações direcionais para gêneros, segmentos e promoções para determinados dias da semana e datas especiais. 

Em relação aos dados a empresa possui um bom portfólio de dados principalmente demográficos que contribuem para as análises. Mas a falta de preenchimento de dados nas colunas produtos e categorias acabam causando um ponto de atenção nas análises.   


##  Estrutura de arquivos do repositório
  
* `Base Varejo_limpa.csv`: Base de dados limpa e pronta para análises avançadas.  
* `mini_projeto_Michael_T_E_Santo_BI_Turma4.py`: Script principal contendo os códigos de tratamento de dados e os códigos das utlizandos para realizar as analises.  
* `README_Michael T. E Santo_BI_Turma4`: Documentação oficial do projeto com todos os dados e relatório final.

---
