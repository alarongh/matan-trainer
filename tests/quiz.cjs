const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const base=process.env.TEST_URL||'http://127.0.0.1:4173/';
async function main(){
 const {formulaBanks}=await import('../src/formula-bank.js');
 fs.mkdirSync('test-results',{recursive:true});
 const browser=await chromium.launch({headless:true,channel:'msedge'});
 const context=await browser.newContext({viewport:{width:1440,height:1000}});
 const old={version:1,theme:'sage',selected:'sequence-01',group:'all',origin:'all',mode:'all',autoAdvance:false,items:{'sequence-01':{attempts:[{answer:'1/2',correct:true,at:1}],status:'solved',step:0,draft:'1/2'}}};
 await context.addInitScript(value=>{if(!localStorage.getItem('matan-trainer:v1'))localStorage.setItem('matan-trainer:v1',JSON.stringify(value));},old);
 const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));page.setDefaultTimeout(15000);
 const state=subject=>page.evaluate(s=>JSON.parse(localStorage.getItem('formula-quiz:'+s+':v1')),subject);
 async function fill(subject,parts){
  const round=(await state(subject)).round;
  for(let i=0;i<parts.length;i++){await page.locator('#quiz-slots [data-slot="'+i+'"]').click();await page.locator('#quiz-pieces [data-piece="'+round.choices.indexOf(parts[i])+'"]').click();}
 }
 async function ready(){await page.locator('#theme-select').waitFor({state:'attached'});await page.locator('#show-quiz').waitFor();}
 async function overflow(width){assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'page overflow at '+width);}
 try{
  await page.goto(base);await ready();const calculus=await page.evaluate(()=>localStorage.getItem('matan-trainer:v1'));
  assert.equal(await page.locator('#count-all').innerText(),'426');
  await page.locator('#show-quiz').click();assert.equal(await page.locator('#task-practice').isVisible(),false);
  assert.equal(await page.locator('.quiz-topic input').count(),10);
  await page.getByRole('button',{name:'Снять выбор',exact:true}).click();assert.equal(await page.locator('#quiz-start').isDisabled(),true);
  await page.getByRole('button',{name:'Все номера',exact:true}).click();await page.locator('#quiz-auto-next').uncheck();await page.locator('#quiz-start').click();
  for(const subject of ['matan','linear']){
   if(subject==='linear'){
    const before=await state('matan');await page.locator('#subject-select').selectOption('linear');await ready();
    assert.ok(await page.locator('#formula-quiz').isVisible());assert.ok(page.url().includes('practice=formulas'));
    assert.equal(await page.locator('#count-all').innerText(),'121');assert.deepEqual(await state('matan'),before);
    await page.locator('#quiz-auto-next').uncheck();await page.locator('#quiz-start').click();
   }
   const source=formulaBanks[subject],firstState=await state(subject),first=source.find(c=>c.id===firstState.round.id);
   assert.equal(await page.locator('#quiz-check').isDisabled(),true);
   // A draft, its shuffled options and its wave position survive a reload.
   await fill(subject,first.parts);await page.reload();await ready();
   assert.deepEqual((await state(subject)).round.selected,first.parts);
   await page.locator('#quiz-undo').click();assert.equal(await page.locator('#quiz-check').isDisabled(),true);
   if(first.parts.length>1)await page.locator('#quiz-clear').click();
   else assert.equal(await page.locator('#quiz-clear').isDisabled(),true);
   assert.ok((await state(subject)).round.selected.every(v=>v===null));
   const amount=process.env.TEST_SMOKE?8:source.length;
   for(let i=0;i<amount;i++){
    const current=await state(subject),card=source.find(c=>c.id===current.round.id),wrong=[...card.parts];wrong[0]=card.wrong[0];
    await fill(subject,wrong);await page.locator('#quiz-check').click();
    assert.match(await page.locator('#quiz-feedback').innerText(),/Проверь/);assert.equal(await page.locator('#quiz-solution .step').count(),1);
    for(let step=2;step<=4;step++){await page.locator('#quiz-next-step').click();assert.equal(await page.locator('#quiz-solution .step').count(),step);}
    assert.equal(await page.locator('.katex-error').count(),0,card.id);
    await fill(subject,card.parts);await page.locator('#quiz-check').click();assert.match(await page.locator('#quiz-feedback').innerText(),/^Верно/);
    const record=(await state(subject)).items[card.id];assert.equal(record.clean,0,card.id+' hints');assert.equal(record.correct,1,card.id);
    if(i===0)await page.locator('#formula-quiz').screenshot({path:'test-results/quiz-'+subject+'-desktop.png'});
    await page.locator('#quiz-next').click();
    if((i+1)%20===0)console.log(subject+': '+(i+1)+' formulas with all four stages checked.');
   }
   if(!process.env.TEST_SMOKE)assert.equal((await state(subject)).wave,2);
   const last=await state(subject),card=source.find(c=>c.id===last.round.id);
   const order=card.orders.at(-1);await fill(subject,order.map(i=>card.parts[i]));await page.locator('#quiz-check').click();
   assert.match(await page.locator('#quiz-feedback').innerText(),/^Верно/);
   for(const name of ['paper','lavender','night','sage']){await page.locator('button[data-theme="'+name+'"]').click();assert.equal(await page.locator('html').getAttribute('data-theme'),name);}
   for(const width of [768,390,320]){await page.setViewportSize({width,height:844});await overflow(width);if(width===390)await page.locator('#quiz-card').screenshot({path:'test-results/quiz-'+subject+'-mobile.png'});}
   await page.setViewportSize({width:1440,height:1000});await page.evaluate(()=>document.body.style.zoom='2');await overflow('200%');await page.evaluate(()=>document.body.style.zoom='1');
   // Automatic advance runs in the quiz, but stops when leaving it.
   await page.locator('#quiz-next').click();await page.locator('#quiz-auto-next').check();
   const autoState=await state(subject),autoCard=source.find(c=>c.id===autoState.round.id);
   await fill(subject,autoCard.parts);await page.locator('#quiz-check').click();
   await page.waitForFunction(({subject,cursor})=>JSON.parse(localStorage.getItem('formula-quiz:'+subject+':v1')).cursor!==cursor,{subject,cursor:autoState.cursor});
   await page.locator('#quiz-auto-next').uncheck();
   assert.equal(await page.evaluate(()=>localStorage.getItem('matan-trainer:v1')),calculus);
  }
  const linearHistory=await page.evaluate(()=>localStorage.getItem('linear-trainer:v1'));
  await page.locator('#subject-select').selectOption('matan');await ready();assert.ok(await page.locator('#formula-quiz').isVisible());assert.ok((await state('matan')).items);
  await page.locator('#show-tasks').click();assert.ok(await page.locator('#task-practice').isVisible());assert.equal(await page.locator('#answer').inputValue(),'');
  assert.equal(await page.evaluate(()=>localStorage.getItem('linear-trainer:v1')),linearHistory);
  assert.deepEqual(errors,[]);
  const phone=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
  const mobile=await phone.newPage();await mobile.goto(base+'?practice=formulas');await mobile.locator('#quiz-start').tap();await mobile.locator('#quiz-auto-next').uncheck();
  const mobileRound=await mobile.evaluate(()=>JSON.parse(localStorage.getItem('formula-quiz:matan:v1')).round);
  const mobileCard=formulaBanks.matan.find(c=>c.id===mobileRound.id);
  for(let i=0;i<mobileCard.parts.length;i++){await mobile.locator('#quiz-slots [data-slot="'+i+'"]').tap();await mobile.locator('#quiz-pieces [data-piece="'+mobileRound.choices.indexOf(mobileCard.parts[i])+'"]').tap();}
  await mobile.locator('#quiz-check').tap();assert.match(await mobile.locator('#quiz-feedback').innerText(),/^Верно/);await phone.close();
  console.log('Quiz browser QA passed: '+(process.env.TEST_SMOKE?'16':'106')+' constructors, progressive hints, repeats, reload, subject isolation, auto-advance, all themes, touch, 320px and 200% zoom.');
 }finally{await browser.close();}
}
main().catch(e=>{console.error(e);process.exit(1)});
