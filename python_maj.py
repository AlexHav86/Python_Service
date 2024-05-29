from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy


# Инициализация Flask приложения
app = Flask(__name__)

# Конфигурация базы данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///consambles.db'

# Инициализация SQLAlchemy
db = SQLAlchemy(app)

# Определение длины строковых полей
num_string = 30

# Модель для таблицы "Consambles"
class Consambles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(num_string))
    category = db.Column(db.String(num_string))
    amount = db.Column(db.String(num_string))
    num_place = db.Column(db.String(num_string))

    def __init__(self, name, category, amount, num_place):
        self.name = name
        self.category = category
        self.amount = amount
        self.num_place = num_place

# Создание таблиц в базе данных
with app.app_context():
    db.create_all()

# Маршрут для добавления новой записи
@app.route('/add_consambles', methods=['POST'])
def add_consambles():
    name = request.form['name']
    category = request.form['category']
    amount = request.form['amount']
    num_place = request.form['num_place']
    consambles = Consambles(name, category, amount, num_place)
    db.session.add(consambles)
    db.session.commit()
    return {"session": "Consambles added successfully"}

# Маршрут для получения записи по id
@app.route('/get_consumables/<int:id>')
def get_consumables(id):
    consambles = Consambles.query.get(id)
    if consambles:
        return jsonify({
            'id': consambles.id,
            'name': consambles.name,
            'category': consambles.category,
            'units': consambles.amount,
            'num_place': consambles.num_place
        })
    else:
        return {'error': 'Consambles not found'}

# Маршрут для удаления записи по id
@app.route('/del_consumables/<int:id>', methods=['DELETE'])
def del_consumables(id):

        consambles = Consambles.query.get(id)
        if consambles:
            db.session.delete(consambles)
            db.session.commit()
            return {"session": "Consambles deleted successfully"}
        else:
            return {'error': 'Consambles not found'}



@app.route('/get_all_consumables', methods=['GET'])

def get_all_consumables():
    consumables = Consambles.query.all()
    return render_template('consumables_table.html', consumables=consumables)

# Запуск Flask приложения
if __name__ == "__main__":
    app.run(host="0.0.0.0")
