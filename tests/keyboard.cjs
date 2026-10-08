const {chromium}=require(process.env.PLAYWRIGHT_PATH||'playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const base=process.env.TEST_URL||'http://127.0.0.1:4173/';
async function main(){
 fs.mkdirSync('test-results',{recursive:true});
 const browser=await chromium.launch({headless:true,channel:process.env.BROWSER_CHANNEL||'msedge'});
 const context=await browser.newContext({viewport:{width:1440,height:1000}});
 const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base);await page.locator('[data-task-id]').first().waitFor();
 assert.equal(await page.locator('#math-keyboard').isVisible(),false,'Parity uses ticket choices');
 await page.locator('#open-settings').click();await page.locator('#auto-advance').uncheck();await page.locator('#settings-dialog .close-dialog').click();
 await page.locator('[data-group="3"]').click();await page.locator('[data-task-id="demo-power-3"]').click();
 assert.match(await page.locator('#problem .katex-html').innerText(),/arctan/);assert.match(await page.locator('#problem .katex-html').innerText(),/arccot/);
 // Real pointer clicks preserve the selected input and position in templates.
 const click=async id=>page.locator(`#math-keyboard [data-key="${id}"]`).first().click();
 await click('clear');await click('exponential');assert.equal(await page.locator('#answer').inputValue(),'e^()');
 for(const id of ['-','3','*','π','/','4',')'])await click(id);
 assert.equal(await page.locator('#answer').inputValue(),'e^(-3*π/4)');
 await page.locator('#keyboard-check').click();assert.match(await page.locator('#feedback').innerText(),/^Верно/);
 await page.screenshot({path:'test-results/keyboard-desktop.png',fullPage:true});
 await page.reload();await page.locator('[data-task-id]').first().waitFor();assert.equal(await page.locator('#answer').inputValue(),'e^(-3*π/4)');
 await page.locator('#answer').fill('1234');await page.locator('#answer').evaluate(e=>e.setSelectionRange(1,3));await click('9');assert.equal(await page.locator('#answer').inputValue(),'194');
 await click('delete');assert.equal(await page.locator('#answer').inputValue(),'14');await click('left');await click('7');await click('right');await click('0');assert.equal(await page.locator('#answer').inputValue(),'7104');
 await page.locator('#answer').fill('1+3');await page.locator('#answer').selectText();await click('root');assert.equal(await page.locator('#answer').inputValue(),'sqrt(1+3)');
 await click('clear');await click('delete');assert.equal(await page.locator('#answer').inputValue(),'');
 for(const id of ['3','power','2',')'])await click(id);assert.equal(await page.locator('#answer').inputValue(),'3^(2)');
 await page.locator('#answer').fill('7'.repeat(256));await click('7');assert.equal((await page.locator('#answer').inputValue()).length,256);
 await page.locator('#toggle-keyboard').click();assert.equal(await page.locator('#math-keys').isVisible(),false);assert.equal(await page.locator('#toggle-keyboard').getAttribute('aria-expanded'),'false');
 await page.locator('#toggle-keyboard').click();assert.equal(await page.locator('#math-keys').isVisible(),true);
 await page.locator('.keyboard-more summary').click();await click('clear');await click('arctan');await click('1');await click(')');assert.equal(await page.locator('#answer').inputValue(),'arctan(1)');
 await page.locator('[data-group="2"]').click();await page.locator('[data-task-id="sequence-01"]').click();
 await click('1');await click('/');await click('2');await page.locator('#keyboard-check').click();assert.match(await page.locator('#feedback').innerText(),/^Верно/);
 await page.locator('[data-task-id="sequence-16"]').click();await click('root');await click('2');await click(')');await page.locator('#keyboard-check').click();assert.match(await page.locator('#feedback').innerText(),/^Верно/);
 for(const width of [1440,768,390,320]){
  await page.setViewportSize({width,height:900});
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Keyboard page overflow at '+width);
  assert.ok(await page.locator('#math-keys').evaluate(e=>e.scrollWidth<=e.clientWidth+1),'Keyboard panel overflow at '+width);
  if(width===390){await page.locator('#answer').scrollIntoViewIfNeeded();await page.screenshot({path:'test-results/keyboard-mobile.png',fullPage:true});}
 }
 const mobile=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,deviceScaleFactor:1});
 const touch=await mobile.newPage();await touch.goto(base);await touch.locator('[data-task-id]').first().waitFor();await touch.locator('[data-group="3"]').tap();
 const tap=async id=>touch.locator(`#math-keyboard [data-key="${id}"]`).first().tap();
 await tap('exponential');await tap('-');await tap('3');await tap(')');assert.equal(await touch.locator('#answer').inputValue(),'e^(-3)');
 assert.notEqual(await touch.evaluate(()=>document.activeElement.id),'answer','Touch keys should not summon native keyboard');
 await touch.locator('#answer').scrollIntoViewIfNeeded();await touch.screenshot({path:'test-results/keyboard-touch.png',fullPage:true});
 await tap('clear');for(const id of ['exponential','-','3','/','2',')'])await tap(id);
 await touch.locator('#keyboard-check').tap();await touch.waitForTimeout(1400);
 assert.equal(await touch.locator('[aria-current="true"]').getAttribute('data-task-id'),'demo-power-2');
 assert.notEqual(await touch.evaluate(()=>document.activeElement.id),'answer','Auto advance must not summon native keyboard on touch');
 await page.setViewportSize({width:1440,height:1000});await page.evaluate(()=>document.body.style.zoom='2');
 assert.ok(await page.locator('#math-keys').evaluate(e=>e.scrollWidth<=e.clientWidth+1),'Keyboard zoom overflow');
 assert.deepEqual(errors,[]);await browser.close();console.log('Keyboard passed: arctan/arccot display; pointer and touch typing; exponent/root/fraction answers; cursor; selected text; deletion; maxlength; collapse; persistent draft; mobile layout and 200% zoom.');
}
main().catch(e=>{console.error(e);process.exit(1);});
