import argparse
from dataclasses import dataclass

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


FUNDAMENTUS_URL = "https://www.fundamentus.com.br/resultado.php"


@dataclass
class Filters:
    pl_min: float = 0
    pvp_max: float = 1
    roic_min: float = 0
    roe_min: float = 0
    mrg_liq_min: float = 0
    mrg_ebit_min: float = 0
    cresc_rec_5a_min: float = 0
    liq_corr_min: float = 1
    liq_2m_min: float = 1_000_000
    div_brut_patrim_max: float = 1


def _to_float_percent_br(series: pd.Series) -> pd.Series:
    """
    Converte strings percentuais do formato BR para float.
    Ex: '12,34%' -> 12.34
    """
    s = series.astype("string").str.replace("%", "", regex=False)
    s = s.str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
    return s.astype(float)


def fetch_table_from_fundamentus(headless: bool = True) -> pd.DataFrame:
    """Abre o Fundamentus via Selenium e retorna a tabela como DataFrame."""
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1400,900")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )
    try:
        driver.get(FUNDAMENTUS_URL)

        local_tabela = "/html/body/div[1]/div[2]/table"
        tabela_el = driver.find_element("xpath", local_tabela)

        html_tabela = tabela_el.get_attribute("outerHTML")
        df = pd.read_html(str(html_tabela), thousands=".", decimal=",")[0]
        return df
    finally:
        driver.quit()


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """Seleciona colunas, define índice e converte tipos."""
    df = df.set_index("Papel")

    cols = [
        "Cotação",
        "P/L",
        "P/VP",
        "ROIC",
        "ROE",
        "Mrg. Líq.",
        "Mrg Ebit",
        "Cresc. Rec.5a",
        "Liq. Corr.",
        "Liq.2meses",
        "Dív.Brut/ Patrim.",
    ]
    df = df[cols].copy()

    # Converte colunas percentuais (no seu notebook você tratava essas)
    df["ROIC"] = _to_float_percent_br(df["ROIC"])
    df["ROE"] = _to_float_percent_br(df["ROE"])
    df["Mrg. Líq."] = _to_float_percent_br(df["Mrg. Líq."])
    df["Mrg Ebit"] = _to_float_percent_br(df["Mrg Ebit"])
    df["Cresc. Rec.5a"] = _to_float_percent_br(df["Cresc. Rec.5a"])

    return df


def apply_filters(df: pd.DataFrame, f: Filters) -> pd.DataFrame:
    """Aplica filtros (mesma lógica do notebook, só parametrizada)."""
    out = df.copy()

    out = out[out["P/L"] > f.pl_min]
    out = out[out["P/VP"] < f.pvp_max]
    out = out[out["ROIC"] > f.roic_min]
    out = out[out["ROE"] > f.roe_min]
    out = out[out["Mrg. Líq."] > f.mrg_liq_min]
    out = out[out["Mrg Ebit"] > f.mrg_ebit_min]
    out = out[out["Cresc. Rec.5a"] > f.cresc_rec_5a_min]
    out = out[out["Liq. Corr."] > f.liq_corr_min]
    out = out[out["Liq.2meses"] > f.liq_2m_min]
    out = out[out["Dív.Brut/ Patrim."] < f.div_brut_patrim_max]

    return out


def rank(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ordena seguindo a ideia do notebook: aplicar ordenações sucessivas
    (mantive a essência, sem inventar score complexo).
    """
    colunas_preferencias = {
        "P/L": "menor",
        "P/VP": "menor",
        "ROIC": "maior",
        "ROE": "maior",
        "Mrg. Líq.": "maior",
        "Mrg Ebit": "maior",
        "Cresc. Rec.5a": "maior",
        "Liq. Corr.": "maior",
        # "Liq.2meses": "maior",  # opcional (igual seu comentário)
        "Dív.Brut/ Patrim.": "menor",
    }

    out = df.copy()
    for coluna, pref in colunas_preferencias.items():
        out = out.sort_values(by=coluna, ascending=(pref == "menor"))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Coleta dados do Fundamentus, aplica filtros e gera um ranking simples."
    )
    parser.add_argument("--top", type=int, default=15, help="Quantidade de ações para exibir (padrão: 15).")
    parser.add_argument("--no-headless", action="store_true", help="Abre o Chrome visível (debug).")
    parser.add_argument("--out", type=str, default="", help="Caminho para salvar CSV (opcional).")

    args = parser.parse_args()

    df_raw = fetch_table_from_fundamentus(headless=not args.no_headless)
    df = preprocess(df_raw)

    filtros = Filters()  # valores padrão iguais ao seu notebook
    df_f = apply_filters(df, filtros)
    df_rank = rank(df_f)

    if args.top > 0:
        df_rank = df_rank.head(args.top)

    print(df_rank)

    if args.out:
        df_rank.to_csv(args.out, encoding="utf-8-sig")
        print(f"\nArquivo salvo em: {args.out}")


if __name__ == "__main__":
    main()
