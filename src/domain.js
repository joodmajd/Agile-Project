export const QUIZ_SIZE = 10;

export function publishedForTopic(questions, course, week) {
  return questions.filter(q => q.status === 'published' && q.course === course && String(q.week) === String(week));
}

export function createQuiz(questions, course, week, random = Math.random, size = QUIZ_SIZE) {
  const pool = publishedForTopic(questions, course, week);
  if (pool.length < size) throw new Error(`This topic needs at least ${size} published questions (currently ${pool.length}).`);
  const shuffled = [...pool];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled.slice(0, size);
}

export function scoreQuiz(questions, answers) {
  if (!questions.length) throw new Error('A quiz must contain at least one question.');
  const correct = questions.reduce((sum, q) => sum + (answers[q.id] === q.answer ? 1 : 0), 0);
  return { correct, total: questions.length, percent: Math.round(correct / questions.length * 100) };
}

export function reviewQuestion(question, reviewer, decision, note = '') {
  if (!['draft', 'approved'].includes(question.status)) throw new Error('Only draft or approved questions can be reviewed.');
  if (!['approve', 'publish', 'reject'].includes(decision)) throw new Error('Choose approve, publish, or reject.');
  if (decision === 'approve' && question.status !== 'draft') throw new Error('Only draft questions can be approved.');
  if (decision === 'publish' && question.status !== 'approved') throw new Error('Approve a question before publishing it.');
  if (decision === 'reject' && !note.trim()) throw new Error('Add feedback when rejecting a question.');
  const status = decision === 'approve' ? 'approved' : decision === 'publish' ? 'published' : 'rejected';
  return { ...question, status, reviewer, reviewNote: decision === 'reject' ? note.trim() : question.reviewNote || '' };
}

export function recordAttempt(history, course, week, questions, answers, at = new Date().toISOString()) {
  const result = scoreQuiz(questions, answers);
  return [...history, { id: `attempt-${Date.parse(at)}-${history.length}`, course, week: Number(week), ...result, at,
    details: questions.map(q => ({ questionId: q.id, answer: answers[q.id] ?? null, correctAnswer: q.answer })) }];
}
