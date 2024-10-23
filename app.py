from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Episode, Guest, Appearance
from sqlalchemy.exc import DatabaseError


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/episodes', methods=["GET"])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([episode_item.episode_serialize() for episode_item in episodes])

@app.route('/episodes/<int:id>', methods=["GET", "DELETE"])
def get_episode_by_id(id):
    episode = Episode.query.filter_by(id=id).first()

    if not episode:
        return jsonify({"error": "Episode not found"}), 404


    if request.method == "GET":
        return jsonify(episode.single_episode_serialize())
    else:
        db.session.delete(episode)
        db.session.commit()
        
        return jsonify(""), 204

@app.route('/guests', methods=["GET"])
def get_guests():
    guests = Guest.query.all()
    return jsonify([guest_item.guest_serialize() for guest_item in guests])

@app.route('/appearances', methods=["POST"])
def create_appearance():
    try:
        data = request.get_json()
        rating = data.get("rating")
        episode_id = data.get("episode_id")
        guest_id = data.get("guest_id")
        appearance= Appearance(rating=rating, episode_id=episode_id, guest_id=guest_id)
        
        db.session.add(appearance)
        db.session.commit()
        return jsonify(appearance.create_appearance_serialize()), 201
    except DatabaseError as error:
        return jsonify({"errors": error.messages}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5555)