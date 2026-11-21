from __future__ import annotations
import asyncio
import json
from abc import ABC, abstractmethod
import httpx
from .config import Settings
from .schemas import Evidence, LayaFinding, LayaResult

SYSTEM_PROMPT = "Responda em português apenas com base nas evidências. Cite etapa, recurso, indicador e valor. Diferencie fato de hipótese. Não invente causas ou números."

class LayaUnavailable(RuntimeError): pass
class DeepSeekUnavailable(RuntimeError): pass

class LayaClient(ABC):
    @abstractmethod
    async def evaluate(self, evidence: Evidence) -> LayaResult: ...

class MockLayaClient(LayaClient):
    async def evaluate(self, evidence: Evidence) -> LayaResult:
        findings=[]
        for index, anomaly in enumerate(evidence.anomalies):
            resource = anomaly["recurso"]; score = min(100, max(0, round(float(anomaly["score"]) * 20 + min(float(anomaly["custo_estimado_brl"])/100, 30))))
            category = "perda de matéria-prima" if resource == "matéria-prima" else "consumo excessivo de energia" if resource == "energia" else "uso ineficiente de água"
            severity = "alta" if score >= 70 else "média" if score >= 40 else "baixa"
            findings.append(LayaFinding(anomaly_id=anomaly["id"], categoria=category, severidade=severity, atencao="requer atenção imediata" if severity == "alta" else "acompanhar", pontuacao=score, prioridade=index+1, confianca=.82, status="avaliado"))
        return LayaResult(modelo="MockLayaClient determinístico", achados=findings)

class LocalLayaClient(LayaClient):
    async def evaluate(self, evidence: Evidence) -> LayaResult:
        # TODO: integrar a assinatura oficial documentada de choice/score do Laya local.
        # Nunca enviar a planilha: apenas fichas de evidência normalizadas em português.
        raise LayaUnavailable("Modelo Laya local indisponível.")

class DeepSeekClient(ABC):
    @abstractmethod
    async def explain(self, focus: str, evidence: Evidence, laya: LayaResult) -> str: ...
    @abstractmethod
    async def follow_up(self, question: str, evidence: Evidence, laya: LayaResult) -> str: ...

class MockDeepSeekClient(DeepSeekClient):
    async def explain(self, focus: str, evidence: Evidence, laya: LayaResult) -> str:
        if not evidence.anomalies: return "Não há anomalias estatísticas suficientes para um diagnóstico."
        item=evidence.anomalies[0]; indicator=next((x for x in evidence.indicators if x["etapa"] == item["etapa"] and x["recurso"] == item["recurso"]), evidence.indicators[0])
        return f"Para “{focus}”, a maior atenção está na etapa {item['etapa']}, no recurso {item['recurso']}. O consumo específico foi {indicator['consumo_especifico']} {indicator['unidade']}, contra referência de {indicator['referencia']} ({indicator['desvio_pct']}%). Isso foi identificado por comparação consumo × volume e detecção robusta de anomalia. Hipótese: revise processo e sobras desta etapa."
    async def follow_up(self, question: str, evidence: Evidence, laya: LayaResult) -> str:
        return (await self.explain(question, evidence, laya)) + " Não há evidência para atribuir uma causa única."

class ApiDeepSeekClient(DeepSeekClient):
    def __init__(self, settings: Settings): self.settings=settings
    async def _request(self, user: str) -> str:
        if not self.settings.deepseek_api_key: raise DeepSeekUnavailable("DEEPSEEK_API_KEY não configurada.")
        payload={"model":self.settings.deepseek_model,"messages":[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":user}],"temperature":0,"max_tokens":700}
        for attempt in range(2):
            try:
                async with httpx.AsyncClient(timeout=self.settings.deepseek_timeout_seconds) as client:
                    response=await client.post(f"{self.settings.deepseek_base_url.rstrip('/')}/chat/completions", headers={"Authorization":f"Bearer {self.settings.deepseek_api_key}"}, json=payload); response.raise_for_status()
                    return response.json()["choices"][0]["message"]["content"]
            except (httpx.HTTPError, KeyError) as exc:
                if attempt: raise DeepSeekUnavailable("A explicação textual não pôde ser gerada.") from exc
                await asyncio.sleep(.5)
        raise DeepSeekUnavailable("A explicação textual não pôde ser gerada.")
    async def explain(self, focus: str, evidence: Evidence, laya: LayaResult) -> str: return await self._request(f"Pergunta: {focus}\nEvidências: {evidence.model_dump_json()}\nAvaliação: {laya.model_dump_json()}")
    async def follow_up(self, question: str, evidence: Evidence, laya: LayaResult) -> str: return await self._request(f"Pergunta de acompanhamento: {question}\nEvidências: {evidence.model_dump_json()}\nAvaliação: {laya.model_dump_json()}")

def get_laya(settings: Settings) -> LayaClient: return LocalLayaClient() if settings.laya_mode == "local" else MockLayaClient()
def get_deepseek(settings: Settings) -> DeepSeekClient: return ApiDeepSeekClient(settings) if settings.deepseek_mode == "api" else MockDeepSeekClient()
