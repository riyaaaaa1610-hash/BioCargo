export type UserRole='Admin'|'Airport Operator'|'Medical Logistics Officer';
export type User={username:string,password:string,role:UserRole};
const KEY='biocargo_users'; const CUR='biocargo_current_user';
const DEFAULT=[{username:'admin',password:'biocargo123',role:'Admin'},{username:'operator',password:'operator123',role:'Airport Operator'},{username:'medical',password:'medical123',role:'Medical Logistics Officer'}];
export const getUsers=()=>JSON.parse(localStorage.getItem(KEY)||JSON.stringify(DEFAULT));
export const saveUser=(u:User)=>{const users=getUsers(); if(users.find((x:any)=>x.username===u.username)) throw Error('Username exists'); users.push(u); localStorage.setItem(KEY,JSON.stringify(users));};
export const login=(u:string,p:string)=>{const user=getUsers().find((x:any)=>x.username.toLowerCase()===u.toLowerCase()&&x.password===p); if(user){localStorage.setItem(CUR,user.username); localStorage.setItem('biocargo_role',user.role); return user;} return null;};
export const logout=()=>{localStorage.removeItem(CUR); localStorage.removeItem('biocargo_role');};
