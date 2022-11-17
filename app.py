from flask import Flask, request, jsonify
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('designers', user='khristopherpatrick', password='', host='localhost', port=5432)

class BaseModel(Model):
  class Meta:
    database = db

class Designer(BaseModel):
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

@app.route('/designer/', methods=['GET', 'POST'])
@app.route('/designer/<id>', methods=['GET', 'PUT', 'POST', 'DELETE'])
def endpoint(id=None):
  if request.method == 'GET':
    if id: 
      return jsonify(model_to_dict(Designer.get(Designer.id == id)))
    else:
        designer_list =[]
        for designer in Designer.select():
          designer_list.append(model_to_dict(designer))
    return jsonify(designer_list)
      
  if request.method == 'PUT':
    body = request.get_json()
    Designer.update(body).where(Designer.id == id).execute()
    return "Designer " + str(id) + " has been updated!"

  if request.method == 'POST':
    new_designer = dict_to_model(Designer, request.get_json())
    new_designer.save()
    return jsonify({"success": True})

  if request.method == 'DELETE':
    Designer.delete().where (Designer.id == id).execute()
    return "Designer " + str(id) + " deleted!"

# Run our application, by default on port 5000
app.run(port=9000, debug=True)