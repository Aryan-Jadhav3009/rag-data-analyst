export type Database={id:number|string;name:string}
export type QueryResult={success:boolean;question:string;sql:string;explanation:string;columns:string[];rows:unknown[][];error?:string}
export type ConnectionInput={name:string;host:string;port:string;database_name:string;username:string;password:string}
const base=process.env.NEXT_PUBLIC_API_BASE_URL||''
async function request<T>(path:string,options?:RequestInit):Promise<T>{const res=await fetch(`${base}${path}`,{...options,headers:{'Content-Type':'application/json',...(options?.headers||{})}});const data=await res.json().catch(()=>({error:'Invalid server response'}));if(!res.ok)throw new Error(data.error||'Request failed');return data}
export const api={listDatabases:()=>request<Database[]>('/api/databases/list/'),createDatabase:(input:ConnectionInput)=>request<{success:boolean;database_id:number|string;name:string;message?:string}>('/api/databases/',{method:'POST',body:JSON.stringify(input)}),query:(question:string,database_id:number|string)=>request<QueryResult>('/api/query/',{method:'POST',body:JSON.stringify({question,database_id})})}
