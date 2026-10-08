const {chromium}=require(process.env.PLAYWRIGHT_PATH||'playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const tasks=JSON.parse(fs.readFileSync(path.join(__dirname,'../data/tasks.json'),'utf8'));
const base=process.env.TEST_URL||'http://127.0.0.1:4173/';
const key='matan-trainer:v1';
async function main(){
 fs.mkdirSync('test-results',{recursive:true});
 const browser=await chromium.launch({headless:true,channel:process.env.BROWSER_CHANNEL||'msedge'});
 const context=await browser.newContext({viewport:{width:1440,height:1000}});
 const page=await context.newPage();const errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 page.on('response',r=>{if(r.status()>=400)errors.push(r.status()+' '+r.url());});
 await page.goto(base);await page.locator('[data-task-id]').first().waitFor();await page.evaluate(()=>document.fonts.ready);
 await page.screenshot({path:'test-results/desktop.png',fullPage:true});
 await page.locator('#open-settings').click();await page.locator('#auto-advance').uncheck();await page.locator('#settings-dialog .close-dialog').click();
 await page.locator('[data-group="2"]').click();
 await page.locator('[data-task-id="sequence-01"]').click();
 await page.locator('#answer').fill('oops');await page.locator('#check-button').click();
 let state=await page.evaluate(k=>JSON.parse(localStorage.getItem(k)),key);
 assert.equal(state.items['sequence-01'].attempts.length,0);
 await page.locator('#answer').fill('0');await page.locator('#check-button').click();
 assert.equal(await page.locator('.step').count(),1);assert.match(await page.locator('#steps .step:last-child h4').innerText(),/формулы/i);
 await page.locator('#next-step').click();assert.equal(await page.locator('.step').count(),2);
 await page.locator('#next-step').click();await page.locator('#next-step').click();assert.equal(await page.locator('.step').count(),4);
 await page.locator('#answer').fill('1/2');await page.locator('#check-button').click();
 assert.match(await page.locator('#feedback').innerText(),/Верно/);
 state=await page.evaluate(k=>JSON.parse(localStorage.getItem(k)),key);assert.equal(state.items['sequence-01'].status,'assisted');
 await page.reload();await page.locator('#answer').waitFor();assert.equal(await page.locator('#answer').inputValue(),'1/2');assert.equal(await page.locator('.step').count(),4);
 await page.locator('#next-step').click();assert.equal(await page.locator('.step').count(),0);
 await page.locator('#answer').fill('0,5');await page.locator('#check-button').click();
 assert.equal(await page.locator('#progress-number').innerText(),'1');
 await page.locator('[data-theme="night"]').click();await page.reload();await page.locator('[data-task-id]').first().waitFor();assert.equal(await page.locator('html').getAttribute('data-theme'),'night');
 await page.locator('#open-settings').click();const downloadPromise=page.waitForEvent('download');await page.locator('#export-progress').click();const download=await downloadPromise;await download.saveAs('test-results/progress.json');
 assert.equal(await page.locator('.history-entry').count(),3);
 await page.locator('#settings-dialog .close-dialog').click();
 const fresh=await browser.newContext();const imported=await fresh.newPage();await imported.goto(base);await imported.locator('[data-task-id]').first().waitFor();
 await imported.locator('#open-settings').click();await imported.locator('#import-file').setInputFiles('test-results/progress.json');await imported.locator('#settings-dialog').waitFor({state:'hidden'});
 const restored=await imported.evaluate(k=>JSON.parse(localStorage.getItem(k)),key);assert.equal(restored.items['sequence-01'].status,'solved');assert.equal(restored.items['sequence-01'].attempts.length,3);assert.equal(restored.theme,'night');
 await fresh.close();
 await page.locator('[data-theme="sage"]').click();await page.locator('[data-group="all"]').click();
 for(const task of tasks){
  await page.locator(`[data-task-id="${task.id}"]`).click();
  if(task.kind==='choice')await page.locator(`[data-choice="${task.answer}"]`).click();
  else{await page.locator('#answer').fill(task.answer);await page.locator('#check-button').click();}
  assert.match(await page.locator('#feedback').innerText(),/^Верно/,task.id);
  assert.equal(await page.locator('.katex-error').count(),0,task.id);
 }
 assert.equal(await page.locator('#progress-number').innerText(),'96');
 await page.locator('[data-task-id="extra-07"]').count().then(async n=>{if(n)await page.locator('[data-task-id="extra-07"]').click();});
 await page.locator('#open-formulas').click();assert.equal(await page.locator('.katex-error').count(),0);await page.locator('#formulas-dialog .close-dialog').click();
 await page.locator('#open-settings').click();await page.locator('#auto-advance').check();await page.locator('#settings-dialog .close-dialog').click();
 await page.locator('[data-task-id="sequence-02"]').click();await page.locator('#answer').fill('9/5');await page.locator('#check-button').click();await page.waitForTimeout(1400);assert.equal(await page.locator('[aria-current="true"]').getAttribute('data-task-id'),'sequence-03');
 for(const width of [1440,1024,768,390,320]){
  await page.setViewportSize({width,height:900});
  const dims=await page.evaluate(()=>({viewport:innerWidth,scroll:document.documentElement.scrollWidth}));assert.ok(dims.scroll<=dims.viewport+1,JSON.stringify(dims));
  if(width===390)await page.screenshot({path:'test-results/mobile.png',fullPage:true});
 }
 await page.setViewportSize({width:1440,height:1000});await page.evaluate(()=>document.body.style.zoom='2');
 assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'200% zoom overflow');
 assert.ok(await page.locator('#task-card').evaluate(e=>e.getBoundingClientRect().width>500),'200% zoom must keep the study card usable');
 await page.screenshot({path:'test-results/zoom.png',fullPage:true});await page.evaluate(()=>document.body.style.zoom='1');
 await page.locator('[data-theme="night"]').click();await page.screenshot({path:'test-results/night.png',fullPage:true});
 assert.deepEqual(errors,[]);
 await browser.close();console.log('Browser passed: 96 answers; progressive hints; persistence; export/import; navigation; formula rendering; 320–1440 px; 200% zoom; no page or HTTP errors.');
}
main().catch(e=>{console.error(e);process.exit(1);});
