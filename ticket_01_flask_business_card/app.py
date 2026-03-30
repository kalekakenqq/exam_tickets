# установка: pip install flask
# запуск: python app.py
from flask import Flask, render_template_string

app = Flask(__name__)

BASE_STYLE = """
<style>
    body { font-family: Arial, sans-serif; margin: 0; padding: 0; background: #f5f5f5; }
    nav { background: #333; padding: 10px 20px; }
    nav a { color: white; margin-right: 15px; text-decoration: none; font-size: 16px; }
    nav a:hover { text-decoration: underline; }
    .content { padding: 20px; max-width: 800px; margin: 0 auto; }
    h1 { color: #333; }
    ul li { margin-bottom: 8px; }
</style>
"""

INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head><meta charset="UTF-8"><title>Сайт-визитка</title>""" + BASE_STYLE + """</head>
<body>
<nav><a href="/">Главная</a><a href="/about">О себе</a><a href="/portfolio">Портфолио</a></nav>
<div class="content">
<h1>Привет! Я Python-разработчик</h1>
<p>Добро пожаловать на мой сайт-визитку.</p>
<p>Здесь вы можете узнать обо мне и посмотреть мои проекты.</p>
</div>
</body>
</html>"""

ABOUT_TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head><meta charset="UTF-8"><title>О себе</title>""" + BASE_STYLE + """</head>
<body>
<nav><a href="/">Главная</a><a href="/about">О себе</a><a href="/portfolio">Портфолио</a></nav>
<div class="content">
<h1>О себе</h1>
<p>Студент 2 курса, изучаю Python и веб-разработку.</p>
<p>Увлекаюсь созданием веб-приложений и автоматизацией.</p>
</div>
</body>
</html>"""

PORTFOLIO_TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head><meta charset="UTF-8"><title>Портфолио</title>""" + BASE_STYLE + """</head>
<body>
<nav><a href="/">Главная</a><a href="/about">О себе</a><a href="/portfolio">Портфолио</a></nav>
<div class="content">
<h1>Портфолио</h1>
<ul>
{% for project in projects %}
    <li><strong>{{ project.name }}</strong> — {{ project.desc }}</li>
{% endfor %}
</ul>
</div>
</body>
</html>"""

# три проекта для портфолио
projects = [
    {'name': 'Проект 1', 'desc': 'Веб-приложение на Flask'},
    {'name': 'Проект 2', 'desc': 'Телеграм-бот на Python'},
    {'name': 'Проект 3', 'desc': 'REST API для заметок'},
]


@app.route('/')
def index():
    return render_template_string(INDEX_TEMPLATE)


@app.route('/about')
def about():
    return render_template_string(ABOUT_TEMPLATE)


@app.route('/portfolio')
def portfolio():
    return render_template_string(PORTFOLIO_TEMPLATE, projects=projects)


if __name__ == '__main__':
    app.run(debug=True)
