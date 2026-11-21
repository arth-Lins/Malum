# Malum — front-end MVP

Interface Next.js/TypeScript para a demonstração do Malum. Esta entrega é intencionalmente apenas visual e usa dados de marcenaria simulados; não há chamadas ao back-end, IA ou armazenamento de planilhas.

## Rodar

```bash
cd frontend
npm install
npm run dev
```

Abra `http://localhost:3000`. Para validar:

```bash
npm run test
npx playwright install
npm run test:e2e
npm run build
```

## Configuração

Crie `.env.local` se necessário:

```env
NEXT_PUBLIC_API_MODE=mock
```

`mock` é o padrão. A variável aceita `api`, mas o cliente HTTP ainda é um `TODO` deliberadamente isolado em `src/services/index.ts`; os contratos que ele deverá implementar estão em `src/services/contracts.ts`. Enquanto não houver implementação real, `api` preserva o mock para a demo.

## Tipografia

O CSS tenta carregar `public/fonts/DecimaMonoCyr.woff2` e `public/fonts/DecimaMonoBold.woff2`. Estes arquivos não acompanham o repositório por licença/disponibilidade. Coloque-os nesses caminhos para usar Decima; caso contrário, os fallbacks monoespaçados são aplicados. Montserrat e Noto Sans JP têm fallback `sans-serif` e podem ser adicionadas localmente da mesma forma.

## Decisões

- Gráficos são SVG/CSS nativos para manter a demo leve e acessível, com resumo textual para leitor de tela.
- O histórico de chats fica em `localStorage`, como especificado para o MVP; arquivos não são persistidos.
- Em telas estreitas, a análise alterna entre as abas Gráfico e Chat.
- O estado “análise incompleta” está modelado por `Analysis.layaAvailable`; a implementação mock padrão entrega Laya disponível. Quando o adaptador real a marcar indisponível, a UI deve mostrar o aviso do PRD e não solicitar diagnóstico ao chat. Isso depende da API e ficou como pendência desta etapa de front-end mockado.

## Divergências do pedido/PRD

Não há conflito substantivo. Como o escopo determina não implementar back-end, os critérios de aceite ligados à execução local da Laya e ao benchmark não foram implementados; estão abaixo como pendentes. O aviso de análise incompleta é um estado preparado no contrato, mas não é ativável pelo usuário na demo atual.

## Checklist de aceite do PRD (front-end)

- [x] Hero digita título e texto sequencialmente, mantém o conteúdo e respeita redução de movimento.
- [x] Entrar e cadastro dummy; cadastro valida visualmente e vai para preços.
- [x] Planos Semente, Oficina, Fábrica e Núcleo; destaque e aviso de valores demonstrativos.
- [x] Introdução, Quem somos, equipe AdaCore e âncoras.
- [x] Upload, prévia, planilha modelo, pergunta de foco e análise demonstrativa.
- [x] Alternância entre colunas, linha, pizza e histograma; descrição textual acessível.
- [x] DataMalum explica onde e como, citando etapa, recurso e indicador mockado.
- [x] Barra lateral recolhível, novo chat e histórico local.
- [x] Estados de carregamento e erros de arquivo; layout responsivo e foco visível.
- [x] Serviços mock com contratos e chave única para futura API.
- [x] Teste de componente e fluxo Playwright incluídos.
- [ ] Laya local/`choice`/`score`: é back-end, fora desta etapa.
- [ ] Benchmark Laya: é back-end/documentação experimental, fora desta etapa.
- [ ] Aviso de análise incompleta visível em cenário ativável: contrato pronto, aguardando estado de API/controle de demo.
