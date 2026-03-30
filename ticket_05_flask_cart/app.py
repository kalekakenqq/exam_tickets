# установка: pip install flask
# запуск: python app.py
from flask import Flask, render_template_string, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'secret123'

STYLE = """
<style>
    body { font-family: Arial, sans-serif; margin: 0; padding: 0; }
    nav { background: #333; padding: 10px 20px; }
    nav a { color: white; margin-right: 15px; text-decoration: none; }
    .content { padding: 20px; max-width: 800px; margin: 0 auto; }
    .item { border: 1px solid #ddd; padding: 15px; margin-bottom: 10px; border-radius: 4px; display: flex; justify-content: space-between; align-items: center; }
    a.btn { padding: 8px 14px; background: #0066cc; color: white; text-decoration: none; border-radius: 4px; }
    a.del { padding: 8px 14px; background: #cc0000; color: white; text-decoration: none; border-radius: 4px; }
    .total { font-size: 1.3em; font-weight: bold; }
</style>
"""

INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head><meta charset="UTF-8"><title>Магазин</title>{{ style }}</head>
<body>
<nav>
    <a href="/">Каталог</a>
    <a href="/cart">Корзина ({{ cart_count }})</a>
</nav>
<div class="content">
<h1>Каталог книг</h1>
{% for item in catalog %}
<div class="item">
    <span><strong>{{ item.name }}</strong> — {{ item.price }} руб.</span>
    <a href="/add/{{ item.id }}" class="btn">в корзину</a>
</div>
{% endfor %}
</div>
</body>
</html>"""

CART_TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head><meta charset="UTF-8"><title>Корзина</title>{{ style }}</head>
<body>
<nav>
    <a href="/">Каталог</a>
    <a href="/cart">Корзина ({{ items|length }})</a>
</nav>
<div class="content">
<h1>Корзина</h1>
{% if items %}
{% for item in items %}
<div class="item">
    <span>{{ item.name }} — {{ item.price }} руб.</span>
    <a href="/remove/{{ item.id }}" class="del">удалить</a>
</div>
{% endfor %}
<p class="total">Итого: {{ total }} руб.</p>
<a href="/clear" class="del">очистить корзину</a>
{% else %}
<p>Корзина пуста. <a href="/">Перейти в каталог</a></p>
{% endif %}
</div>
</body>
</html>"""

# каталог из 5 книг
catalog = [
    {'id': 1, 'name': 'Python для начинающих', 'price': 500},
    {'id': 2, 'name': 'Flask в деталях', 'price': 700},
    {'id': 3, 'name': 'Django с нуля', 'price': 800},
    {'id': 4, 'name': 'Алгоритмы на Python', 'price': 600},
    {'id': 5, 'name': 'SQL для разработчиков', 'price': 450},
]


@app.route('/')
def index():
    cart_ids = session.get('cart', [])
    return render_template_string(INDEX_TEMPLATE,
                                  style=STYLE, catalog=catalog,
                                  cart_count=len(cart_ids))


@app.route('/add/<int:item_id>')
def add_to_cart(item_id):
    cart = session.get('cart', [])
    # добавляем только если ещё нет
    if item_id not in cart:
        cart.append(item_id)
    session['cart'] = cart
    return redirect(url_for('index'))


@app.route('/cart')
def cart():
    cart_ids = session.get('cart', [])
    items = [p for p in catalog if p['id'] in cart_ids]
    total = sum(p['price'] for p in items)
    return render_template_string(CART_TEMPLATE,
                                  style=STYLE, items=items, total=total)


@app.route('/remove/<int:item_id>')
def remove_from_cart(item_id):
    cart = session.get('cart', [])
    cart = [i for i in cart if i != item_id]
    session['cart'] = cart
    return redirect(url_for('cart'))


@app.route('/clear')
def clear_cart():
    session['cart'] = []
    return redirect(url_for('cart'))


if __name__ == '__main__':
    app.run(debug=True)
