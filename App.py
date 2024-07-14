from flask import Flask, render_template,request,redirect,url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
Bootstrap(app)

class Item(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    description=db.Column(db.String(200),nullable=False)

@app.route('/')
def index():
    items=Item.query.all()
    return render_template("index.html",items=items)

@app.route('/add',methods=['GET','POST'])
def add():
    if request.method=='POST':
        name=request.form['name']
        description=request.form['description']
        new_item=Item(name=name,description=description)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')
    
@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    item=Item.query.get_or_404(id)
    if request.method=='POST':
        item.name=request.form['name']
        item.description=request.form['description']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html',item=item)

@app.route('/delete/<int:id>',methods=['GET','POST'])
def delete(id):
        item=Item.query.get(id)
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/display')
def display():
    items = Item.query.all()
    return render_template('display.html', items=items)


if __name__=="__main__":
    app.run(debug=True)