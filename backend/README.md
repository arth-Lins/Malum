# Malum API

## Executar

```bash
cd backend
python -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
uvicorn app.main:app --reload
pytest
```

Variáveis: `LAYA_MODE=mock|local`, `DEEPSEEK_MODE=mock|api`, `DEEPSEEK_API_KEY`, `DEEPSEEK_BASE_URL` (padrão `https://api.deepseek.com`) e `DEEPSEEK_MODEL` (padrão `deepseek-flash`). Nunca exponha essas variáveis ao frontend.

O modo padrão é inteiramente mockado e determinístico. `LocalLayaClient` é deliberadamente um ponto TODO: a assinatura oficial de `choice` e `score` deve ser integrada depois de validar o runtime/modelo local.

## Divergência com o frontend

O frontend atual usa mocks e mantém o histórico no navegador; a API retorna o mesmo núcleo de `Analysis` e acrescenta evidências para rastreabilidade. A troca do serviço front-end para `api` continua isolada no adaptador já existente.

## Checklist

- [x] Ingestão, indicadores e anomalias determinísticos.
- [x] Clientes mock/real isolados e degradação Laya/DeepSeek.
- [x] Endpoints, contratos e amostras.
- [x] Script-base de benchmark e dados de três atividades.
- [ ] Laya local e métricas reais de F1/kappa/Spearman: dependem do modelo e benchmark real.
- [ ] DeepSeek real: depende de chave configurada.
