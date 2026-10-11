const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const tasks=JSON.parse(fs.readFileSync('data/tasks.json','utf8'));
const base=process.env.TEST_URL||'http://127.0.0.1:4173/';
async function main(){
 const browser=await chromium.launch({headless:true,channel:'msedge'});
 const errors=[];
 async function scenario({mode='new',autoAdvance=false,selected='sequence-10',items={},search=''},run){
  const context=await browser.newContext({viewport:{width:1440,height:1000}});
  await context.addInitScript(state=>localStorage.setItem('matan-trainer:v1',JSON.stringify(state)),{version:1,theme:'sage',selected,group:'2',origin:'all',mode,autoAdvance,items});
  const page=await context.newPage();page.setDefaultTimeout(10000);page.on('pageerror',e=>errors.push(e.message));
  try{
   await page.goto(base);await page.locator(`[data-task-id="${selected}"]`).waitFor();
   if(search)await page.locator('#search').fill(search);
   await run(page);
  }finally{await context.close();}
 }
 async function selected(page,id){assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('matan-trainer:v1')).selected),id);}
 async function correct(page,id='sequence-10'){
  const task=tasks.find(t=>t.id===id);
  if(task.kind==='choice')await page.locator(`[data-choice="${task.answer}"]`).click();
  else{await page.locator('#answer').fill(task.answer);await page.locator('#check-button').click();}
  assert.match(await page.locator('#feedback').innerText(),/^Верно/);
 }
 try{
  await scenario({},async page=>{
   await page.locator('#answer').fill('123');
   await page.evaluate(()=>document.activeElement.blur());
   await page.keyboard.press('ArrowRight');await selected(page,'sequence-11');
   await page.keyboard.press('ArrowLeft');await selected(page,'sequence-10');
   assert.equal(await page.locator('#answer').inputValue(),'123');
   await page.locator('#answer').focus();await page.keyboard.press('End');
   await page.keyboard.press('ArrowLeft');await selected(page,'sequence-10');
   assert.equal(await page.locator('#answer').evaluate(input=>input.selectionStart),2);
   await page.locator('#search').focus();await page.keyboard.press('ArrowRight');await selected(page,'sequence-10');
   await page.locator('#origin-filter').focus();await page.keyboard.press('ArrowLeft');await selected(page,'sequence-10');
   await page.evaluate(()=>document.activeElement.blur());
   await page.keyboard.press('Shift+ArrowRight');await selected(page,'sequence-10');
   await page.locator('#open-settings').click();await page.keyboard.press('ArrowRight');await selected(page,'sequence-10');
   await page.keyboard.press('Escape');
   await page.locator('#show-quiz').click();await page.keyboard.press('ArrowRight');await selected(page,'sequence-10');
   await page.locator('#show-tasks').click();await page.keyboard.press('ArrowRight');await selected(page,'sequence-11');
  });
  await scenario({selected:'sequence-01'},async page=>{await page.keyboard.press('ArrowLeft');await selected(page,'sequence-01');});
  await scenario({autoAdvance:true},async page=>{
   await correct(page);await page.keyboard.press('ArrowLeft');
   await selected(page,'sequence-09');await page.waitForTimeout(1300);await selected(page,'sequence-09');
  });
  await scenario({},async page=>{
   await page.goto(new URL('?subject=linear',base).href);await page.locator('[data-task-id]').first().waitFor();
   const ids=await page.locator('[data-task-id]').evaluateAll(buttons=>buttons.map(button=>button.dataset.taskId));
   await page.locator(`[data-task-id="${ids[1]}"]`).click();
   await page.keyboard.press('ArrowRight');
   assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('linear-trainer:v1')).selected),ids[2]);
   await page.keyboard.press('ArrowLeft');
   assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('linear-trainer:v1')).selected),ids[1]);
  });
  await scenario({},async page=>{
   await page.locator('[data-group="all"]').click();
   await page.locator('[data-task-id="textbook-20-4-full"]').click();
   await page.locator('#written-notes').fill('Черновик');await page.keyboard.press('ArrowLeft');
   await selected(page,'textbook-20-4-full');
  });
  await scenario({},async page=>{await correct(page);await page.locator('#next').click();await selected(page,'sequence-11');});
  await scenario({autoAdvance:true},async page=>{await correct(page);await page.waitForFunction(()=>JSON.parse(localStorage.getItem('matan-trainer:v1')).selected==='sequence-11');});
  await scenario({autoAdvance:true},async page=>{
   await page.locator('#answer').fill('-999');await page.locator('#check-button').click();
   assert.match(await page.locator('#feedback').innerText(),/неверно/);
   await correct(page);await page.waitForFunction(()=>JSON.parse(localStorage.getItem('matan-trainer:v1')).selected==='sequence-11');
  });
  await scenario({autoAdvance:true},async page=>{
   await page.locator('#reveal').click();await correct(page);
   await page.waitForFunction(()=>JSON.parse(localStorage.getItem('matan-trainer:v1')).selected==='sequence-11');
  });
  await scenario({},async page=>{await correct(page);await page.locator('#previous').click();await selected(page,'sequence-09');});
  const solved={status:'solved',step:0,draft:'0',attempts:[{answer:'0',correct:true,at:1}]};
  await scenario({items:{'sequence-11':solved}},async page=>{
   await page.keyboard.press('ArrowRight');await selected(page,'sequence-12');
   await page.keyboard.press('ArrowLeft');await selected(page,'sequence-10');
  });
  await scenario({items:{'sequence-11':solved}},async page=>{await correct(page);await page.locator('#next').click();await selected(page,'sequence-12');});
  await scenario({mode:'all',autoAdvance:true},async page=>{await correct(page);await page.waitForFunction(()=>JSON.parse(localStorage.getItem('matan-trainer:v1')).selected==='sequence-11');});
  await scenario({search:'sequence-10'},async page=>{
   await correct(page);await page.locator('#next').click();await selected(page,'sequence-10');
   assert.match(await page.locator('#toast').innerText(),/Дальше/);
  });
  const last=tasks.filter(t=>t.group===2).at(-1).id;
  await scenario({mode:'all',selected:last},async page=>{await page.keyboard.press('ArrowRight');await selected(page,last);});
  await scenario({mode:'all',autoAdvance:true,selected:last},async page=>{
   await correct(page,last);await page.locator('#toast').filter({hasText:'Дальше'}).waitFor();
   await selected(page,last);
  });
  await scenario({mode:'review',items:{'sequence-10':{...solved,status:'learning',step:0},'sequence-11':{...solved,status:'learning',step:0}}},async page=>{
   await correct(page);await page.locator('#next').click();await selected(page,'sequence-11');
  });
  await scenario({autoAdvance:true},async page=>{
   await correct(page);await page.locator('[data-task-id="sequence-20"]').click();
   await page.waitForTimeout(1300);await selected(page,'sequence-20');
  });
  assert.deepEqual(errors,[]);
  console.log('Navigation passed: arrow keys in both subjects, drafts, input cursors, search/select/textarea, dialogs, quiz, filtered neighbours, boundaries and cancelled auto-advance; existing button and automatic navigation.');
 }finally{await browser.close();}
}
main().catch(e=>{console.error(e);process.exit(1)});
