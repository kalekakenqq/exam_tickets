# установка: pip install flask
# запуск: python app.py
from flask import Flask, render_template_string, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'secret123'

_STYLE = """<style>
    body { font-family: Arial, sans-serif; padding: 20px; max-width: 700px; margin: 0 auto; }
    .btn { padding: 8px 16px; background: #0066cc; color: white; border: none; cursor: pointer;
           border-radius: 4px; text-decoration: none; font-size: 14px; }
    .btn-back { background: #666; }
    .correct { color: green; font-weight: bold; }
    .wrong { color: red; }
    .progress { color: #666; font-size: 0.9em; }
</style>"""

QUESTION_TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head><meta charset="UTF-8"><title>Опросник</title>""" + _STYLE + """</head>
<body>
<p class="progress">Вопрос {{ num + 1 }} из {{ total }}</p>
<h2>{{ q.question }}</h2>
<form method="post">
    {% for option in q.options %}
    <label style="display:block;margin-bottom:10px;">
        <input type="radio" name="answer" value="{{ option }}"
            {% if saved == option %}checked{% endif %} required>
        {{ option }}
    </label>
    {% endfor %}
    <br>
    {% if num > 0 %}
    <a href="{{ url_for('question', num=num-1) }}" class="btn btn-back">назад</a>
    {% endif %}
    <button type="submit" class="btn">вперёд</button>
</form>
</body>
</html>"""

RESULTS_TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head><meta charset="UTF-8"><title>Результаты</title>""" + _STYLE + """</head>
<body>
<h1>Результаты</h1>
<h2>Правильных ответов: {{ score }} из {{ total }}</h2>
<ul>
{% for r in results %}
    <li style="margin-bottom:10px;">
        <strong>{{ r.question }}</strong><br>
        {% if r.is_correct %}
            <span class="correct">правильно: {{ r.user }}</span>
        {% else %}
            <span class="wrong">ваш ответ: {{ r.user }}</span>
            (правильно: <strong>{{ r.correct }}</strong>)
        {% endif %}
    </li>
{% endfor %}
</ul>
<a href="{{ url_for('start') }}" class="btn">пройти заново</a>
</body>
</html>"""

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
    return render_template_string(QUESTION_TEMPLATE,
                                  q=q, num=num,
                                  total=len(questions), saved=saved)


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
    return render_template_string(RESULTS_TEMPLATE,
                                  score=score,
                                  total=len(questions),
                                  results=results_list)


if __name__ == '__main__':
    app.run(debug=True)
