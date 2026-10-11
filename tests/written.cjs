const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const base=process.env.TEST_URL||'http://127.0.0.1:4173/';
async function main(){
 const browser=await chromium.launch({headless:true,channel:'msedge'});
 try{
  const context=await browser.newContext({viewport:{width:1440,height:1000}}),page=await context.newPage(),errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base);await page.locator('[data-task-id]').first().waitFor();
  await page.locator('#origin-filter').selectOption('textbook');
  assert.equal(await page.locator('#textbook-section option').count(),27);
  await page.locator('#textbook-section').selectOption('1');
  assert.equal(await page.locator('[data-task-id]').count(),30);
  await page.locator('[data-task-id="textbook-01-1"]').click();
  await page.locator('#answer').fill('800');await page.locator('#check-button').click();assert.match(await page.locator('#feedback').innerText(),/^Верно/);
  await page.locator('#textbook-section').selectOption('3');
  await page.locator('[data-task-id="textbook-03-1"]').click();
  assert.equal(await page.locator('#choices .katex').count(),3);
  assert.equal(await page.locator('#choices .katex-error').count(),0);
  await page.locator('#textbook-section').selectOption('20');
  assert.equal(await page.locator('[data-task-id]').count(),90);
  await page.locator('[data-task-id="textbook-20-4-full"]').click();
  assert.equal(await page.locator('#answer-row').isVisible(),false);
  assert.equal(await page.locator('#math-keyboard').isVisible(),false);
  assert.equal(await page.locator('#review-complete').count(),0);
  await page.locator('#written-notes').fill('Исключены x=1 и x=2, сокращение не возвращает их.');
  await page.reload();await page.locator('#written-notes').waitFor();
  assert.equal(await page.locator('#textbook-section').inputValue(),'20');
  assert.match(await page.locator('#written-notes').inputValue(),/Исключены/);
  await page.locator('#reveal').click();
  for(let i=1;i<7;i++)await page.locator('#next-step').click();
  assert.equal(await page.locator('.step').count(),7);
  assert.equal(await page.locator('#review-complete').isDisabled(),true);
  assert.equal(await page.locator('.graph-reference svg').count(),1);
  await page.locator('.graph-reference input[type="range"]').fill('8');
  for(const check of await page.locator('.written-checklist input').all())await check.check();
  await page.locator('#review-complete').click();
  assert.match(await page.locator('#feedback').innerText(),/Автоматическая оценка.*не выполнялась/);
  const item=await page.evaluate(()=>JSON.parse(localStorage.getItem('matan-trainer:v1')).items['textbook-20-4-full']);
  assert.equal(item.status,'assisted');assert.equal(item.draft,'');
  await page.screenshot({path:'test-results/written-desktop.png',fullPage:true});
  for(const width of [390,320]){
   await page.setViewportSize({width,height:844});
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'overflow at '+width);
   if(width===390)await page.screenshot({path:'test-results/written-mobile.png',fullPage:true});
  }
  await page.locator('#textbook-section').selectOption('23');
  await page.locator('[data-task-id="textbook-23-11"]').click();await page.locator('#reveal').click();
  for(let i=1;i<4;i++)await page.locator('#next-step').click();
  assert.equal(await page.locator('.graph-reference svg').count(),1);
  await page.locator('#restart-attempt').click();assert.equal(await page.locator('#written-notes').inputValue(),'');
  assert.equal(await page.locator('#solution').isVisible(),false);
  await page.locator('#textbook-section').selectOption('26');
  await page.locator('[data-task-id="textbook-26-1"]').click();
  for(const [id,value] of Object.entries({point:'(2/7;-13/7;-1)',value:'-36/7',type:'1'}))await page.locator('#field-'+id).fill(value);
  await page.locator('#answer-fields button[type="submit"]').click();assert.match(await page.locator('#feedback').innerText(),/^Верно/);
  await page.locator('#subject-select').selectOption('linear');await page.waitForURL(/subject=linear/);
  await page.locator('[data-task-id]').first().waitFor();assert.equal(await page.locator('#count-all').innerText(),'121');
  assert.equal(await page.locator('#textbook-section-row').isVisible(),false);
  assert.deepEqual(errors,[]);console.log('Written review passed: 26 sections, manual grading boundaries, notes, graph, checklist, assisted history, retry, 320 px and linear subject.');
 }finally{await browser.close();}
}
main().catch(e=>{console.error(e);process.exitCode=1;});
