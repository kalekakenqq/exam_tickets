# установка: pip install flask
# запуск: python app.py
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'secret123'

# вопросы с вариантами ответов
questions = [
    {
        'question': 'Столица России?',
        'options': ['Москва', 'Санкт-Петербург', 'Казань', 'Новосибирск'],
        'answer': 'Москва',
    },
    {
        'question': 'Сколько будет 7 умножить на 8?',
        'options': ['54', '56', '64', '48'],
        'answer': '56',
    },
    {
        'question': 'Кто написал "Войну и мир"?',
        'options': ['Пушкин', 'Достоевский', 'Толстой', 'Чехов'],
        'answer': 'Толстой',
    },
    {
        'question': 'В каком году Гагарин полетел в космос?',
        'options': ['1957', '1959', '1961', '1963'],
        'answer': '1961',
    },
]


@app.route('/')
def start():
    # сбрасываем ответы при старте
    session['answers'] = {}
    return redirect(url_for('question', num=0))


@app.route('/question/<int:num>', methods=['GET', 'POST'])
def question(num):
    if num >= len(questions):
        return redirect(url_for('results'))
    if request.method == 'POST':
        answers = session.get('answers', {})
        answers[str(num)] = request.form.get('answer', '')
        session['answers'] = answers
        if num + 1 < len(questions):
            return redirect(url_for('question', num=num + 1))
        return redirect(url_for('results'))
    q = questions[num]
    saved = session.get('answers', {}).get(str(num), '')
    return render_template('question.html', q=q, num=num, total=len(questions), saved=saved)


@app.route('/results')
def results():
    answers = session.get('answers', {})
    score = 0
    results_list = []
    for i, q in enumerate(questions):
        user_answer = answers.get(str(i), '')
        correct = user_answer == q['answer']
        if correct:
            score += 1
        results_list.append({
            'question': q['question'],
            'user': user_answer or 'не ответил',
            'correct': q['answer'],
            'is_correct': correct,
        })
    return render_template('results.html', score=score, total=len(questions), results=results_list)


if __name__ == '__main__':
    app.run(debug=True)
