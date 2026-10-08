const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const base=process.env.TEST_URL||'http://127.0.0.1:4173/';
async function main(){
 const browser=await chromium.launch({headless:true,channel:'msedge'});
 const context=await browser.newContext({viewport:{width:1440,height:1000}});
 const page=await context.newPage(),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 const item={status:'solved',step:0,draft:'5',attempts:[{answer:'5',correct:true,at:1}]};
 const matan={version:1,theme:'night',selected:'sequence-10',group:'2',origin:'all',mode:'all',autoAdvance:false,items:{'sequence-10':item}};
 const linear={...matan,theme:'paper',selected:'la-example-07',group:'all',items:{'la-example-07':{...item,draft:'1'}}};
 async function ready(p=page){await p.locator('#theme-select').waitFor({state:'attached'});await p.locator('[data-task-id]').first().waitFor();}
 async function hasTheme(name,p=page){await p.waitForFunction(n=>document.documentElement.dataset.theme===n,name);assert.equal(await p.locator('#theme-select').inputValue(),name);assert.equal(await p.locator(`button[data-theme="${name}"]`).getAttribute('aria-pressed'),'true');}
 async function switchTo(subject){await page.locator('#subject-select').selectOption(subject);await page.waitForFunction(s=>document.querySelector('#subject-select').value===s,subject);await ready();}
 async function progress(key){return page.evaluate(k=>JSON.parse(localStorage.getItem(k)).items,key);}
 try{
  await page.goto(base);await ready();
  await page.evaluate(({matan,linear})=>{localStorage.clear();localStorage.setItem('matan-trainer:v1',JSON.stringify(matan));localStorage.setItem('linear-trainer:v1',JSON.stringify(linear));},{matan,linear});
  await page.reload();await ready();await hasTheme('night');
  assert.equal(await page.evaluate(()=>localStorage.getItem('trainer:theme:v1')),'night');
  await switchTo('linear');await hasTheme('night');
  for(const name of ['sage','paper','lavender','night']){
   await page.locator(`button[data-theme="${name}"]`).click();
   await switchTo('matan');await hasTheme(name);
   await page.reload();await ready();await hasTheme(name);
   await switchTo('linear');await hasTheme(name);
  }
  await page.locator('#open-settings').click();await page.locator('#theme-select').selectOption('lavender');await page.locator('#settings-dialog .close-dialog').click();
  await switchTo('matan');await hasTheme('lavender');
  assert.deepEqual(await progress('matan-trainer:v1'),matan.items);
  assert.deepEqual(await progress('linear-trainer:v1'),linear.items);
  assert.equal(await page.locator('#answer').inputValue(),'5');
  // Importing an old progress file must not restore its subject-specific theme.
  await page.locator('#open-settings').click();
  await page.locator('#import-file').setInputFiles({name:'old-progress.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(matan))});
  await page.waitForFunction(()=>!document.querySelector('#settings-dialog').open);await hasTheme('lavender');
  await page.setViewportSize({width:390,height:844});await page.locator('#mobile-settings').click();
  await page.locator('#theme-select').selectOption('paper');await page.locator('#settings-dialog .close-dialog').click();
  await switchTo('linear');await hasTheme('paper');
  // An already-open subject receives the same preference through the storage event.
  const other=await context.newPage();other.on('pageerror',e=>errors.push(e.message));await other.goto(base);await ready(other);await hasTheme('paper',other);
  const storedMatan=await page.evaluate(()=>localStorage.getItem('matan-trainer:v1'));
  await page.locator('#mobile-settings').click();await page.locator('#theme-select').selectOption('sage');await page.locator('#settings-dialog .close-dialog').click();await hasTheme('sage',other);
  assert.equal(await page.evaluate(()=>localStorage.getItem('matan-trainer:v1')),storedMatan,'A background tab must not rewrite study history when receiving a theme.');
  await page.locator('#mobile-settings').click();await page.locator('#settings-dialog details summary').click();page.once('dialog',d=>d.accept());await page.locator('#reset-progress').click();await hasTheme('sage');
  await page.reload();await ready();await hasTheme('sage');await switchTo('matan');await hasTheme('sage');
  assert.deepEqual(await progress('matan-trainer:v1'),matan.items);assert.deepEqual(errors,[]);
  console.log('Shared theme passed: legacy migration, all four themes, both subjects, reload, settings, mobile, old imports, reset, cross-tab sync and intact study progress.');
 }finally{await browser.close();}
}
main().catch(e=>{console.error(e);process.exit(1)});
