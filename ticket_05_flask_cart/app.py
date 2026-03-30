# установка: pip install flask
# запуск: python app.py
from flask import Flask, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'secret123'

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
    return render_template('index.html', catalog=catalog, cart_count=len(cart_ids))


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
    return render_template('cart.html', items=items, total=total)


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
