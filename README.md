# Fundamentus Stock Ranking (Selenium + Pandas)

Automação em Python para coletar dados do site Fundamentus, aplicar filtros fundamentalistas simples e gerar um ranking básico de ações para análise exploratória.

> English (short): Python automation that scrapes stock fundamentals from Fundamentus using Selenium, applies basic filters, and outputs a simple ranking for exploratory analysis.

---

## Principais recursos

* Coleta automatizada da tabela de ações no Fundamentus (Selenium)
* Conversão dos dados para `pandas.DataFrame`
* Limpeza e normalização de campos numéricos (percentuais, valores, etc.)
* Aplicação de filtros fundamentalistas objetivos
* Geração de ranking (ex.: Top 10 / Top 15) diretamente no terminal
* Estrutura simples e direta, refletindo o objetivo educacional do projeto

---

## Contexto

Ao estudar automação e análise de dados no mercado financeiro, é comum precisar:

* coletar dados públicos de forma estruturada
* transformar tabelas em datasets utilizáveis
* aplicar filtros e regras simples
* gerar rankings e comparações rápidas

Este projeto é um exercício prático de **web scraping + tratamento de dados**, com foco em clareza e simplicidade.

---

## Aviso importante (uso responsável)

Este repositório é apresentado como **projeto de estudo/portfólio**.

* Não representa recomendação de compra ou venda de ativos
* Utilize apenas para fins educacionais
* O site Fundamentus pode alterar layout/estrutura, o que pode quebrar o scraping
* Evite execução em alta frequência (respeite o serviço e boas práticas)

---

## Estrutura do projeto

```
.
├─ main.py
├─ requirements.txt
├─ LICENSE
└─ README.md
```

---

## Requisitos

* Python 3.10+
* Google Chrome ou Microsoft Edge
* WebDriver compatível (ChromeDriver / EdgeDriver)

> Observação: dependendo da versão do Selenium, o driver pode ser gerenciado automaticamente. Caso contrário, será necessário manter o driver instalado e disponível no PATH.

---

## Instalação

Crie um ambiente virtual e instale as dependências:

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

---

## Execução

Execute o script principal:

```bash
python main.py
```

O processo executa as seguintes etapas:

* acesso ao Fundamentus
* coleta da tabela de ações
* conversão para DataFrame
* aplicação de filtros
* ordenação e impressão do ranking no terminal

---

## Saídas geradas

* Ranking exibido no terminal
* Dataset em memória (DataFrame) pronto para evoluções futuras

---

## Sanitização de dados

Este repositório não contém dados sensíveis.

* Os dados são públicos (fonte: Fundamentus)
* Não há credenciais, tokens ou arquivos privados

---

## Licença

MIT
