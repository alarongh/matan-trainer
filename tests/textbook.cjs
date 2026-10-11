const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const tasks=JSON.parse(fs.readFileSync('data/tasks.json','utf8'));
const base=process.env.TEST_URL||'http://127.0.0.1:4173/';
async function main(){
 fs.mkdirSync('test-results',{recursive:true});
 const browser=await chromium.launch({headless:true,channel:'msedge'});
 try{
  const context=await browser.newContext({viewport:{width:1440,height:1000}});
  await context.addInitScript(()=>{
   if(!localStorage.getItem('matan-trainer:v1'))localStorage.setItem('matan-trainer:v1',JSON.stringify({version:1,theme:'lavender',selected:'sequence-01',group:'all',origin:'all',mode:'all',autoAdvance:false,items:{'sequence-01':{status:'solved',step:0,draft:'',attempts:[{answer:'1/2',correct:true,at:1}]}}}));
  });
  const page=await context.newPage(),errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base);await page.locator('[data-task-id]').first().waitFor();
  await page.locator('#origin-filter').selectOption('textbook');
  assert.equal(await page.locator('[data-task-id]').count(),747);
  await page.locator('[data-group="3"]').click();
  assert.equal(await page.locator('[data-task-id]').count(),120);
  await page.locator('[data-task-id="textbook-07-13"]').click();
  assert.match(await page.locator('#source-links').innerText(),/Задача 7.*пример 13/);
  assert.match(await page.locator('#source-links a').first().getAttribute('href'),/textbook\.pdf#page=22$/);
  await page.locator('#answer').fill('sqrt(3/2)');await page.locator('#check-button').click();
  assert.match(await page.locator('#feedback').innerText(),/неверно/);
  assert.equal(await page.locator('.step').count(),1);
  await page.locator('#next-step').click();assert.equal(await page.locator('.step').count(),2);
  await page.locator('#restart-attempt').click();
  assert.equal(await page.locator('#answer').inputValue(),'');
  assert.equal(await page.locator('#solution').isVisible(),false);
  await page.locator('#answer').fill('sqrt(2/3)');await page.locator('#check-button').click();
  assert.match(await page.locator('#feedback').innerText(),/^Верно/);
  await page.locator('#next').click();
  assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('matan-trainer:v1')).selected),'textbook-07-14');
  await page.locator('[data-task-id="textbook-07-13"]').click();
  assert.equal(await page.locator('#answer').inputValue(),'');
  await page.reload();await page.locator('[data-task-id="textbook-07-13"]').waitFor();
  assert.equal(await page.locator('#origin-filter').inputValue(),'textbook');
  const old=await page.evaluate(()=>JSON.parse(localStorage.getItem('matan-trainer:v1')).items['sequence-01']);
  assert.equal(old.status,'solved');assert.equal(old.attempts.length,1);
  await page.locator('[data-group="6"]').click();await page.locator('[data-task-id="textbook-14-24"]').click();
  const task=tasks.find(t=>t.id==='textbook-14-24');
  for(const f of task.fields)await page.locator('#field-'+f.id).fill(f.answer);
  await page.locator('#answer-fields button[type="submit"]').click();
  assert.match(await page.locator('#feedback').innerText(),/^Верно/);
  await page.locator('#reveal').click();
  for(let i=1;i<task.stages.length;i++)await page.locator('#next-step').click();
  assert.equal(await page.locator('.katex-error').count(),0);
  await page.screenshot({path:'test-results/textbook-desktop.png',fullPage:true});
  for(const width of [768,390,320]){
   await page.setViewportSize({width,height:844});
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'overflow '+width);
   if(width===390)await page.screenshot({path:'test-results/textbook-mobile.png',fullPage:true});
  }
  await page.setViewportSize({width:1440,height:1000});await page.evaluate(()=>document.body.style.zoom='2');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  await page.evaluate(()=>document.body.style.zoom='1');
  await page.locator('#subject-select').selectOption('linear');
  await page.waitForURL(/subject=linear/);await page.locator('[data-task-id]').first().waitFor();
  assert.equal(await page.locator('#origin-filter option[value="textbook"]').count(),0);
  assert.equal(await page.locator('#count-all').innerText(),'121');
  await page.locator('#subject-select').selectOption('matan');
  await page.waitForURL(url=>!url.searchParams.has('subject'));
  await page.locator('[data-task-id]').first().waitFor();
  assert.equal(await page.locator('#origin-filter').inputValue(),'textbook');
  assert.deepEqual(errors,[]);
  const pdf=await page.request.get(new URL('sources/textbook.pdf',base).href);assert.equal(pdf.status(),200);assert.ok((await pdf.body()).subarray(0,5).equals(Buffer.from('%PDF-')));
  console.log('Textbook browser checks passed: filters, retake examples, wrong/correct answers, staged hints, retry clearing, next task, old/new history, fields, 320px and 200%, linear subject, PDF.');
 }finally{await browser.close();}
}
main().catch(e=>{console.error(e);process.exit(1)});
