from __future__ import annotations
from io import BytesIO
import math
import re
import pandas as pd
import numpy as np
from scipy import stats
from .schemas import Evidence


class SpreadsheetError(ValueError): pass

ALIASES = {"etapa": ["etapa", "processo", "stage"], "volume_produzido": ["volume_produzido", "volume", "produzido"], "materia_prima_entrada": ["materia_prima_entrada", "entrada", "materia prima"], "materia_prima_saida_util": ["materia_prima_saida_util", "saida_util", "saída útil"], "energia_kwh": ["energia_kwh", "energia"], "agua_litros": ["agua_litros", "água", "agua"], "custo_total_brl": ["custo_total_brl", "custo", "valor"]}


def read_spreadsheet(raw: bytes, filename: str) -> pd.DataFrame:
    suffix = filename.lower().rsplit(".", 1)[-1]
    try:
        if suffix == "csv": frame = pd.read_csv(BytesIO(raw))
        elif suffix in {"xlsx", "xls"}: frame = pd.read_excel(BytesIO(raw))
        else: raise SpreadsheetError("Formato não suportado. Envie CSV, XLS ou XLSX.")
    except Exception as exc:
        raise SpreadsheetError("Não foi possível ler a planilha. Verifique cabeçalhos e formato.") from exc
    if frame.empty or not len(frame.columns): raise SpreadsheetError("A planilha está vazia ou não contém cabeçalhos.")
    frame.columns = [str(column).strip().lower() for column in frame.columns]
    if not any(pd.api.types.is_numeric_dtype(frame[column]) or pd.to_numeric(frame[column], errors="coerce").notna().any() for column in frame.columns): raise SpreadsheetError("A planilha precisa ter ao menos uma coluna numérica.")
    return frame.drop_duplicates().replace([np.inf, -np.inf], np.nan)


def _column(frame: pd.DataFrame, canonical: str) -> str | None:
    return next((candidate for candidate in ALIASES[canonical] if candidate in frame.columns), None)


def analyze(frame: pd.DataFrame) -> Evidence:
    stage_column = _column(frame, "etapa")
    volume_column = _column(frame, "volume_produzido")
    if not stage_column or not volume_column: raise SpreadsheetError("São necessárias as colunas etapa e volume_produzido para analisar desperdício.")
    stages = frame[stage_column].fillna("Sem etapa").astype(str)
    volume = pd.to_numeric(frame[volume_column], errors="coerce").replace(0, np.nan)
    indicators: list[dict] = []; anomalies: list[dict] = []
    resources = [("materia_prima_entrada", "matéria-prima", "kg"), ("energia_kwh", "energia", "kWh"), ("agua_litros", "água", "L")]
    cost_column = _column(frame, "custo_total_brl")
    for canonical, label, unit in resources:
        column = _column(frame, canonical)
        if not column: continue
        consumption = pd.to_numeric(frame[column], errors="coerce")
        specific = consumption / volume
        valid = specific.dropna()
        if valid.empty: continue
        reference = float(valid.median()); mad = float(np.median(np.abs(valid - reference)))
        robust_z = 0.6745 * (specific - reference) / mad if mad else pd.Series(0, index=specific.index)
        q1, q3 = valid.quantile(.25), valid.quantile(.75); iqr_limit = q3 + 1.5 * (q3 - q1)
        grouped = pd.DataFrame({"stage": stages, "specific": specific}).groupby("stage").specific.mean()
        for stage, value in grouped.dropna().items():
            deviation = (float(value) / reference - 1) * 100 if reference else 0
            indicators.append({"etapa": stage, "recurso": label, "consumo_especifico": round(float(value), 4), "referencia": round(reference, 4), "desvio_pct": round(deviation, 2), "unidade": f"{unit}/unidade"})
        anomalous = (robust_z.abs() >= 3.5) | (specific > iqr_limit)
        for index in frame.index[anomalous.fillna(False)]:
            excess = max(0.0, float(consumption.loc[index] - reference * volume.loc[index]))
            cost = float(pd.to_numeric(frame.loc[index, cost_column], errors="coerce") or 0) if cost_column else 0.0
            anomalies.append({"id": f"A{len(anomalies)+1}", "etapa": str(stages.loc[index]), "recurso": label, "periodo": str(frame.loc[index, "data"]) if "data" in frame else "não informado", "metodo": "z_robusto_iqr", "score": round(float(abs(robust_z.loc[index])), 2), "excesso_estimado": round(excess, 2), "unidade": unit, "custo_estimado_brl": round(cost, 2)})
    if not indicators: raise SpreadsheetError("Não foi possível calcular indicadores com as colunas encontradas.")
    return Evidence(dataset={"linhas": len(frame), "qualidade": {"ausentes_pct": round(float(frame.isna().mean().mean() * 100), 2)}}, indicators=indicators, anomalies=anomalies)


def preview(frame: pd.DataFrame, filename: str) -> tuple[list[str], list[list[str]], list[str]]:
    headers = list(frame.columns); rows = [["" if pd.isna(value) else str(value) for value in row] for row in frame.head(5).itertuples(index=False, name=None)]
    numeric = [column for column in headers if pd.to_numeric(frame[column], errors="coerce").notna().any()]
    return headers, rows, numeric
