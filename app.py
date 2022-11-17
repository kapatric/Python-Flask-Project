from flask import Flask, request, jsonify
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('designer', user='postgres', password='', host='localhost', port=5432)

class BaseModel(Model):
  class Meta:
    database = db

class Desinger(BaseModel):
  name = CharField()
  established = IntegerField()

db.connect()
db.drop_tables([Designer])
db.create_tables([Designer])

Designer(name='Comme de Garçon', established=1969).save()
Designer(name='Theophilio', established=2016).save()
Designer(name='Dion Lee', established=2010).save()
Designer(name='Telfar', established=2005).save()

app = Flask(__name__)

# Define our route
# This syntax is using a Python decorator, which is essentially a succinct way to wrap a function in another function.

@app.route('/person/', methods=['GET', 'PPOST'])
@app.route('/designer/<id>', methods=['GET', 'PUT', 'POST', 'DELETE'])
def endpoint(id=None):
  if request.method == 'GET':
    if id: 
      return jsonify(model_to_dict(Desinger.get(Desinger.id == id)))
    else:
        designer_list =[]
        for desinger in Designer.select():
          designer_list.append(model_to_dict(desinger))
    return jsonify(desinger_list)
      
  if request.method == 'PUT':
    return 'PUT request'

  if request.method == 'POST':
    return 'POST request'

  if request.method == 'DELETE':
    return 'DELETE request'

# Run our application, by default on port 5000
app.run(port=9000, debug=True)