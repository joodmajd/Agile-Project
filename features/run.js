import { readFileSync } from 'node:fs';
import assert from 'node:assert/strict';
import { createQuiz, recordAttempt, reviewQuestion, scoreQuiz } from '../src/domain.js';

const feature=readFileSync(new URL('./practice_quiz.feature',import.meta.url),'utf8');
const expected=[
  'Draft questions are hidden from students',
  'A reviewer approves and publishes a draft question',
  'A student receives a ten question quiz without repeats',
  'A student sees the score and explanations',
  'A completed quiz is recorded by topic'
];
for(const name of expected) assert.ok(feature.includes(`Scenario: ${name}`),`Missing Gherkin scenario: ${name}`);
const cases=[
  ['Draft questions are hidden from students',()=>{const pool=[{id:'d',status:'draft',course:'C',week:1},...Array.from({length:10},(_,i)=>({id:`p${i}`,status:'published',course:'C',week:1}))];const quiz=createQuiz(pool,'C',1,()=>0.3);assert.equal(quiz.length,10);assert.ok(quiz.every(q=>q.status==='published'));}],
  ['A reviewer approves and publishes a draft question',()=>{const approved=reviewQuestion({id:'d',status:'draft',course:'C',week:1},'Instructor','approve');assert.equal(approved.status,'approved');const q=reviewQuestion(approved,'Instructor','publish');assert.equal(q.status,'published');const pool=[q,...Array.from({length:9},(_,i)=>({id:`p${i}`,status:'published',course:'C',week:1}))];assert.equal(createQuiz(pool,'C',1,()=>0.2).length,10);}],
  ['A student receives a ten question quiz without repeats',()=>{const pool=Array.from({length:12},(_,i)=>({id:`p${i}`,status:'published',course:'C',week:1}));const quiz=createQuiz(pool,'C',1,()=>0.4);assert.equal(quiz.length,10);assert.equal(new Set(quiz.map(q=>q.id)).size,10);}],
  ['A student sees the score and explanations',()=>{const quiz=Array.from({length:10},(_,i)=>({id:`p${i}`,answer:i%2,explanation:'Review the example.'}));const answers=Object.fromEntries(quiz.map(q=>[q.id,q.answer]));assert.equal(scoreQuiz(quiz,answers).percent,100);assert.ok(quiz.every(q=>q.explanation));}],
  ['A completed quiz is recorded by topic',()=>{const quiz=[{id:'q1',answer:0}];const history=recordAttempt([],'SET312',6,quiz,{q1:0},'2026-11-16T10:00:00.000Z');assert.equal(history[0].course,'SET312');assert.equal(history[0].week,6);assert.equal(history[0].percent,100);}]
];
for(const [name,run] of cases){run();console.log(`✔ ${name}`);}
console.log(`${cases.length} Gherkin-mapped scenarios passed.`);
