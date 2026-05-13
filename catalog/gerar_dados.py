import pandas as pd
import random
from datetime import datetime, timedelta

produtos = ['Cerveja Pilsen 1L', 'Cerveja Uva 600ml', 'Chopp Abacaxi 1l', 'Chopp Malte 800ml']
depositos = ['Camara fria', 'Deposito norte', 'Depósito secundário']

dados = []
quantidade_linhas = 500

print(f"Gerando {quantidade_linhas} linhas...")

for _ in range(quantidade_linhas):
    produto = random.choice(produtos)
    deposito = random.choice(depositos)
    quantidade = random.randint(10, 300)

    dias_frente = random.randint(30, 700)
    data_validade = datetime.now() + timedelta(days=dias_frente)

    data_formatada = data_validade.strftime('%d/%m/%Y')

    dados.append([produto, deposito, quantidade, data_formatada])

df = pd.DataFrame(dados, columns=['produto', 'deposito', 'quantidade', 'data_validade'])

nome_arquivo = 'planilha_teste_carga.csv'
df.to_csv(nome_arquivo, index=False)

print(f"Sucesso! Arquivo '{nome_arquivo}' criado na sua pasta atual.")