const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const base=process.env.TEST_URL||'http://127.0.0.1:4173/';
async function main(){
 const {formulaBanks}=await import('../src/formula-bank.js');const cards=formulaBanks.matan;
 const browser=await chromium.launch({headless:true,channel:'msedge'}),context=await browser.newContext({viewport:{width:1440,height:1000}}),page=await context.newPage();
 const errors=[];page.on('pageerror',e=>errors.push(e.message));page.setDefaultTimeout(12000);fs.mkdirSync('test-results',{recursive:true});
 const state=()=>page.evaluate(()=>JSON.parse(localStorage.getItem('formula-quiz:matan:v1')));
 async function fill(parts){const round=(await state()).round;for(let i=0;i<parts.length;i++){await page.locator(`[data-slot="${i}"]`).click();await page.locator(`[data-piece="${round.choices.indexOf(parts[i])}"]`).click();}}
 try{
  await page.goto(new URL('?practice=formulas',base).href);await page.locator('#quiz-practice-kind').waitFor();await page.locator('#quiz-auto-next').uncheck();
  for(const kind of ['reverse','transform','forward']){
   await page.locator('.quiz-topics').evaluate(e=>e.open=true);await page.locator('#quiz-practice-kind').selectOption(kind);await page.locator('#quiz-start').click();
   const initial=await state(),expected=cards.filter(c=>c.type===kind).length;assert.equal(initial.queue.length,expected);assert.equal(initial.practice,kind);
   const amount=kind==='forward'?8:expected;
   for(let i=0;i<amount;i++){
    const round=(await state()).round,card=cards.find(c=>c.id===round.id);assert.equal(card.type,kind);
    assert.match(await page.locator('#quiz-instruction').innerText(),kind==='reverse'?/исходную левую/:kind==='transform'?/следующий переход/:/правую часть/);
    const wrong=[...card.parts];wrong[0]=card.wrong[0];await fill(wrong);await page.locator('#quiz-check').click();assert.equal(await page.locator('#quiz-solution .step').count(),1);
    for(let step=2;step<=4;step++){await page.locator('#quiz-next-step').click();assert.equal(await page.locator('#quiz-solution .step').count(),step);}
    assert.equal(await page.locator('.katex-error').count(),0,card.id);await fill(card.parts);await page.locator('#quiz-check').click();assert.match(await page.locator('#quiz-feedback').innerText(),/^Верно/);
    if(i===0){await page.locator('#quiz-card').screenshot({path:`test-results/quiz-${kind}-desktop.png`});const saved=await state();await page.reload();await page.locator('#quiz-card').waitFor();assert.deepEqual(await state(),saved);assert.equal(await page.locator('#quiz-practice-kind').inputValue(),kind);}
    await page.locator('#quiz-next').click();
   }
   if(kind!=='forward')assert.equal((await state()).wave,2);
   console.log(kind+': '+amount+' constructors and all hint stages verified.');
  }
  await page.setViewportSize({width:390,height:844});await page.locator('.quiz-topics').evaluate(e=>e.open=true);await page.locator('#quiz-practice-kind').selectOption('reverse');await page.locator('#quiz-start').click();
  const round=(await state()).round,card=cards.find(c=>c.id===round.id);assert.ok(round.selected.every(v=>v===null));await page.locator('#quiz-card').screenshot({path:'test-results/quiz-reverse-mobile-unsolved.png'});await fill(card.parts);await page.locator('#quiz-check').click();assert.match(await page.locator('#quiz-feedback').innerText(),/^Верно/);await page.locator('#quiz-card').screenshot({path:'test-results/quiz-reverse-mobile.png'});
  for(const width of [320,390,768]){await page.setViewportSize({width,height:844});assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'overflow '+width);}
  await page.setViewportSize({width:1440,height:1000});await page.evaluate(()=>document.body.style.zoom='2');assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'zoom overflow');await page.evaluate(()=>document.body.style.zoom='1');
  await page.locator('#subject-select').selectOption('linear');await page.locator('#quiz-start').waitFor();assert.equal(await page.locator('#quiz-practice-kind').count(),0);
  await page.locator('#subject-select').selectOption('physics');await page.locator('#quiz-start').waitFor();assert.equal(await page.locator('#quiz-practice-kind').count(),0);
  assert.deepEqual(errors,[]);console.log('Matan formula variants passed: reverse, transformation and forward modes, shuffled distractors, progressive steps, reload/history, infinite waves, mobile and unchanged other subjects.');
 }finally{await browser.close();}
}
main().catch(error=>{console.error(error);process.exit(1);});
