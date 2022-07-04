from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta
from static.python.calculateSummary import calculateSummary
from constants.constants import CONSTANTS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///materials.db'
db = SQLAlchemy(app)


class MaterialItem(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(30), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    deliveryDate = db.Column(db.Date, nullable=False)
    dateAdded = db.Column(db.Date, nullable=False,
                          default=datetime.now().date())
    timeAdded = db.Column(db.Time, nullable=False,
                          default=datetime.now().time())

    def __repr__(self):
        return 'Material item ' + str(self.id)


# db.create_all() shall be executed only once, to create database
# db.create_all()

@app.route('/')
def show_main_page():
    return render_template('mainMenu.html')


@app.route('/materials', methods=['GET', 'POST'])
def show_materials():

    if request.method == 'POST':
        searchCriteria = dict()
        searchCriteria['sortingOrder'] = request.form['sortingOrder']
        searchCriteria['filterBalance'] = request.form['filterBalance']
        searchCriteria['filterHistory'] = request.form['filterHistory']

        searchCriterion = getattr(
            MaterialItem, searchCriteria['sortingOrder'].split(" ")[0])

        if searchCriteria['filterHistory'] == 'futureTrades':
            firstDayToScope = date.today()
            lastDayToScope = date.max
        elif searchCriteria['filterHistory'] == 'fromVeryBeginning':
            firstDayToScope = date.min
            lastDayToScope = date.max
        else:
            timeSpan = timedelta(int(searchCriteria['filterHistory']))
            today = date.today()
            firstDayToScope = today - timeSpan
            lastDayToScope = today

        if searchCriteria['filterBalance'] == 'soldMaterials':
            balanceFilter = MaterialItem.weight < 0
        elif searchCriteria['filterBalance'] == 'purchasedMaterials':
            balanceFilter = MaterialItem.weight >= 0
        else:
            balanceFilter = True

        materials = MaterialItem.query.order_by(searchCriterion).filter(MaterialItem.deliveryDate >= firstDayToScope,
                                                                        MaterialItem.deliveryDate <= lastDayToScope, balanceFilter).all()
        direction = searchCriteria['sortingOrder'].split(" ")[-1]

        if direction == 'desc':
            materials.reverse()

        summary = dict()
        summary = calculateSummary(materials)

        return render_template('materials.html', materials=materials, summary=summary, constants=CONSTANTS)
    else:

        if 'searchCriteria' not in locals():
            materials = MaterialItem.query.order_by(MaterialItem.id).all()
        else:
            materials = MaterialItem.query.order_by(MaterialItem.title).all()

        summary = dict()
        summary = calculateSummary(materials)

        return render_template('materials.html', materials=materials, summary=summary, constants=CONSTANTS)


@app.route('/materials/delete/<int:id>')
def delete(id):

    material = MaterialItem.query.get_or_404(id)
    db.session.delete(material)
    db.session.commit()

    return redirect('/materials')


@app.route('/materials/view/<int:id>')
def view(id):

    material = MaterialItem.query.get_or_404(id)

    return render_template('view.html', material=material)


@app.route('/materials/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    material = MaterialItem.query.get_or_404(id)
    if request.method == 'POST':
        material.title = request.form['titleEdit']
        material.weight = request.form['weightEdit']
        material.category = request.form['categoryEdit']
        material.description = request.form['descriptionEdit']
        material.deliveryDate = datetime.strptime(
            request.form['deliveryDateEdit'], "%Y-%m-%d")
        material.dateAdded = datetime.now().date()
        material.timeAdded = datetime.now().time()
        db.session.commit()
        return redirect('/materials')

    else:
        return render_template('edit.html', material=material, constants=CONSTANTS)


@app.route('/materials/new', methods=['GET', 'POST'])
def new_material():

    if request.method == 'POST':
        material_title = request.form['title']
        material_weight = request.form['weight']
        material_category = request.form['category']
        material_description = request.form['description']
        time = datetime.strptime(request.form['deliveryDate'], "%Y-%m-%d")
        deliveryDate = date(time.year, time.month, time.day)
        new_material = MaterialItem(title=material_title, weight=material_weight,
                                    category=material_category, description=material_description, deliveryDate=deliveryDate,
                                    dateAdded=datetime.now().date(), timeAdded=datetime.now().time())
        db.session.add(new_material)
        db.session.commit()

        return redirect('/materials')

    else:
        return render_template('addNew.html', constants=CONSTANTS)


if __name__ == '__main__':
    app.run(debug=True)
