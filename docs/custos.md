# Custos e preço mínimo

`custo_por_análise = tokens_in × preço_in + tokens_out × preço_out + custo_compute + rateio_infra`

`preço_mínimo = (análises_incluídas × custo_por_análise × (1 + fator_chat)) ÷ (1 − margem_alvo − taxa_gateway)`

Os valores de planos no frontend são demonstrativos. Antes da publicação, preencher preço de entrada/saída vigente do DeepSeek, tamanho médio das evidências e custo real do servidor que executa Data Engine e Laya.
