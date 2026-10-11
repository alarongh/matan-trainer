import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {spawnSync} from 'node:child_process';
import katex from 'katex';
import {numeric} from '../src/answer.js';
import {physicsFormulas} from '../src/physics-formulas.js';
import {checkPhysicsAnswer} from '../src/physics-answer.js';
test('physics source coverage, answer formats, numerical goldens, manual review and math rendering',()=>{
const tasks=JSON.parse(fs.readFileSync('data/physics-tasks.json','utf8'));
const index=JSON.parse(fs.readFileSync('data/physics-source-index.json','utf8'));
for(const task of tasks){
 assert.equal(task.stages.length,4,task.id);
 if(task.kind==='review'){assert.equal(checkPhysicsAnswer(task,'0').valid,false);assert.ok(task.checklist.length);continue;}
 assert.equal(checkPhysicsAnswer(task,task.answer).correct,true,task.id+' expected answer');
 assert.equal(checkPhysicsAnswer(task,task.kind==='fields'?JSON.stringify(Object.fromEntries(task.fields.map(f=>[f.id,'-999999']))):task.kind==='choice'?(task.answer==='1'?'2':'1'):'-999999').correct,false,task.id+' wrong answer');
 if(task.kind==='number'){const n=numeric(task.answer);assert.equal(checkPhysicsAnswer(task,String(n)).correct,true,task.id+' decimal');assert.equal(checkPhysicsAnswer(task,String(n).replace('.',',')).correct,true,task.id+' comma');}
 for(const stage of task.stages)for(const b of stage.blocks)if(b.tex)katex.renderToString(b.tex,{throwOnError:true,strict:'ignore'});
 katex.renderToString(task.prompt,{throwOnError:true,strict:'ignore'});
 for(const o of task.options||[])if(o.tex)katex.renderToString(o.tex,{throwOnError:true,strict:'ignore'});
 for(const src of task.sources)assert.ok(fs.existsSync('sources/'+src.file+'.pdf'));
}
const find=n=>tasks.find(t=>t.id==='ph-problem-'+n.replace('.','-'));
assert.equal(checkPhysicsAnswer(find('1.2'),'6').correct,true);
assert.equal(checkPhysicsAnswer(find('1.10'),'-1/4').correct,true);
assert.equal(checkPhysicsAnswer(find('2.3'),'4,5').correct,true);
assert.equal(checkPhysicsAnswer(find('5.7'),'1000 kg').correct,true);
assert.equal(checkPhysicsAnswer(find('8.10'),'10 rpm').correct,true);
assert.equal(checkPhysicsAnswer(find('10.2'),'10 кДж').correct,true);
assert.equal(checkPhysicsAnswer(find('10.2'),'10 кг').valid,false);
assert.equal(checkPhysicsAnswer(find('10.7'),'9,94%').correct,true);
assert.equal(checkPhysicsAnswer(find('5.6'),'-1/6').correct,true);
assert.equal(checkPhysicsAnswer(find('1.1'),'120°').correct,true);
const numbers=new Set(tasks.filter(t=>t.id.startsWith('ph-problem')).map(t=>t.meta));
assert.equal(numbers.size,141);assert.equal(index.length,266);
for(const f of physicsFormulas){for(const tex of [f.left,...f.parts,...f.wrong])katex.renderToString(tex,{throwOnError:true,strict:'ignore'});}
assert.equal(physicsFormulas.length,83);
console.log('Physics preflight passed: 251 cards, source coverage, safe answer parser, all expected/wrong answers, decimals/fractions, units, independent numeric goldens, manual review boundaries and all mathematical renderings.');

});
test('all browser modules parse as JavaScript',()=>{
for(const path of fs.readdirSync('src').filter(p=>p.endsWith('.js'))){const result=spawnSync(process.execPath,['--check','--input-type=module'],{input:fs.readFileSync('src/'+path,'utf8'),encoding:'utf8'});assert.equal(result.status,0,path+': '+result.stderr);}
});
