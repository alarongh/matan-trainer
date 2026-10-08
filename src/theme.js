export const THEME_KEY='trainer:theme:v1';
const themes=new Set(['sage','paper','lavender','night']);
export function loadTheme(storage,fallback='sage'){
 try{const saved=storage.getItem(THEME_KEY);if(themes.has(saved))return saved;}catch{}
 return themes.has(fallback)?fallback:'sage';
}
export function saveTheme(storage,name){
 if(!themes.has(name))return false;
 try{storage.setItem(THEME_KEY,name);return true;}catch{return false;}
}
