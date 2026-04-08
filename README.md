# 📊 Pipeline ETL: Taxa de Desocupação (IBGE)

Este projeto consiste em um pipeline **ETL (Extract, Transform, Load)** desenvolvido em Python para o monitoramento de indicadores socioeconômicos.

O objetivo principal é extrair a série temporal da **taxa de desocupação do Brasil** (com foco em Pernambuco) a partir da API do IBGE e armazenar esses dados de forma estruturada no **MongoDB Atlas**.


### Equipe:  Fabiana Carolie e Renan Vanbasten
---

## 🎯 Funcionalidades

### 🔍 Extração (Extract)

* Coleta de dados da **Tabela 4093 (PNAD Contínua)** via API de Agregados do IBGE.
* Filtro por:

  * Localidade (**Pernambuco**)
  * Categorias de sexo (**Total, Homens e Mulheres**)

### 🔄 Transformação (Transform)

* Processo de **achatamento (flattening)** de JSON aninhado para documentos planos.
* Conversão de tipos de dados:

  * String → Float
* Tratamento de valores nulos (`...`)

### 📦 Carregamento (Load)

* Inserção de dados em banco NoSQL na nuvem (**MongoDB Atlas**)
* **Idempotência garantida**:

  * A coleção é limpa antes de novas inserções para evitar duplicidade

---

## 📂 Estrutura do Projeto

```plaintext
eng_data_atvd/
│
├── main.py               # Orquestrador que executa o fluxo completo
├── .env                  # Credenciais do MongoDB (não versionado)
├── .gitignore            # Ignora venv e informações sensíveis
├── requirements.txt      # Dependências do projeto
│
└── src/
    ├── __init__.py       # Define a pasta como pacote Python
    ├── extract.py        # Classe Extract: comunicação com API do IBGE
    └── load.py           # Classe Load: transformação e carga no MongoDB
```

---

## 🚀 Como Executar

### 1. ✅ Pré-requisitos

* Python **3.10 ou superior**
* Ambiente virtual (**venv**) configurado
* Conta no **MongoDB Atlas** com IP liberado no Network Access

---

### 2. ⚙️ Instalação e Configuração

Clone o repositório e entre na pasta do projeto.

#### Criar e ativar o ambiente virtual:

```bash
python -m venv venv
source venv/Scripts/activate  # Windows (Git Bash)
# ou
source venv/bin/activate      # Linux/Mac
```

#### Instalar dependências:

```bash
pip install -r requirements.txt
```

#### Configurar variáveis de ambiente:

Crie um arquivo `.env` na raiz do projeto:

```env
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
```

---

### 3. ▶️ Rodando o Pipeline

```bash
python main.py
```

---

## 💡 Notas de Engenharia de Dados

* 📈 **Série Temporal**: O projeto trabalha com 56 períodos trimestrais (2012–2025)
* ⚙️ **Escalabilidade**: A estrutura em classes permite adicionar novas tabelas do IBGE facilmente ao extrator
* 🧠 **Design NoSQL**: Uso de documentos atômicos para facilitar:

  * Agregações
  * Filtros por categoria no MongoDB
