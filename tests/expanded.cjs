const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const base=process.env.TEST_URL||'http://127.0.0.1:4173/';
async function main(){
 fs.mkdirSync('test-results',{recursive:true});
 const browser=await chromium.launch({headless:true,channel:'msedge'});
 const context=await browser.newContext({viewport:{width:1440,height:1000}});
 // Import the old v1 format before opening the expanded application.
 await context.addInitScript(()=>{
  if(!localStorage.getItem('matan-trainer:v1'))localStorage.setItem('matan-trainer:v1',JSON.stringify({version:1,theme:'sage',selected:'sequence-01',group:'2',origin:'all',mode:'all',autoAdvance:false,items:{'sequence-01':{status:'solved',step:0,draft:'1/2',attempts:[{answer:'1/2',correct:true,at:1}]}}}));
 });
 const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base);await page.locator('[data-task-id]').first().waitFor();
 assert.equal(await page.locator('[data-group]').count(),11);
 assert.equal(await page.locator('#count-all').innerText(),'426');
 assert.equal(await page.locator('#progress-number').innerText(),'1');
 assert.equal(await page.locator('#answer').inputValue(),'1/2');
 await page.locator('[data-group="6"]').click();await page.locator('[data-task-id="tangent-11"]').click();
 await page.locator('#field-line').fill('y=5-6x');await page.locator('#field-area').fill('49/12');await page.locator('#answer-fields button[type=submit]').click();
 assert.match(await page.locator('#feedback').innerText(),/Площадь/);assert.equal(await page.locator('.step').count(),1);
 await page.locator('#field-area').fill('25/12');await page.locator('#answer-fields button[type=submit]').click();assert.match(await page.locator('#feedback').innerText(),/^Верно/);
 await page.reload();await page.locator('#field-area').waitFor();assert.equal(await page.locator('#field-line').inputValue(),'y=5-6x');assert.equal(await page.locator('#field-area').inputValue(),'25/12');
 await page.locator('#field-area').click();await page.locator('[data-key="clear"]').click();await page.locator('[data-key="2"]').click();assert.equal(await page.locator('#field-area').inputValue(),'2');assert.equal(await page.locator('#field-line').inputValue(),'y=5-6x');
 await page.locator('[data-group="5"]').click();await page.locator('[data-task-id="function-theory-06"]').click();
 assert.ok(await page.locator('#choices button[type=submit]').evaluate(e=>{const s=getComputedStyle(e);return s.color!==s.backgroundColor;}),'Submit label must contrast with the button');
 await page.locator('#choices input[value="1"]').check();await page.locator('#choices button[type=submit]').click();assert.match(await page.locator('#feedback').innerText(),/неверно/);assert.equal(await page.locator('.step').count(),1);
 for(const v of ['2','3','4'])await page.locator(`#choices input[value="${v}"]`).check();await page.locator('#choices button[type=submit]').click();assert.match(await page.locator('#feedback').innerText(),/^Верно/);
 await page.locator('[data-group="8"]').click();await page.locator('[data-task-id="asymptote-29"]').click();await page.locator('#field-lines').fill('y=1; x=1');await page.locator('#answer-fields button[type=submit]').click();assert.match(await page.locator('#feedback').innerText(),/^Верно/);
 await page.locator('#reveal').click();for(let i=0;i<3;i++)await page.locator('#next-step').click();assert.equal(await page.locator('.katex-error').count(),0);
 await page.screenshot({path:'test-results/expanded-asymptotes.png',fullPage:true});
 await page.locator('[data-group="10"]').click();await page.locator('[data-task-id="practical-01"]').click();
 await page.locator('#field-speed').fill('20');await page.locator('#field-cost').fill('72000');
 for(const theme of ['sage','paper','lavender','night']){await page.locator(`button[data-theme="${theme}"]`).click();assert.equal(await page.locator('html').getAttribute('data-theme'),theme);}
 await page.locator('button[data-theme="sage"]').click();await page.screenshot({path:'test-results/expanded-practical-desktop.png',fullPage:true});
 for(const width of [1440,768,390,320]){
  await page.setViewportSize({width,height:900});
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'expanded field overflow '+width);
  for(const selector of ['#answer-fields','#math-keys'])assert.ok(await page.locator(selector).evaluate(e=>e.scrollWidth<=e.clientWidth+1),selector+' overflow '+width);
  if(width===390)await page.screenshot({path:'test-results/expanded-practical-mobile.png',fullPage:true});
 }
 await page.setViewportSize({width:1440,height:1000});await page.evaluate(()=>document.body.style.zoom='2');assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));await page.evaluate(()=>document.body.style.zoom='1');
 await page.locator('[data-group="5"]').click();await page.locator('[data-task-id="oral-28"]').click();await page.locator('#reveal').click();for(let i=0;i<3;i++)await page.locator('#next-step').click();assert.equal(await page.locator('.katex-error').count(),0);
 await page.screenshot({path:'test-results/expanded-theory.png',fullPage:true});
 await page.locator('#open-sources').click();assert.equal(await page.locator('.source-issue').count(),12);await page.locator('.source-issue').first().click();assert.equal(await page.locator('#sources-dialog').isVisible(),false);
 const old=await page.evaluate(()=>JSON.parse(localStorage.getItem('matan-trainer:v1')).items['sequence-01']);assert.equal(old.attempts.length,1);assert.equal(old.status,'solved');
 assert.deepEqual(errors,[]);await browser.close();console.log('Expanded flows passed: old history, 10 sections, multiple fields and keyboard target, wrong-field feedback, multiple statements, lines, all themes, 320px/200% zoom, oral theory and source issues.');
}
main().catch(e=>{console.error(e);process.exit(1)});
