import {mockAnalysisService,mockAuthService,mockChatService} from './mock';
// TODO(api): conecte clientes HTTP que implementem estes contratos quando NEXT_PUBLIC_API_MODE=api.
const mode=process.env.NEXT_PUBLIC_API_MODE ?? 'mock';
if(mode === 'api') console.warn('API mode ainda não conectado; usando demo mock.');
export const services={analysis:mockAnalysisService,chat:mockChatService,auth:mockAuthService};
