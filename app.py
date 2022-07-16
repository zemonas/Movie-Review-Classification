from flask import Flask, request, jsonify, render_template, redirect
import prediction as p
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///records.db'
db = SQLAlchemy(app)


class history(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.String(200), nullable=False)
    res = db.Column(db.Boolean, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route("/")
def hello():
    records = history.query.order_by(history.date_created).all()
    return render_template("index.html", records=records)


@app.route("/predict", methods=['POST'])
def prediction():
    review = request.form["review"]
    pred = p.prediction(review)
    prediction = pred[0]
    if(prediction == 'neg'):
        prediction = 0
    if(prediction == 'pos'):
        prediction = 1
    new_review = history(review=review, res=prediction)
    print(prediction)
    try:
        db.session.add(new_review)
        db.session.commit()
        return redirect('/')
    except:
        return 'there was an issue adding task in records'


if __name__ == "__main__":
    app.run(debug=True)
