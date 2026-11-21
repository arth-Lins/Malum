from __future__ import annotations
from uuid import uuid4
from fastapi import FastAPI, File, HTTPException, UploadFile
from .clients import DeepSeekUnavailable, LayaUnavailable, get_deepseek, get_laya
from .config import get_settings
from .data_engine import SpreadsheetError, analyze, preview, read_spreadsheet
from .schemas import AnalyzeRequest, AnalysisResponse, ChatMessage, ChatRecord, ChatRequest, Finding, Preview, UploadResponse

app = FastAPI(title="Malum API", version="0.1.0")
uploads: dict[str, object] = {}; chats: dict[str, ChatRecord] = {}

def response_from_evidence(focus: str, evidence, laya, explanation: str | None, warning: str | None) -> AnalysisResponse:
    ranked = sorted(evidence.indicators, key=lambda item: item["desvio_pct"], reverse=True)
    findings=[]
    for index, item in enumerate(ranked[:8]):
        linked=next((a for a in evidence.anomalies if a["etapa"] == item["etapa"] and a["recurso"] == item["recurso"]), None)
        severity="alta" if item["desvio_pct"] >= 20 else "média" if item["desvio_pct"] >= 10 else "baixa"
        findings.append(Finding(id=linked["id"] if linked else f"I{index+1}",stage=item["etapa"],resource=item["recurso"],value=item["consumo_especifico"],reference=item["referencia"],deviation=item["desvio_pct"],unit=item["unidade"],cost=linked["custo_estimado_brl"] if linked else 0,severity=severity))
    top=findings[0]; estimated=sum(item.cost for item in findings)
    return AnalysisResponse(dataset=evidence.dataset, focus=focus, findings=findings, estimatedWaste=f"R$ {estimated:,.2f}".replace(",","X").replace(".",",").replace("X","."), attentionStage=top.stage, indicator=f"{top.value:.2f} {top.unit}", layaAvailable=laya is not None, warning=warning, evidence=evidence, laya=laya, explanation=explanation)

@app.post("/upload", response_model=UploadResponse)
async def upload(file: UploadFile = File(...)):
    settings=get_settings(); raw=await file.read()
    if len(raw) > settings.max_upload_bytes: raise HTTPException(413,"Arquivo excede o limite do plano.")
    try: frame=read_spreadsheet(raw,file.filename or "planilha.csv"); headers, rows, numeric=preview(frame,file.filename or "planilha.csv")
    except SpreadsheetError as exc: raise HTTPException(422,str(exc))
    upload_id=str(uuid4()); uploads[upload_id]=frame
    return UploadResponse(uploadId=upload_id,preview=Preview(fileName=file.filename or "planilha",rows=len(frame),headers=headers,preview=rows),numericColumns=numeric)

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_upload(request: AnalyzeRequest):
    frame=uploads.get(request.upload_id)
    if frame is None: raise HTTPException(404,"Upload não encontrado. Envie a planilha novamente.")
    try: evidence=analyze(frame)
    except SpreadsheetError as exc: raise HTTPException(422,str(exc))
    settings=get_settings()
    try: laya=await get_laya(settings).evaluate(evidence)
    except LayaUnavailable: return response_from_evidence(request.focus,evidence,None,None,"Análise incompleta: a avaliação da Laya não está disponível no momento. Os indicadores foram calculados, mas a classificação e o diagnóstico completo dependem dessa etapa.")
    try: explanation=await get_deepseek(settings).explain(request.focus,evidence,laya); warning=None
    except DeepSeekUnavailable: explanation=None; warning="A classificação foi concluída, mas a explicação textual não pôde ser gerada. Tente novamente."
    result=response_from_evidence(request.focus,evidence,laya,explanation,warning)
    analysis_id=str(uuid4()); result.analysis_id=analysis_id
    record=ChatRecord(id=analysis_id,title=request.focus,analysis=result,messages=[ChatMessage(id=str(uuid4()),role="bot",text=explanation or warning or "Indicadores calculados.")]); chats[record.id]=record
    return result

@app.post("/chat", response_model=ChatMessage)
async def chat(request: ChatRequest):
    record=chats.get(request.analysis_id)
    if record is None: raise HTTPException(404,"Análise não encontrada.")
    if not record.analysis.laya: raise HTTPException(409,"Análise incompleta: não é possível gerar diagnóstico sem Laya.")
    try: text=await get_deepseek(get_settings()).follow_up(request.question,record.analysis.evidence,record.analysis.laya)
    except DeepSeekUnavailable as exc: raise HTTPException(503,str(exc))
    message=ChatMessage(id=str(uuid4()),role="bot",text=text); record.messages.extend([ChatMessage(id=str(uuid4()),role="user",text=request.question),message]); return message

@app.get("/chats", response_model=list[ChatRecord])
async def list_chats(): return list(chats.values())
