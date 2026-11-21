from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field


class Preview(BaseModel):
    file_name: str = Field(serialization_alias="fileName")
    rows: int
    headers: list[str]
    preview: list[list[str]]


class UploadResponse(BaseModel):
    upload_id: str = Field(serialization_alias="uploadId")
    preview: Preview
    numeric_columns: list[str] = Field(serialization_alias="numericColumns")


class Finding(BaseModel):
    id: str
    stage: str
    resource: str
    value: float
    reference: float
    deviation: float
    unit: str
    cost: float = 0
    severity: Literal["alta", "média", "baixa"] = "baixa"


class Evidence(BaseModel):
    dataset: dict
    indicators: list[dict]
    anomalies: list[dict]


class LayaFinding(BaseModel):
    anomaly_id: str
    categoria: Literal["perda de matéria-prima", "consumo excessivo de energia", "uso ineficiente de água", "padrão anormal de consumo", "sem desperdício relevante"]
    severidade: Literal["baixa", "média", "alta"]
    atencao: Literal["requer atenção imediata", "acompanhar", "sem ação"]
    pontuacao: int = Field(ge=0, le=100)
    prioridade: int
    confianca: float = Field(ge=0, le=1)
    status: Literal["avaliado", "nao_avaliado"]


class LayaResult(BaseModel):
    modelo: str
    achados: list[LayaFinding]


class AnalysisResponse(BaseModel):
    analysis_id: str | None = Field(default=None, serialization_alias="analysisId")
    dataset: dict
    focus: str
    findings: list[Finding]
    estimated_waste: str = Field(serialization_alias="estimatedWaste")
    attention_stage: str = Field(serialization_alias="attentionStage")
    indicator: str
    laya_available: bool = Field(serialization_alias="layaAvailable")
    warning: str | None = None
    evidence: Evidence
    laya: LayaResult | None = None
    explanation: str | None = None


class AnalyzeRequest(BaseModel):
    upload_id: str = Field(alias="uploadId")
    focus: str = Field(min_length=3, max_length=1000)


class ChatRequest(BaseModel):
    analysis_id: str = Field(alias="analysisId")
    question: str = Field(min_length=2, max_length=1000)


class ChatMessage(BaseModel):
    id: str
    role: Literal["bot", "user"]
    text: str
    references: list[str] | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow, serialization_alias="createdAt")


class ChatRecord(BaseModel):
    id: str
    title: str
    created_at: datetime = Field(default_factory=datetime.utcnow, serialization_alias="createdAt")
    analysis: AnalysisResponse
    messages: list[ChatMessage]
