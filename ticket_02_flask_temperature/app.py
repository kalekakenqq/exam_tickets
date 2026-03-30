# установка: pip install flask
# запуск: python app.py
from flask import Flask, render_template_string, request, session

app = Flask(__name__)
app.secret_key = 'secret123'

TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Конвертер температур</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; max-width: 600px; margin: 0 auto; }
        .error { color: red; font-weight: bold; }
        .result { color: green; font-size: 1.2em; font-weight: bold; }
        input, select { padding: 8px; margin-right: 5px; }
        button { padding: 8px 16px; background: #0066cc; color: white; border: none; cursor: pointer; border-radius: 4px; }
        ul { background: #f5f5f5; padding: 15px 30px; border-radius: 4px; }
    </style>
</head>
<body>
<h1>Конвертер температур</h1>
<form method="post">
    <input type="text" name="temp" placeholder="Введите температуру" required>
    <select name="scale">
        <option value="C">Цельсий в Фаренгейт</option>
        <option value="F">Фаренгейт в Цельсий</option>
    </select>
    <button type="submit">Конвертировать</button>
</form>
{% if error %}
    <p class="error">{{ error }}</p>
{% endif %}
{% if result %}
    <p class="result">{{ result }}</p>
{% endif %}
{% if history %}
    <h3>Последние конвертации:</h3>
    <ul>
    {% for item in history %}
        <li>{{ item }}</li>
    {% endfor %}
    </ul>
{% endif %}
</body>
</html>"""


def celsius_to_fahrenheit(c):
    return round(c * 9 / 5 + 32, 2)


def fahrenheit_to_celsius(f):
    return round((f - 32) * 5 / 9, 2)


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    if request.method == 'POST':
        try:
            temp = float(request.form['temp'])
            scale = request.form['scale']
            if scale == 'C':
                converted = celsius_to_fahrenheit(temp)
                result = f'{temp} C = {converted} F'
            else:
                converted = fahrenheit_to_celsius(temp)
                result = f'{temp} F = {converted} C'
            # сохраняем последние 5 конвертаций в сессии
            history = session.get('history', [])
            history.insert(0, result)
            session['history'] = history[:5]
        except ValueError:
            error = 'введите корректное число'
    return render_template_string(TEMPLATE,
                                  result=result,
                                  error=error,
                                  history=session.get('history', []))


if __name__ == '__main__':
    app.run(debug=True)
