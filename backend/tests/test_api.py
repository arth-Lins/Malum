from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)
CSV=b"data,etapa,volume_produzido,materia_prima_entrada,energia_kwh,custo_total_brl\n2026-01-01,Corte,10,12,5,20\n2026-01-02,Corte,10,30,5,20\n2026-01-03,Montagem,10,10,4,10\n"

def test_upload_and_analysis_contract():
    up=client.post('/upload',files={'file':('demo.csv',CSV,'text/csv')}); assert up.status_code==200
    body=up.json(); assert {'uploadId','preview','numericColumns'} <= body.keys()
    result=client.post('/analyze',json={'uploadId':body['uploadId'],'focus':'Onde há desperdício?'}); assert result.status_code==200
    assert {'focus','findings','estimatedWaste','attentionStage','indicator','layaAvailable'} <= result.json().keys()

def test_invalid_file_is_friendly():
    assert client.post('/upload',files={'file':('bad.txt',b'x','text/plain')}).status_code==422
