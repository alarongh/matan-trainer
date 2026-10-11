const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const tasks=JSON.parse(fs.readFileSync('data/physics-tasks.json','utf8'));
const base=process.env.TEST_URL||'http://127.0.0.1:4173/';
async function main(){
 const {formulaBanks}=await import('../src/formula-bank.js');
 const browser=await chromium.launch({headless:true,channel:'msedge'});
 const context=await browser.newContext({viewport:{width:1440,height:1000}});
 const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));page.setDefaultTimeout(15000);
 fs.mkdirSync('test-results',{recursive:true});
 const state=()=>page.evaluate(()=>JSON.parse(localStorage.getItem('physics-trainer:v1')));
 async function ready(){await page.locator('[data-task-id]').first().waitFor({state:'attached'});}
 async function select(task){await page.locator('#search').fill('');await page.locator(`[data-task-id="${task.id}"]`).click();await page.waitForFunction(id=>JSON.parse(localStorage.getItem('physics-trainer:v1')).selected===id,task.id);}
 async function fillTask(task){
  if(task.kind==='fields'){const values=JSON.parse(task.answer);for(const f of task.fields)await page.locator('#field-'+f.id).fill(values[f.id]);await page.locator('#answer-fields button[type=submit]').click();}
  else if(task.kind==='choice')await page.locator(`[data-choice="${task.answer}"]`).click();
  else{await page.locator('#answer').fill(task.answer);await page.locator('#check-button').click();}
 }
 async function fillFormula(parts){const round=await page.evaluate(()=>JSON.parse(localStorage.getItem('formula-quiz:physics:v1')).round);for(let i=0;i<parts.length;i++){await page.locator(`[data-slot="${i}"]`).click();await page.locator(`[data-piece="${round.choices.indexOf(parts[i])}"]`).click();}}
 try{
  await page.goto(new URL('?subject=physics',base).href);await ready();
  assert.equal(await page.locator('#count-all').innerText(),'251');
  assert.equal(await page.locator('.mobile-tools').isVisible(),false,'mobile footer stays hidden on desktop');
  await page.locator('#open-settings').click();await page.locator('#auto-advance').uncheck();await page.locator('#settings-dialog .close-dialog').click();
  const simple=tasks.find(t=>t.id==='ph-problem-2-3');await select(simple);
  await page.locator('#answer').fill('-1000');await page.locator('#check-button').click();
  assert.match(await page.locator('#feedback').innerText(),/неверно/);assert.equal(await page.locator('#steps .step').count(),1);
  for(let count=2;count<=4;count++){await page.locator('#next-step').click();assert.equal(await page.locator('#steps .step').count(),count);}
  await page.locator('#restart-attempt').click();assert.equal(await page.locator('#answer').inputValue(),'');assert.equal(await page.locator('#solution').isVisible(),false);
  await page.locator('#answer').fill('9/2');await page.locator('#check-button').click();assert.match(await page.locator('#feedback').innerText(),/^Верно/);
  await page.locator('#next').click();await select(simple);assert.equal(await page.locator('#answer').inputValue(),'');
  await page.locator('#answer').fill('4,5');await page.locator('#check-button').click();assert.match(await page.locator('#feedback').innerText(),/^Верно/);
  const specimens=[tasks.find(t=>t.kind==='fields'),tasks.find(t=>t.kind==='expression'),tasks.find(t=>t.kind==='choice')];
  for(const task of specimens){await select(task);await fillTask(task);assert.match(await page.locator('#feedback').innerText(),/^Верно/,task.id);}
  const review=tasks.find(t=>t.kind==='review');await select(review);assert.equal(await page.locator('#answer-row').isVisible(),false);assert.ok(await page.locator('#written-notes').isVisible());
  await page.locator('#reveal').click();for(let count=2;count<=4;count++)await page.locator('#next-step').click();
  await page.locator('.written-checklist input').evaluateAll(inputs=>inputs.forEach(input=>input.click()));await page.locator('#review-complete').click();
  assert.equal((await state()).items[review.id].status,'assisted');
  const diagram=tasks.find(t=>t.stages.some(s=>s.blocks.some(b=>b.physicsDiagram)));await select(diagram);await page.locator('#reveal').click();for(let count=2;count<=4;count++)await page.locator('#next-step').click();assert.ok(await page.locator('.physics-diagram svg').count());
  await page.locator('#show-quiz').click();assert.equal(await page.locator('.quiz-topic input').count(),10);await page.locator('#quiz-auto-next').uncheck();await page.locator('#quiz-start').click();
  let round=await page.evaluate(()=>JSON.parse(localStorage.getItem('formula-quiz:physics:v1')).round);const formula=formulaBanks.physics.find(f=>f.id===round.id);
  const wrong=[...formula.parts];wrong[0]=formula.wrong[0];await fillFormula(wrong);await page.locator('#quiz-check').click();assert.equal(await page.locator('#quiz-solution .step').count(),1);
  for(let count=2;count<=4;count++)await page.locator('#quiz-next-step').click();await fillFormula(formula.parts);await page.locator('#quiz-check').click();assert.match(await page.locator('#quiz-feedback').innerText(),/^Верно/);
  await page.locator('#quiz-next').click();const before=await state();await page.reload();await ready();assert.deepEqual(await state(),before);
  await page.setViewportSize({width:390,height:844});assert.equal(await page.locator('.mobile-tools').isVisible(),true);
  const positions=await page.evaluate(()=>({formulas:document.querySelector('#mobile-formulas').getBoundingClientRect().bottom,themes:document.querySelector('.mobile-themes').getBoundingClientRect().top}));assert.ok(positions.themes>positions.formulas);
  await page.locator('#mobile-formulas').click();assert.equal(await page.locator('#formula-content section').count(),83);assert.equal(await page.locator('.katex-error').count(),0);await page.locator('#formulas-dialog .close-dialog').click();
  for(const width of [320,390,768]){await page.setViewportSize({width,height:844});assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'overflow '+width);}
  await page.setViewportSize({width:390,height:844});
  for(const subject of ['matan','linear','physics']){
   await page.locator('[data-mobile-theme="lavender"]').click();await page.locator('#subject-select').selectOption(subject);await ready();assert.equal(await page.locator('html').getAttribute('data-theme'),'lavender');
   await page.locator('[data-mobile-theme="night"]').click();await page.reload();await ready();assert.equal(await page.locator('html').getAttribute('data-theme'),'night');
   assert.equal(await page.locator('[data-mobile-theme="night"]').getAttribute('aria-pressed'),'true');
  }
  await page.locator('.mobile-tools').screenshot({path:'test-results/mobile-theme-physics.png'});
  await page.locator('#show-tasks').click();await select(simple);await page.screenshot({path:'test-results/physics-mobile.png'});
  await page.setViewportSize({width:1440,height:1000});await page.locator('[data-theme="sage"]').click();assert.equal(await page.locator('.mobile-tools').isVisible(),false);await page.screenshot({path:'test-results/physics-desktop.png'});
  await page.evaluate(()=>document.body.style.zoom='2');assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'200% zoom overflow');
  assert.deepEqual(errors,[]);
  console.log('Physics/mobile browser checks passed: numeric fractions and comma, structured and parameter answers, gradual hints and reset, manual review, diagrams, formula wave, progress reload, shared themes across 3 subjects, 320/390/768px and 200% zoom.');
 }finally{await browser.close();}
}
main().catch(error=>{console.error(error);process.exit(1);});
