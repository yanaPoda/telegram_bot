from s_taper import Taper
from s_taper.consts import INT,TEXT,FLT,KEY

scheme = {
    'id': INT + KEY,
    'username': TEXT,
    'name': TEXT,
    'age': FLT,
    'city': TEXT,
    'country': TEXT
}
table=Taper('users','data.db').create_table(scheme)

def write_row(data: dict[int,dict],user_id: int):
    data_in = data[user_id]
    username = data_in['username']
    name = data_in['name']
    age = data_in['age']
    city = data_in['city']
    country = data_in ['country']
    table.write([user_id,username,name,age,city,country])
    print('данные о пользователе успешно заполнены')


def read_row(user_id: int):
    table.read('id',user_id)