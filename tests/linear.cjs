const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const tasks=JSON.parse(fs.readFileSync('data/linear-tasks.json','utf8'));
const smokeIds=new Set(['la-example-01','la-example-07','la-example-15','la-example-19','la-example-29','la-example-30','la-example-31','la-example-32','la-example-33','la-example-35','la-example-39','la-example-41','la-example-46','la-example-50','la-example-55','la-example-56','la-example-60','la-oral-30','la-ticket-1-6','la-ticket-2-8']);
const checkedTasks=process.env.TEST_SMOKE?tasks.filter(t=>smokeIds.has(t.id)):tasks;
const base=process.env.TEST_URL||'http://127.0.0.1:4173/';
async function main(){
 fs.mkdirSync('test-results',{recursive:true});
 const browser=await chromium.launch({headless:true,channel:'msedge'});
 const context=await browser.newContext({viewport:{width:1440,height:1000},acceptDownloads:true});
 await context.addInitScript(()=>{if(!localStorage.getItem('matan-trainer:v1'))localStorage.setItem('matan-trainer:v1',JSON.stringify({version:1,theme:'night',selected:'sequence-10',group:'2',origin:'all',mode:'all',autoAdvance:false,items:{'sequence-10':{status:'solved',step:0,draft:'5',attempts:[{answer:'5',correct:true,at:1}]}}}));});
 const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));page.setDefaultTimeout(15000);
 async function select(id){await page.locator(`[data-task-id="${id}"]`).click();}
 async function enter(task){
  if(task.kind==='choice')await page.locator(`[data-choice="${task.answer}"]`).click();
  else if(task.kind==='multi'){for(const value of task.answer.split(';'))await page.locator(`#choices input[value="${value}"]`).check();await page.locator('#choices button[type=submit]').click();}
  else if(task.kind==='fields'){for(const field of task.fields)await page.locator('#field-'+field.id).fill(field.answer);await page.locator('#answer-fields button[type=submit]').click();}
  else{await page.locator('#answer').fill(task.answer);await page.locator('#check-button').click();}
  assert.match(await page.locator('#feedback').innerText(),/^Верно/,task.id);
 }
 try{
  await page.goto(base);await page.locator('[data-task-id]').first().waitFor();
  const calculus=await page.evaluate(()=>localStorage.getItem('matan-trainer:v1'));
  assert.equal(await page.locator('#count-all').innerText(),'426');
  await page.locator('#subject-select').selectOption('linear');await page.locator('[data-task-id="la-example-01"]').waitFor();
  assert.equal(await page.locator('#count-all').innerText(),'121');
  await page.locator('#open-settings').click();await page.locator('#auto-advance').uncheck();await page.locator('#settings-dialog .close-dialog').click();
  await page.locator('#field-inverse').fill('1 0;0 1');await page.locator('#field-result').fill('1 0 -3;0 -2 -1');await page.locator('#answer-fields button[type=submit]').click();
  assert.match(await page.locator('#feedback').innerText(),/Обратная матрица/);assert.equal(await page.locator('.step').count(),1);
  await page.locator('#field-inverse').fill('3 -2;1 -1');await page.locator('#answer-fields button[type=submit]').click();assert.match(await page.locator('#feedback').innerText(),/^Верно/);
  await page.reload();await page.locator('#field-inverse').waitFor();assert.equal(await page.locator('#field-inverse').inputValue(),'');
  assert.equal(await page.evaluate(()=>localStorage.getItem('matan-trainer:v1')),calculus);
  await page.locator('#subject-select').selectOption('matan');await page.locator('[data-task-id="sequence-10"]').waitFor();
  assert.equal(await page.locator('#answer').inputValue(),'');assert.equal(await page.locator('html').getAttribute('data-theme'),'night');
  assert.equal(await page.evaluate(()=>localStorage.getItem('matan-trainer:v1')),calculus);
  await page.locator('#subject-select').selectOption('linear');await page.locator('#field-inverse').waitFor();assert.equal(await page.locator('#field-inverse').inputValue(),'');
  await page.locator('[data-mode="new"]').click();await select('la-example-07');await enter(tasks.find(t=>t.id==='la-example-07'));await page.locator('#next').click();
  assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('linear-trainer:v1')).selected),'la-example-08');
  await page.locator('[data-group="all"]').click();await page.locator('[data-mode="all"]').click();
  let count=0;
  for(const task of checkedTasks){
   await select(task.id);await enter(task);
   await page.locator('#reveal').click();while(await page.locator('.step').count()<task.stages.length)await page.locator('#next-step').click();
   assert.equal(await page.locator('.step').count(),task.stages.length,task.id);assert.equal(await page.locator('.katex-error').count(),0,task.id);
   count++;if(count%25===0)console.log(`Checked ${count}/${checkedTasks.length} linear cards with answers and stages.`);
  }
  await select('la-example-30');await page.screenshot({path:'test-results/linear-conic-desktop.png',fullPage:true});assert.equal(await page.locator('.solution-graph svg').count(),1);
  await select('la-example-41');await page.screenshot({path:'test-results/linear-roots-desktop.png',fullPage:true});assert.equal(await page.locator('.solution-graph circle').count(),4);
  await select('la-example-01');await page.locator('#field-result').click();await page.locator('[data-linear-key=";"]').click();assert.match(await page.locator('#field-result').inputValue(),/;/);
  for(const theme of ['sage','paper','lavender','night']){await page.locator(`button[data-theme="${theme}"]`).click();assert.equal(await page.locator('html').getAttribute('data-theme'),theme);}
  for(const width of [1440,768,390,320]){
   await page.setViewportSize({width,height:900});assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'page overflow '+width);
   assert.ok(await page.locator('#math-keys').evaluate(e=>e.scrollWidth<=e.clientWidth+1),'keyboard overflow '+width);
   if(width===390)await page.screenshot({path:'test-results/linear-matrix-mobile.png',fullPage:true});
  }
  await page.setViewportSize({width:1440,height:1000});await page.evaluate(()=>document.body.style.zoom='2');assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));await page.evaluate(()=>document.body.style.zoom='1');
  await page.locator('#open-formulas').click();assert.equal(await page.locator('.formula-section').count(),12);assert.equal(await page.locator('.katex-error').count(),0);await page.locator('#formulas-dialog .close-dialog').click();
  await page.locator('#open-sources').click();assert.equal(await page.locator('.source-document').count(),3);assert.equal(await page.locator('.source-issue').count(),7);await page.locator('#sources-dialog .close-dialog').click();
  await page.locator('#open-settings').click();const download=page.waitForEvent('download');await page.locator('#export-progress').click();const file=await download;const downloaded=JSON.parse(fs.readFileSync(await file.path(),'utf8'));assert.equal(downloaded.subject,'linear');
  await page.locator('#import-file').setInputFiles({name:'matan.json',mimeType:'application/json',buffer:Buffer.from(calculus)});await page.waitForFunction(()=>document.querySelector('#import-message').textContent.includes('другого предмета'));assert.match(await page.locator('#import-message').innerText(),/другого предмета/);
  await page.locator('#import-file').setInputFiles({name:'linear.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(downloaded))});await page.waitForFunction(()=>!document.querySelector('#settings-dialog').open);
  assert.equal(await page.evaluate(()=>localStorage.getItem('matan-trainer:v1')),calculus);
  await page.locator('#open-settings').click();await page.locator('#settings-dialog details summary').click();page.once('dialog',d=>d.accept());await page.locator('#reset-progress').click();
  assert.equal(await page.evaluate(()=>Object.keys(JSON.parse(localStorage.getItem('linear-trainer:v1')).items).filter(id=>JSON.parse(localStorage.getItem('linear-trainer:v1')).items[id].attempts.length).length),0);
  assert.equal(await page.evaluate(()=>localStorage.getItem('matan-trainer:v1')),calculus);
  await page.locator('#subject-select').selectOption('matan');await page.locator('[data-task-id="sequence-10"]').waitFor();
  await page.locator('#open-settings').click();await page.locator('#import-file').setInputFiles({name:'linear.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(downloaded))});await page.waitForFunction(()=>document.querySelector('#import-message').textContent.includes('другого предмета'));assert.match(await page.locator('#import-message').innerText(),/другого предмета/);
  await page.locator('#import-file').setInputFiles({name:'old-matan.json',mimeType:'application/json',buffer:Buffer.from(calculus)});await page.waitForFunction(()=>!document.querySelector('#settings-dialog').open);
  assert.equal(await page.evaluate(()=>localStorage.getItem('matan-trainer:v1')),calculus);
  assert.deepEqual(errors,[]);console.log(`Linear browser QA passed: ${checkedTasks.length} answers/stages, subject isolation, reload, export/import/reset, keyboard, graphs, formulas, sources, themes, 320px and 200% zoom.`);
 }finally{await browser.close();}
}
main().catch(e=>{console.error(e);process.exit(1)});
