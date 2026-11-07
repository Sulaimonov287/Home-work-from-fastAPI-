
# from fastapi import FastAPI, HTTPException

# app = FastAPI(title='CRUD')

# next_id = 1

# student_list = [
#     {
#         'id': next_id,
#         'name': 'Mrod',
#         'surname': 'Mrodov',
#         'age': 18
#     },
# ]


# @app.get('/students')
# async def get_students():
#     return student_list


# @app.post('/create-student')
# async def create_student(name: str, surname: str, age: int = 20):
#     global next_id
#     next_id += 1

#     students = {
#         'id': next_id,
#         'name': name,
#         'surname': surname,
#         'age': age
#     }

#     student_list.append(students)
#     return students


# @app.put('/update-students/{student_id}')
# async def update_student(student_id: int, name: str, surname: str, age: int):
#     for st in student_list:
#         if st['id'] == student_id:
#             st['name'] = name
#             st['surname'] = surname
#             st['age'] = age
#             return st

#     raise HTTPException(status_code=404, detail='Student not found!')


# @app.patch('/student-update')
# async def patch_student(
#     s_id: int,
#     name: str | None = None,
#     surname: str | None = None,
#     age: int | None = None
# ):
#     for st in student_list:
#         if st['id'] == s_id:
#             if name is not None:
#                 st['name'] = name
#             if surname is not None:
#                 st['surname'] = surname
#             if age is not None:
#                 st['age'] = age
#             return st

#     raise HTTPException(status_code=404, detail='Student not found!')


# @app.delete('/delete-student/{student_id}')
# async def delete_student(student_id: int):
#     for st in student_list:
#         if st['id'] == student_id:
#             student_list.remove(st)
#             return {'message': 'Student deleted successfully!'}

#     raise HTTPException(status_code=404, detail='Student not found!')





from fastapi import FastAPI, HTTPException

app = FastAPI(title='INERNET_MAGAZIN')

user_login = None

next_id += 1

user_list = [
    {
        'id':1,
        'username':'Ali',
        'password': '2211'
    },
]

category_list = [
    {
        'id':1,
        'title':'Notebook'
    },
]


product_list = [
    {
        'id':1,
        'title':'Iphone',
        'price':1200,
        'category_id':1
    },
]


order_list = [
    {
        'id':1,
        'user_id':1  
    },
]


order_items_list = [
    {
        'id':1,
        'oder_id':1,
        'product_id':1,
        'quantity':2
    },
]


@app.post('/register')
async def register(username:str, password:str):
    global next_id
    for user in user_list:
        if user['username'] == username:
            raise HTTPException('this username allreasy exists!')
        next_id += 1
        new_user = {'id': next_id, 'username':username, 'password':password}
        user_list.append(new_user)
        return new_user


@app.post('/login')
async def login(username:str, password:str):
    global user_login
    for user in user_list:
        if user['username'] == username and user['password'] == password:
            user_login = user
            return {'message': "Logined succesfully!"}
        raise HTTPException('Etot user ne zaloginen!')


@app.post('/logout')
async def logout():
    global user_login
    user_login = None
    return 'Ti uspewno viwel is svoego accaunta!'

@app.post('/create-category')
async def create_category(title: str):
    for cat in category_list:
        if 