export type ChartType = 'bar'|'line'|'pie'|'histogram';
export type Preview = { fileName:string; rows: number; headers:string[]; preview:string[][] };
export type Finding = { id:string; stage:string; resource:string; value:number; reference:number; deviation:number; unit:string; cost:number; severity:'alta'|'média'|'baixa' };
export type Analysis = { dataset:{rows:number; period:string; quality:string}; focus:string; findings:Finding[]; estimatedWaste:string; attentionStage:string; indicator:string; layaAvailable:boolean };
export type ChatMessage = {id:string; role:'bot'|'user'; text:string; references?:string[]};
export interface AnalysisService { preview(file:File):Promise<Preview>; analyze(focus:string):Promise<Analysis> }
export interface ChatService { initial(analysis:Analysis):Promise<ChatMessage>; ask(question:string):Promise<ChatMessage> }
export interface AuthService { signIn(email:string,password:string):Promise<void>; signUp(name:string,email:string,password:string):Promise<void> }
