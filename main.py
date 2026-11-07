# from fastapi import FastAPI

# app = FastAPI(title='MAGAZIN')

# next_id = +1

# user_login = None

# user_list = [
#     {
#         'id': 1,
#         'name' : 'Ali',
#         'phone' : '01010101'
#     },


#     {
#         'id':2,
#         'name':'Jurabek',
#         'phone':'400400400'
#     },
# ]

# category_list = [
#     {
#         'id': 1,
#         'title': 'Phones'
#     },
# ]

# product_list = [
#     {
#         'id':1,
#         'title': 'Phone'
#     },
# ]

# order_list = [
#     {
#         'id':1,
#         'user_id':1,
#         'product_id':1,
#         'category_id':1
#     },
# ]





# @app.post('/products-post')
# async def create_products(title:str):
#     global next_id 
#     next_id += 1

#     products = {
#         'id': next_id,
#         'title': title
#     }
#     product_list.append(products)
#     return products

# @app.post('/register')
# async def create_user(name:str, phone: str):
#     global next_id
#     for user in user_list:
#         if user ['name'] == name:
#             return {'message' : 'User allready exist!'} 
#     new_user =  {
#         'id': next_id,
#         'name':name,
#         'phone': phone
#     }

#     user_list.append(new_user)
#     return new_user


# @app.post('/login')
# async def login_user(name:str, phone:str):
#     global user_login

#     for user in user_list:
#         if user['name'] == name and user['phone'] == phone:
#             user_login = user
#             return{'message':'User logined succesfully!'}

#     return "Etot user ne zaloginen!"


# @app.post('/logout')
# async def logout_user():
#     global user_login
#     user_login = None
#     return {'message':'Ti uspewno viwel is svoego accauna!'}


# @app.get('/products')
# async def show_products():
#     return product_list


# @app.post('/create-products')
# async def create_products(title:str):
#     global next_id
#     next_id += 1
#     new_product = {
#         'id':next_id,
#         'title': title
#     }
#     product_list.append(new_product)
#     return new_product


# @app.put('/update-product{product_id}')
# async def update_product(product_id:int, title:str):
#     for product in product_list:
#         if product['id'] == product_id:
#             product['title'] = title
#             return{'message':'Product uspewno obnovlen!'}

#     return {'message': 'Product s takim ID ne suwestvuet!'}

from fastapi import FastAPI, HTTPException

app = FastAPI(title='MAGAZIN')

next_id = 10

user_login = None

user_list = [
    {'id': 1, 'username': 'Ali', 'password': '01010101'},
    {'id': 2, 'username': 'Jurabek', 'password': '400400400'},
]

category_list = [
    {'id': 1, 'title': 'Phones'},
]

product_list = [
    {'id': 1, 'title': 'iPhone 15', 'price': 1200, 'category_id': 1},
]

order_list = [
    {'id': 1, 'user_id': 1},
]

order_items_list = [
    {'id': 1, 'order_id': 1, 'product_id': 1, 'quantity': 2},
]


@app.post('/register')
async def create_user(username: str, password: str):
    global next_id
    for user in user_list:
        if user['username'] == username:
            raise HTTPException(status_code=400, detail='User allready exist!')
    next_id += 1
    new_user = {'id': next_id, 'username': username, 'password': password}
    user_list.append(new_user)
    return {'id': new_user['id'], 'username': new_user['username']}


@app.post('/login')
async def login_user(username: str, password: str):
    global user_login
    for user in user_list:
        if user['username'] == username and user['password'] == password:
            user_login = user
            return {'message': 'User logined succesfully!'}
    raise HTTPException(status_code=401, detail='Etot user ne zaloginen!')


@app.post('/logout')
async def logout_user():
    global user_login
    user_login = None
    return {'message': 'Ti uspewno viwel is svoego accauna!'}


@app.post('/create-category')
async def create_category(title: str):
    global next_id
    next_id += 1
    new_category = {'id': next_id, 'title': title}
    category_list.append(new_category)
    return new_category


@app.post('/create-products')
async def create_products(title: str, price: int, category_id: int):
    global next_id
    category_found = False
    for category in category_list:
        if category['id'] == category_id:
            category_found = True
    if category_found == False:
        raise HTTPException(status_code=404, detail='Kategoriya ne naydena!')
    next_id += 1
    new_product = {
        'id': next_id,
        'title': title,
        'price': price,
        'category_id': category_id
    }
    product_list.append(new_product)
    return new_product


@app.post('/create-order')
async def create_order(user_id: int):
    global next_id
    user_found = False
    for user in user_list:
        if user['id'] == user_id:
            user_found = True
    if user_found == False:
        raise HTTPException(status_code=404, detail='User ne nayden!')
    next_id += 1
    new_order = {'id': next_id, 'user_id': user_id}
    order_list.append(new_order)
    return new_order


@app.get('/products')
async def show_products():
    return product_list


@app.get('/users/{user_id}')
async def get_user(user_id: int):
    for user in user_list:
        if user['id'] == user_id:
            return {'id': user['id'], 'username': user['username']}
    raise HTTPException(status_code=404, detail='User ne nayden!')


@app.patch('/users/{user_id}')
async def update_user(user_id: int, username: str = None, password: str = None):
    for user in user_list:
        if user['id'] == user_id:
            if username is not None:
                for other in user_list:
                    if other['username'] == username and other['id'] != user_id:
                        raise HTTPException(status_code=400, detail='Takoy username uje zanyat!')
                user['username'] = username
            if password is not None:
                user['password'] = password
            return {'id': user['id'], 'username': user['username']}
    raise HTTPException(status_code=404, detail='User ne nayden!')


@app.delete('/users/{user_id}')
async def delete_user(user_id: int):
    global user_login
    for user in user_list:
        if user['id'] == user_id:
            for order in order_list:
                if order['user_id'] == user_id:
                    raise HTTPException(status_code=400, detail='U usera est zakazi, udalit nelzya!')
            user_list.remove(user)
            if user_login is not None and user_login['id'] == user_id:
                user_login = None
            return {'message': 'User udalen!'}
    raise HTTPException(status_code=404, detail='User ne nayden!')


@app.get('/categories/{category_id}')
async def get_category(category_id: int):
    for category in category_list:
        if category['id'] == category_id:
            return category
    raise HTTPException(status_code=404, detail='Kategoriya ne naydena!')


@app.put('/categories/{category_id}')
async def update_category(category_id: int, title: str):
    if title.strip() == '':
        raise HTTPException(status_code=400, detail='Nazvanie ne dolgno bit pustim!')
    for category in category_list:
        if category['id'] == category_id:
            category['title'] = title
            return category
    raise HTTPException(status_code=404, detail='Kategoriya ne naydena!')


@app.delete('/categories/{category_id}')
async def delete_category(category_id: int):
    for category in category_list:
        if category['id'] == category_id:
            for product in product_list:
                if product['category_id'] == category_id:
                    raise HTTPException(status_code=400, detail='K kategorii privyazani tovari, udalit nelzya!')
            category_list.remove(category)
            return {'message': 'Kategoriya udalena!'}
    raise HTTPException(status_code=404, detail='Kategoriya ne naydena!')


@app.get('/categories/{category_id}/products')
async def get_category_products(category_id: int):
    for category in category_list:
        if category['id'] == category_id:
            result = []
            for product in product_list:
                if product['category_id'] == category_id:
                    result.append(product)
            return result
    raise HTTPException(status_code=404, detail='Kategoriya ne naydena!')


@app.get('/products/search')
async def search_products(title: str):
    result = []
    for product in product_list:
        if title.lower() in product['title'].lower():
            result.append(product)
    return result


@app.get('/products/filter')
async def filter_products(min_price: int = None, max_price: int = None):
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(status_code=400, detail='min_price bolshe max_price!')
    result = []
    for product in product_list:
        if min_price is not None and product['price'] < min_price:
            continue
        if max_price is not None and product['price'] > max_price:
            continue
        result.append(product)
    return result


@app.get('/products/{product_id}')
async def get_product(product_id: int):
    for product in product_list:
        if product['id'] == product_id:
            category_title = None
            for category in category_list:
                if category['id'] == product['category_id']:
                    category_title = category['title']
            return {
                'id': product['id'],
                'title': product['title'],
                'price': product['price'],
                'category_id': product['category_id'],
                'category_title': category_title
            }
    raise HTTPException(status_code=404, detail='Tovar ne nayden!')


@app.patch('/products/{product_id}')
async def update_product(product_id: int, title: str = None, price: int = None, category_id: int = None):
    for product in product_list:
        if product['id'] == product_id:
            if price is not None and price <= 0:
                raise HTTPException(status_code=400, detail='Cena doljna bit polojitelnoy!')
            if category_id is not None:
                category_found = False
                for category in category_list:
                    if category['id'] == category_id:
                        category_found = True
                if category_found == False:
                    raise HTTPException(status_code=404, detail='Kategoriya ne naydena!')
                product['category_id'] = category_id
            if title is not None:
                product['title'] = title
            if price is not None:
                product['price'] = price
            return product
    raise HTTPException(status_code=404, detail='Tovar ne nayden!')


@app.delete('/products/{product_id}')
async def delete_product(product_id: int):
    for product in product_list:
        if product['id'] == product_id:
            for item in order_items_list:
                if item['product_id'] == product_id:
                    raise HTTPException(status_code=400, detail='Tovar est v zakazah, udalit nelzya!')
            product_list.remove(product)
            return {'message': 'Tovar udalen!'}
    raise HTTPException(status_code=404, detail='Tovar ne nayden!')


@app.get('/orders/{order_id}')
async def get_order(order_id: int):
    for order in order_list:
        if order['id'] == order_id:
            items = []
            for item in order_items_list:
                if item['order_id'] == order_id:
                    for product in product_list:
                        if product['id'] == item['product_id']:
                            items.append({
                                'quantity': item['quantity'],
                                'product': product
                            })
            return {'id': order['id'], 'user_id': order['user_id'], 'items': items}
    raise HTTPException('Zakaz ne nayden!')


@app.post('/orders/{order_id}/items')
async def add_order_item(order_id: int, product_id: int, quantity: int):
    global next_id

    if quantity <= 0:
        raise HTTPException('quantity doljen bit bolshe 0!')

    order_found = False
    for order in order_list:
        if order['id'] == order_id:
            order_found = True
    if order_found == False:
        raise HTTPException('Zakaz ne nayden!')

    product_found = False
    for product in product_list:
        if product['id'] == product_id:
            product_found = True
    if product_found == False:
        raise HTTPException('Tovar ne nayden!')

    for item in order_items_list:
        if item['order_id'] == order_id and item['product_id'] == product_id:
            item['quantity'] += quantity
            return item

    next_id += 1
    new_item = {
        'id': next_id,
        'order_id': order_id,
        'product_id': product_id,
        'quantity': quantity
    }
    order_items_list.append(new_item)
    return new_item


@app.get('/orders/{order_id}/total')
async def get_order_total(order_id: int):
    for order in order_list:
        if order['id'] == order_id:
            total = 0
            for item in order_items_list:
                if item['order_id'] == order_id:
                    for product in product_list:
                        if product['id'] == item['product_id']:
                            total += product['price'] * item['quantity']
            return {'order_id': order_id, 'total': total}
    raise HTTPException('Zakaz ne nayden!')