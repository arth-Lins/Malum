# Contratos da API

`POST /upload` recebe `multipart/form-data` com `file` e retorna `uploadId`, `preview` (`fileName`, `rows`, `headers`, `preview`) e `numericColumns`.

`POST /analyze` recebe `{ "uploadId", "focus" }`. Os campos principais da resposta correspondem ao frontend: `dataset`, `focus`, `findings`, `estimatedWaste`, `attentionStage`, `indicator` e `layaAvailable`. A resposta também inclui `evidence`, `laya`, `warning` e `explanation` para rastreabilidade.

`POST /chat` recebe `{ "analysisId", "question" }` e retorna uma mensagem `{ id, role, text, references }`. `GET /chats` retorna os registros mantidos em memória no MVP.

Quando Laya falha, `layaAvailable=false`, há `warning` e não há `explanation`. Quando DeepSeek falha, Laya e evidências continuam presentes e `warning` explica a nova tentativa.
