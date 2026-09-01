# Documentação Técnica e Governança de Dados

Este documento descreve a arquitetura dimensional, o dicionário de dados e as regras de negócio implementadas no modelo de dados do Power BI.

---

## 1. Arquitetura do Modelo (Star Schema)

O modelo foi construído seguindo os padrões de modelagem dimensional de Ralph Kimball. 

As tabelas de fatos registram os eventos quantitativos do negócio (concessão de crédito, captação de depósitos e metas mensais), enquanto as tabelas de dimensão fornecem o contexto analítico (quem, onde, quando e qual produto).

### Relacionamentos do Modelo

* **Fatos_Carteira_Credito:**
  * `ID_Associado` -> `Dim_Associados[ID_Associado]` (N:1, Unidirecional)
  * `ID_Agencia` -> `Dim_Agencias[ID_Agencia]` (N:1, Unidirecional)
  * `ID_Produto` -> `Dim_Produtos[ID_Produto]` (N:1, Unidirecional)
  * `Data_Contratacao` -> `Dim_Calendario[Date]` (N:1, Unidirecional)
  * `Rating_Bacen` -> `Dim_Rating_Bacen[Rating_Bacen]` (N:1, Unidirecional)
  * `Faixa_Atraso` -> `Dim_Faixa_Atraso[Faixa_Atraso]` (N:1, Unidirecional)

* **Fatos_Captacao:**
  * `ID_Associado` -> `Dim_Associados[ID_Associado]` (N:1, Unidirecional)
  * `ID_Agencia` -> `Dim_Agencias[ID_Agencia]` (N:1, Unidirecional)
  * `ID_Produto` -> `Dim_Produtos[ID_Produto]` (N:1, Unidirecional)
  * `Data_Aplicacao` -> `Dim_Calendario[Date]` (N:1, Unidirecional)

* **Fatos_Metas_Agencias:**
  * `ID_Agencia` -> `Dim_Agencias[ID_Agencia]` (N:1, Unidirecional)
  * `Data_Mes` -> `Dim_Calendario[Date]` (N:1, Unidirecional)

* **Dim_Associados:**
  * `Faixa_Score` -> `Dim_Faixa_Score[Faixa_Score]` (N:1, Unidirecional)

> A opção de "Data/Hora Automática" foi desativada nas propriedades do modelo (`__PBI_TimeIntelligenceEnabled = 0`) para evitar a criação oculta de tabelas locais de calendário, reduzindo o consumo de memória e mantendo a governança explícita via `Dim_Calendario`.

---

## 2. Dicionário de Dados

### 2.1 Tabelas Fato

#### `Fatos_Carteira_Credito`
Registra a posição da carteira de operações de crédito ativas (3.500 contratos).

| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `ID_Contrato` | Texto | Identificador único do contrato de crédito |
| `ID_Associado` | Texto | Identificador do cooperado tomador |
| `ID_Agencia` | Texto | Identificador da agência de originação |
| `ID_Produto` | Texto | Identificador da modalidade de crédito |
| `Data_Contratacao` | Data | Data de liberação do recurso |
| `Data_Vencimento_Final` | Data | Data de vencimento final pactuada |
| `Valor_Contratado` | Moeda | Valor original contratado |
| `Saldo_Devedor` | Moeda | Saldo devedor contábil em aberto |
| `Taxa_Juros_aa` | Número | Taxa de juros anual pactuada no contrato |
| `Dias_Atraso` | Inteiro | Número de dias corridos em atraso de pagamento |
| `Faixa_Atraso` | Texto | Classificação por faixa de atraso |
| `Rating_Bacen` | Texto | Classificação de risco regulatória (AA a H) |
| `Perc_Provisao_PCLD` | Número | Percentual mínimo de provisão exigido pelo BACEN |
| `Valor_Provisao_PCLD` | Moeda | Montante provisionado no balanço (`Saldo_Devedor * Perc_Provisao_PCLD`) |
| `Status_Contrato` | Texto | Status operacional (`Ativo`) |
| `Receita_Juros_Anual_Estimada` | Moeda | Projeção anual de receita financeira |

---

#### `Fatos_Captacao`
Registra as operações de depósitos e investimentos dos associados (2.200 operações ativas).

| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `ID_Operacao_Captacao` | Texto | Identificador único da operação |
| `ID_Associado` | Texto | Identificador do cooperado investidor |
| `ID_Agencia` | Texto | Identificador da agência custodiante |
| `ID_Produto` | Texto | Modalidade de captação (RDC, Poupança, LCA) |
| `Data_Aplicacao` | Data | Data de início da aplicação |
| `Saldo_Aplicado` | Moeda | Saldo atual mantido em depósito |
| `Taxa_Remuneracao_aa` | Número | Taxa de remuneração anual paga ao associado |
| `Custo_Captacao_Anual_Estimado` | Moeda | Custo anual estimado de funding (`Saldo_Aplicado * Taxa`) |

---

#### `Fatos_Metas_Agencias`
Metas mensais corporativas estabelecidas pela diretoria para as agências.

| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `ID_Agencia` | Texto | Identificador da agência |
| `Data_Mes` | Data | Mês de competência da meta |
| `Meta_Originacao_Credito` | Moeda | Meta financeira de concessão de novos créditos |
| `Meta_Captacao_Depositos` | Moeda | Meta financeira de captação líquida de depósitos |
| `Meta_Teto_NPL90_Pct` | Número | Teto máximo tolerado de inadimplência (2,5%) |

---

### 2.2 Tabelas Dimensão

* **`Dim_Agencias`:** Dados das 12 agências da cooperativa regional, incluindo nome, cidade, UF, porte e classificação por polo regional (Polo Santa Cruz, Polo Venâncio Aires, Polo Rio Pardo & Vales e Polo Encosta da Serra).
* **`Dim_Associados`:** Cadastro dos 1.500 associados com segmento (Produtor Rural, Pessoa Jurídica, Pessoa Física), score de crédito e faixa de renda/faturamento.
* **`Dim_Produtos`:** Catálogo de 9 produtos financeiros (linhas de crédito para custeio agro, investimento, capital de giro, veículos e linhas de captação).
* **`Dim_Calendario`:** Calendário contínuo de 2022 a 2028 gerado via DAX, contendo ano, mês, semestre, trimestre e ordenação cronológica estrita (`Ano_Mes` ordenado por `Ano_Mes_Num`).
* **`Dim_Rating_Bacen`:** Dimensão com os 9 níveis de risco da Resolução BACEN 2.682, com ordenação explícita de AA (1) a H (9).
* **`Dim_Faixa_Atraso`:** Dimensão com as faixas de atraso (Em Dia, 01-14 dias, 15-30 dias, 31-60 dias, 61-90 dias e 90+ dias) ordenadas cronologicamente.
* **`Dim_Faixa_Score`:** Dimensão com as faixas de pontuação de crédito (Excelente 800+, Bom 700-799, Regular 550-699 e Crítico <550).

---

## 3. Catálogo de Medidas DAX

Todas as medidas foram centralizadas na tabela técnica `_Medidas` e organizadas em pastas temáticas:

### 3.1 Carteira e Crédito

```dax
-- Saldo devedor total da carteira ativa
Carteira Total Ativa = 
SUM(Fatos_Carteira_Credito[Saldo_Devedor])

-- Montante original concedido
Volume Concedido Original = 
SUM(Fatos_Carteira_Credito[Valor_Contratado])

-- Contagem distinta de contratos
Total Contratos Ativos = 
DISTINCTCOUNT(Fatos_Carteira_Credito[ID_Contrato])

-- Saldo devedor médio por contrato
Ticket Medio por Contrato = 
DIVIDE([Carteira Total Ativa], [Total Contratos Ativos], 0)

-- Taxa anual média de juros ponderada pelo saldo devedor
Taxa Media Juros aa = 
DIVIDE(
    SUMX(Fatos_Carteira_Credito, [Saldo_Devedor] * [Taxa_Juros_aa]),
    [Carteira Total Ativa],
    0
)
```

---

### 3.2 Risco e Inadimplência (BACEN / NPL)

```dax
-- Volume de crédito com pagamentos em dia
Carteira em Dia = 
CALCULATE([Carteira Total Ativa], Fatos_Carteira_Credito[Dias_Atraso] = 0)

-- Volume de crédito com atraso superior a 90 dias (critério oficial BACEN)
Carteira NPL 90+ (Inadimplente) = 
CALCULATE([Carteira Total Ativa], Fatos_Carteira_Credito[Dias_Atraso] > 90)

-- Índice percentual oficial de inadimplência (retorna 0% quando não há atraso no contexto)
Indice NPL 90 % = 
IF(
    NOT ISBLANK([Carteira Total Ativa]) && [Carteira Total Ativa] > 0,
    DIVIDE(
        COALESCE([Carteira NPL 90+ (Inadimplente)], 0),
        [Carteira Total Ativa],
        0
    ),
    BLANK()
)

-- Provisão para Créditos de Liquidação Duvidosa (Resolução BACEN 2.682)
Provisao PCLD Total = 
SUM(Fatos_Carteira_Credito[Valor_Provisao_PCLD])

-- Índice de Cobertura de Provisão sobre a carteira inadimplente (> 100% indica solidez)
Cobertura da Provisao % = 
DIVIDE([Provisao PCLD Total], [Carteira NPL 90+ (Inadimplente)], 0)

-- Percentual da provisão em relação à carteira total ativa
Perc PCLD sobre Carteira % = 
DIVIDE([Provisao PCLD Total], [Carteira Total Ativa], 0)
```

---

### 3.3 Captação e Liquidez

```dax
-- Volume total custodiado em depósitos dos associados
Volume Total Captacao = 
SUM(Fatos_Captacao[Saldo_Aplicado])

-- Custo médio ponderado do funding pago aos cooperados
Custo Medio Captacao aa = 
DIVIDE(
    SUMX(Fatos_Captacao, [Saldo_Aplicado] * [Taxa_Remuneracao_aa]),
    [Volume Total Captacao],
    0
)

-- Relação entre crédito concedido e depósitos captados (Intermediação Financeira)
Indice Credito sobre Depositos % = 
DIVIDE([Carteira Total Ativa], [Volume Total Captacao], 0)

-- Ticket médio por operação de depósito
Ticket Medio Captacao = 
DIVIDE([Volume Total Captacao], [Total Operacoes Captacao], 0)

-- Saldo líquido entre depósitos e empréstimos por unidade de atendimento
Superavit de Liquidez Agencias = 
[Volume Total Captacao] - [Carteira Total Ativa]
```

---

### 3.4 Resultado Financeiro

```dax
-- Diferença entre a taxa de juros cobrada e o custo de funding
Spread Bancario Medio aa = 
[Taxa Media Juros aa] - [Custo Medio Captacao aa]

-- Resultado operacional bruto anual da intermediação financeira
Margem Financeira Bruta Anual = 
SUM(Fatos_Carteira_Credito[Receita_Juros_Anual_Estimada]) - SUM(Fatos_Captacao[Custo_Captacao_Anual_Estimado])
```

---

### 3.5 Eixos Visuais Dinâmicos

```dax
-- Limite superior do Eixo Y no gráfico por polo (+20% de margem no topo)
Eixo Y Max Liquidez Regional = 
VAR _MaxCredito = MAXX(ALLSELECTED(Dim_Agencias[Regional]), [Carteira Total Ativa])
VAR _MaxCaptacao = MAXX(ALLSELECTED(Dim_Agencias[Regional]), [Volume Total Captacao])
RETURN
    MAX(_MaxCredito, _MaxCaptacao) * 1.20

-- Limite superior do Eixo Y no gráfico por agência (+20% de margem no topo)
Eixo Y Max Intermediacao Agencia = 
VAR _MaxCredito = MAXX(ALLSELECTED(Dim_Agencias[Nome_Agencia]), [Carteira Total Ativa])
VAR _MaxCaptacao = MAXX(ALLSELECTED(Dim_Agencias[Nome_Agencia]), [Volume Total Captacao])
RETURN
    MAX(_MaxCredito, _MaxCaptacao) * 1.20
```

---

## 4. Enquadramento Regulatório (BACEN - Resolução 2.682)

A classificação de risco e o cálculo de provisão foram parametrizados com base nas regras mínimas do Conselho Monetário Nacional:

| Nível de Risco | Dias de Atraso Mínimos | Alíquota Mínima de Provisão | Descrição |
| :---: | :---: | :---: | :--- |
| **AA** | 0 dias | **0,0%** | Risco Mínimo |
| **A** | 0 dias | **0,5%** | Risco Muito Baixo |
| **B** | 0 dias | **1,0%** | Risco Baixo |
| **C** | 15 a 30 dias | **3,0%** | Risco Moderado |
| **D** | 31 a 60 dias | **10,0%** | Risco Médio |
| **E** | 61 a 90 dias | **30,0%** | Risco Alto |
| **F** | 91 a 120 dias | **50,0%** | Risco Muito Alto |
| **G** | 121 a 180 dias | **70,0%** | Risco Crítico |
| **H** | > 180 dias | **100,0%** | Perda Provável |

---

## 5. Rastreabilidade e Auditoria

A geração dos dados sintéticos registra log de execução em `logs/geracao_dados.log`, contendo data e hora, contagem de registros por tabela e totalizadores de controle financeiro para conferência de consistência.
