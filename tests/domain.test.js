import test from 'node:test';
import assert from 'node:assert/strict';
import { createQuiz, scoreQuiz, reviewQuestion, recordAttempt } from '../src/domain.js';
const qs=Array.from({length:12},(_,i)=>({id:`q${i}`,course:'SET312',week:6,status:i===11?'draft':'published',answer:i%4}));

test('only published questions are eligible and quiz has ten unique questions',()=>{const quiz=createQuiz(qs,'SET312',6,()=>0.42);assert.equal(quiz.length,10);assert.equal(new Set(quiz.map(q=>q.id)).size,10);assert.ok(quiz.every(q=>q.status==='published'));});
test('insufficient published pool gives a useful error',()=>assert.throws(()=>createQuiz(qs.slice(0,9),'SET312',6),/at least 10/));
test('scoring uses correct divided by total rounded to nearest whole percent',()=>{const questions=[{id:'a',answer:0},{id:'b',answer:1},{id:'c',answer:2}];assert.deepEqual(scoreQuiz(questions,{a:0,b:1,c:0}),{correct:2,total:3,percent:67});});
test('review uses draft, approved, published, and rejected states with feedback',()=>{const q={id:'d',status:'draft'};const approved=reviewQuestion(q,'Reviewer','approve');assert.equal(approved.status,'approved');assert.throws(()=>reviewQuestion(q,'Reviewer','publish'),/Approve a question/);assert.equal(reviewQuestion(approved,'Reviewer','publish').status,'published');assert.equal(reviewQuestion(q,'Reviewer','reject','Please clarify the explanation.').reviewNote,'Please clarify the explanation.');assert.throws(()=>reviewQuestion(q,'Reviewer','reject'),/Add feedback/);assert.throws(()=>reviewQuestion({...q,status:'published'},'Reviewer','reject','No'),/Only draft or approved/);});
test('attempt history keeps topic, score, timestamp, and answer detail',()=>{const quiz=[{id:'a',answer:0},{id:'b',answer:1}];const history=recordAttempt([],'SET312',6,quiz,{a:0,b:0},'2026-11-16T10:00:00.000Z');assert.equal(history[0].percent,50);assert.equal(history[0].week,6);assert.equal(history[0].details[1].correctAnswer,1);});
