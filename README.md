# Bancos Reviews

Projeto para coleta, organização, rotulagem e análise de reviews de aplicativos bancários, com foco em comentários da **Google Play Store** no ano de **2025**.

## Objetivo

Construir um pipeline de dados para:

- coletar reviews de aplicativos de bancos
- filtrar comentários de 2025
- preparar os dados para rotulagem
- rotular sentimento e assunto
- treinar modelos de machine learning para classificação de texto

## Escopo do projeto

Os aplicativos analisados atualmente são:

- Nubank
- Itaú
- Banco do Brasil
- Caixa
- Inter
- Santander
- Bradesco

## Problema de negócio

Comentários em lojas de aplicativos carregam sinais importantes sobre:

- satisfação do usuário
- falhas recorrentes
- problemas de login
- dificuldades com Pix e pagamentos
- percepção de atendimento, usabilidade e estabilidade

Este projeto busca transformar esses comentários em uma base estruturada para análise e modelagem.

## Estrutura do projeto

```text
bancos-reviews/
├── .venv_ml/
├── app/
├── data/
│   ├── raw/
│   ├── processed/
│   ├── labeling/
│   │   ├── imports/
│   │   └── exports/
│   └── labeled/
├── models/
├── notebooks/
├── src/
│   ├── scraper.py
│   └── preprocessing.py
├── .gitignore
├── inicio.py
├── README.md
└── requirements.txt