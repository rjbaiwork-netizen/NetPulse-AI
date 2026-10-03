import type {Alarm,Customer,CustomerLocation,Device,ONUPollRequest,ONUTelemetry} from "@/types/api";
export const BUILD_API_BASE_URL=(process.env.NEXT_PUBLIC_API_BASE_URL||"").replace(/\/$/,"");
export function getApiBaseUrl():string{if(typeof window!=="undefined"){const runtime=localStorage.getItem("netpulse_api_base_url");if(runtime?.trim())return runtime.trim().replace(/\/$/,"")}return BUILD_API_BASE_URL}
export class ApiError extends Error{constructor(public status:number,message:string){super(message)}}
async function request<T>(path:string,init?:RequestInit):Promise<T>{const base=getApiBaseUrl();if(!base)throw new ApiError(0,"Backend URL is not configured. Set the FastAPI Backend URL on the login screen.");const token=typeof window!=="undefined"?sessionStorage.getItem("netpulse_access_token"):null;const res=await fetch(base+path,{...init,headers:{"Content-Type":"application/json",...(token?{"Authorization":"Bearer "+token}:{}),...(init?.headers||{})},cache:"no-store"});if(!res.ok){let msg="Request failed ("+res.status+")";try{const b=await res.json();msg=b.detail||b.message||msg}catch{}throw new ApiError(res.status,msg)}return res.status===204?undefined as T:res.json()}
export const api={
login:(username:string,password:string)=>request<{access_token:string;token_type:string;role:string}>("/api/v1/auth/login",{method:"POST",body:JSON.stringify({username,password})}),
me:()=>request("/api/v1/auth/me"),
devices:()=>request<Device[]>("/api/v1/devices"),
createDevice:(body:Record<string,unknown>)=>request<Device>("/api/v1/devices",{method:"POST",body:JSON.stringify(body)}),
customers:(q?:string)=>request<Customer[]>("/api/v1/customers"+(q?"?q="+encodeURIComponent(q):"")),
createCustomer:(body:Record<string,unknown>)=>request<Customer>("/api/v1/customers",{method:"POST",body:JSON.stringify(body)}),
updateCustomer:(id:number,body:Record<string,unknown>)=>request<Customer>("/api/v1/customers/"+id,{method:"PATCH",body:JSON.stringify(body)}),
customerLocations:(id:number)=>request<CustomerLocation[]>("/api/v1/customers/"+id+"/locations"),
updateCustomerLocation:(id:number,body:Record<string,unknown>)=>request<CustomerLocation>("/api/v1/customers/"+id+"/location",{method:"POST",body:JSON.stringify(body)}),
pppoeSecrets:(id:number)=>request<unknown[]>("/api/v1/mikrotik/"+id+"/pppoe/secrets"),
activeSessions:(id:number)=>request<unknown[]>("/api/v1/mikrotik/"+id+"/pppoe/active"),
oltMonitor:(id:number)=>request<{telemetry:unknown;fault:string}>("/api/v1/olt/"+id+"/monitor"),
alarms:()=>request<Alarm[]>("/api/v1/alarms").catch(()=>[]),
kick:(id:number,username:string)=>request("/api/v1/mikrotik/"+id+"/pppoe/kick",{method:"POST",body:JSON.stringify({username})}),
speed:(id:number,username:string,download_bps:number,upload_bps:number)=>request("/api/v1/mikrotik/"+id+"/pppoe/speed",{method:"POST",body:JSON.stringify({username,download_bps,upload_bps})}),
pollOnu:(p:ONUPollRequest)=>request<ONUTelemetry>("/api/v1/olt/onu/poll",{method:"POST",body:JSON.stringify(p)}),
aiCommand:(command:string)=>request<{intent:{name:string;parameters:Record<string,unknown>};success:boolean;result:unknown;message:string;audit_id:number}>("/api/v1/ai-noc/command",{method:"POST",body:JSON.stringify({command})})
};
