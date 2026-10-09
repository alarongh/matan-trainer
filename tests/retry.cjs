const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const base=process.env.TEST_URL||'http://127.0.0.1:4173/';
async function main(){
 const browser=await chromium.launch({headless:true,channel:'msedge'});
 try{
  for(const subject of ['matan','linear']){
   const tasks=JSON.parse(fs.readFileSync('data/'+(subject==='linear'?'linear-tasks':'tasks')+'.json','utf8'));
   const key=subject==='linear'?'linear-trainer:v1':'matan-trainer:v1';
   const scalar=subject==='matan'?tasks.find(t=>t.id==='sequence-01'):tasks.find(t=>!['fields','multi','choice'].includes(t.kind));
   const examples=[scalar,tasks.find(t=>t.kind==='fields'),tasks.find(t=>t.kind==='multi')];
   const old={version:1,theme:'sage',selected:scalar.id,group:'all',origin:'all',mode:'all',autoAdvance:false,items:{[scalar.id]:{status:'assisted',step:scalar.stages.length,draft:scalar.answer,attempts:[{answer:scalar.answer,correct:true,at:1}]}}};
   const context=await browser.newContext({viewport:{width:390,height:844}});
   await context.addInitScript(({key,old})=>{if(!localStorage.getItem(key))localStorage.setItem(key,JSON.stringify(old));},{key,old});
   const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
   const read=()=>page.evaluate(k=>JSON.parse(localStorage.getItem(k)),key);
   async function ready(){await page.locator('#theme-select').waitFor({state:'attached'});await page.locator('[data-task-id]').first().waitFor();}
   async function select(id){await page.locator('[data-task-id="'+id+'"]').click();}
   async function enter(task){
    if(task.kind==='fields')for(const field of task.fields)await page.locator('#field-'+field.id).fill(field.answer);
    else if(task.kind==='multi')for(const value of task.answer.split(';'))await page.locator('#choices input[value="'+value+'"]').check();
    else await page.locator('#answer').fill(task.answer);
   }
   async function submit(task){await page.locator(task.kind==='fields'?'#answer-fields button[type=submit]':task.kind==='multi'?'#choices button[type=submit]':'#check-button').click();assert.match(await page.locator('#feedback').innerText(),/^Верно/);}
   async function blank(task){
    if(task.kind==='fields')for(const field of task.fields)assert.equal(await page.locator('#field-'+field.id).inputValue(),'');
    else if(task.kind==='multi')assert.equal(await page.locator('#choices input:checked').count(),0);
    else assert.equal(await page.locator('#answer').inputValue(),'');
    assert.equal(await page.locator('#solution').isVisible(),false);
   }
   try{
    await page.goto(base+(subject==='linear'?'?subject=linear':''));await ready();
    await blank(scalar);assert.equal((await read()).items[scalar.id].status,'assisted');assert.deepEqual((await read()).items[scalar.id].attempts,old.items[scalar.id].attempts);
    for(const task of examples){
     await select(task.id);await page.locator('#reveal').click();await enter(task);await submit(task);
     const completed=(await read()).items[task.id];assert.equal(completed.draft,'');assert.equal(completed.status,'assisted');
     const other=tasks.find(t=>t.id!==task.id);await select(other.id);await select(task.id);await blank(task);
     assert.deepEqual((await read()).items[task.id].attempts,completed.attempts);assert.equal((await read()).items[task.id].status,'assisted');
     await page.reload();await ready();await blank(task);
     // An unfinished new attempt still keeps its draft and partial hints.
     await enter(task);await page.locator('#reveal').click();const unfinished=(await read()).items[task.id];
     await page.reload();await ready();assert.deepEqual((await read()).items[task.id],unfinished);assert.equal(await page.locator('#steps .step').count(),1);
     await page.locator('#restart-attempt').click();await blank(task);
     const restarted=(await read()).items[task.id];assert.equal(restarted.draft,'');assert.equal(restarted.step,0);assert.deepEqual(restarted.attempts,completed.attempts);
     await page.reload();await ready();await blank(task);
    }
    if(subject==='matan'){
     await select(scalar.id);await page.locator('#answer').fill('0');await page.locator('#check-button').click();assert.equal(await page.locator('#steps .step').count(),1);
     await page.locator('#mobile-settings').click();await page.locator('#auto-advance').check();await page.locator('#settings-dialog .close-dialog').click();
     await enter(scalar);await submit(scalar);await page.waitForFunction(k=>JSON.parse(localStorage.getItem(k)).selected==='sequence-02',key);
     await page.locator('#previous').click();await blank(scalar);assert.equal((await read()).items[scalar.id].attempts.at(-1).correct,true);
     // The old final-stage retry action has the same clearing behavior.
     await page.locator('#reveal').click();for(let i=1;i<scalar.stages.length;i++)await page.locator('#next-step').click();
     await page.locator('#answer').fill('1/2');await page.locator('#next-step').click();await blank(scalar);
    }
    assert.deepEqual(errors,[]);
    console.log(subject+': legacy completed answers, all input types, return/reload, close/retry, preserved history and unfinished drafts passed.');
   }finally{await context.close();}
  }
 }finally{await browser.close();}
}
main().catch(e=>{console.error(e);process.exit(1)});
