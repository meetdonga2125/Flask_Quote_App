from flask import Flask ,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# connect our app to postgres database(quotes)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres123@localhost/quotes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db = SQLAlchemy(app)


# create class that makes our table
class Favquotes(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	author = db.Column(db.String(30))
	quote = db.Column(db.String(2000))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
	results = Favquotes.query.all()
	return render_template('index.html',results= results)


@app.route('/quotes')
def quotes():
	 return render_template('quotes.html')

@app.route('/process', methods =['POST'])
def process():
	author = request.form['author']
	quote = request.form['quote']
	quotedata =Favquotes(author=author,quote=quote)
	# insert records into mapping table by db.session.add(model object)
	db.session.add(quotedata)  
	db.session.commit()
	return redirect(url_for('index'))
   

if __name__ == "__main__":
    app.run(debug=True)