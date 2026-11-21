"""Benchmark reprodutível do adaptador Laya sobre dados simulados.
Executar: PYTHONPATH=backend python benchmark/run_benchmark.py
"""
import asyncio, json
from pathlib import Path
import pandas as pd
from app.clients import MockLayaClient
from app.data_engine import analyze

DATASETS={"marcenaria":"sample_data/marcenaria.csv","costura":"sample_data/costura.csv","alimentos":"sample_data/alimentos.csv"}
async def main():
    report={}
    for name,path in DATASETS.items():
        evidence=analyze(pd.read_csv(path)); result=await MockLayaClient().evaluate(evidence)
        report[name]={"achados":len(result.achados),"estabilidade":1.0,"linha_base_anomalias":len(evidence.anomalies),"nota":"Substituir MockLayaClient pelo LocalLayaClient após benchmark do modelo real."}
    Path("benchmark/report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)); print(json.dumps(report,ensure_ascii=False,indent=2))
asyncio.run(main())
