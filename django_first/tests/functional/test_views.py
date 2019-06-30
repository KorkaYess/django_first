from lxml import html

from django_first.models import Order, Product


def test_hello(db, client, data):
    client.login(username='kira', password='testtest')
    response = client.get('/')
    assert response.status_code == 200
    response = response.content.decode('utf-8')
    assert 'Hello, World!' in response
    assert 'kira' in response
    response = html.fromstring(response)
    orders = Order.objects.filter(customer__user__username='kira')
    assert len(response.cssselect('li')) == orders.count()


def test_order_view(db, client, data):
    response = client.get('/orders/1/')
    assert response.status_code == 200
    response = response.content.decode('utf-8')
    response = html.fromstring(response)
    items = response.cssselect('.list-group-item')
    assert len(items) == 1
    assert items[0].text == 'apple 10'
    assert response.cssselect('#product') != []
    assert response.cssselect('#quantity') != []


def test_order_add_new(db, client, data):
    banana = Product.objects.create(name='banana', price=20)
    response = client.post(
        '/orders/1/',
        {'product': banana.id, 'quantity': 30}
    )
    assert response.status_code == 200
    response = response.content.decode('utf-8')
    response = html.fromstring(response)
    items = response.cssselect('.list-group-item')
    assert len(items) == 2
    assert items[0].text == 'apple 10'
    assert items[1].text == 'banana 30'


def test_order_add_same(db, client, data):
    response = client.post('/orders/1/', {'product': 1, 'quantity': 10})
    assert response.status_code == 200
    response = response.content.decode('utf-8')
    response = html.fromstring(response)
    items = response.cssselect('.list-group-item')
    assert len(items) == 1
    assert items[0].text == 'apple 20'


def test_order_add_empty_quantity(db, client, data):
    response = client.post('/orders/1/', {'product': 1, 'quantity': ''})
    assert response.status_code == 400
    response = response.content.decode('utf-8')
    assert response == 'Quantity must be a positive int'


def test_order_add_nonint_quantity(db, client, data):
    response = client.post('/orders/1/', {'product': 1, 'quantity': 'asd'})
    assert response.status_code == 400
    response = response.content.decode('utf-8')
    assert response == 'Quantity must be a positive int'


def test_order_add_zero_quantity(db, client, data):
    response = client.post('/orders/1/', {'product': 1, 'quantity': 0})
    assert response.status_code == 400
    response = response.content.decode('utf-8')
    assert response == 'Quantity must be a positive int'


def test_order_add_negative_quantity(db, client, data):
    response = client.post('/orders/1/', {'product': 1, 'quantity': -10})
    assert response.status_code == 400
    response = response.content.decode('utf-8')
    assert response == 'Quantity must be a positive int'


def test_order_add_product_doesnt_exist(db, client, data):
    response = client.post('/orders/1/', {'product': 10, 'quantity': '1'})
    assert response.status_code == 404
    response = response.content.decode('utf-8')
    assert response == 'Product not found'


def test_order_add_invalid_product_id(db, client, data):
    response = client.post('/orders/1/', {'product': 'asd', 'quantity': '1'})
    assert response.status_code == 400
    response = response.content.decode('utf-8')
    assert response == 'Invalid product id'
