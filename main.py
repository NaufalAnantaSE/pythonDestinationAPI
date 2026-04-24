from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "country": self.country,
            "city": self.city,
            "rating": self.rating
        }
        
with app.app_context():
    AUTO_SYNC = True  
    if AUTO_SYNC == True:
        print("AUTO SYNC ENABLED: dropping & recreating tables")
        db.drop_all()   
        db.create_all() 
    else:
        db.create_all()

@app.route('/')
def home():
    return jsonify({"message": "Travel Destinations api"})

@app.route('/destinations', methods=['POST'])
def add_destination():
    data = request.get_json()
    new_destination = Destination(
        name=data['name'],
        description=data['description'],
        country=data['country'],
        city=data['city'],
        rating=data['rating']
    )
    db.session.add(new_destination)
    db.session.commit()
    return jsonify(new_destination.to_dict()), 201


if __name__ == '__main__':
    app.run(debug=True)