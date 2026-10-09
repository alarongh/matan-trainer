const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const base=process.env.TEST_URL||'http://127.0.0.1:4173/';
async function main(){
 const browser=await chromium.launch({headless:true,channel:'msedge'});
 const context=await browser.newContext({viewport:{width:1440,height:1000}});
 const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await context.addInitScript(()=>{if(!localStorage.getItem('matan-trainer:v1'))localStorage.setItem('matan-trainer:v1',JSON.stringify({version:1,theme:'sage',selected:'sequence-01',group:'all',origin:'all',mode:'all',autoAdvance:false,items:{}}));});
 async function correct(){assert.match(await page.locator('#feedback').innerText(),/^Верно/);}
 try{
  await page.goto(base);await page.locator('[data-task-id="sequence-01"]').waitFor();
  for(const input of ['1/2','0.5','0,5']){await page.locator('#answer').fill(input);await page.locator('#check-button').click();await correct();}
  await page.locator('#answer').fill('0,6');await page.locator('#check-button').click();assert.match(await page.locator('#feedback').innerText(),/неверно/);
  await page.locator('#subject-select').selectOption('linear');await page.locator('[data-task-id="la-example-07"]').waitFor();
  await page.locator('#open-settings').click();await page.locator('#auto-advance').uncheck();await page.locator('#settings-dialog .close-dialog').click();await page.locator('[data-task-id="la-example-07"]').click();
  const variants=[['3/2 1/2;2 1','27/2 -13/2;19 -11'],['1.5 0.5;2 1','13.5 -6.5;19 -11'],['1,5 0,5;2 1','13,5 -6,5;19 -11']];
  for(const [inverse,result] of variants){await page.locator('#field-inverse').fill(inverse);await page.locator('#field-result').fill(result);await page.locator('#answer-fields button[type=submit]').click();await correct();}
  assert.match(await page.locator('.field-entry .input-help').first().innerText(),/0,5/);
  await page.reload();await page.locator('#field-inverse').waitFor();assert.equal(await page.locator('#field-inverse').inputValue(),'');
  await page.locator('#field-result').fill('13,5 -6,5;19 -11');
  await page.locator('#field-inverse').fill('1,5 0,6;2 1');await page.locator('#answer-fields button[type=submit]').click();assert.match(await page.locator('#feedback').innerText(),/Проверь поля: Обратная матрица/);
  assert.deepEqual(errors,[]);console.log('Decimal browser QA passed: real calculus half, both linear matrix fields, fractions/points/commas, wrong values and reload.');
 }finally{await browser.close();}
}
main().catch(e=>{console.error(e);process.exit(1)});
