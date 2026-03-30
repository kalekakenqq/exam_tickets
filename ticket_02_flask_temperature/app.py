# установка: pip install flask
# запуск: python app.py
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = 'secret123'


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
    return render_template('index.html',
                           result=result,
                           error=error,
                           history=session.get('history', []))


if __name__ == '__main__':
    app.run(debug=True)
