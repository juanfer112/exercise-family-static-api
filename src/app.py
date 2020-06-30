"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_members():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    if members:
        return jsonify(members), 200
    else:
        return jsonify(members), 400

@app.route('/member/<id>', methods=['GET'])
def handle_member(id):
    # this is how you can use the Family datastructure by calling its methods
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify(member), 400

@app.route('/member', methods=['POST'])
def post_member():
    # this is how you can use the Family datastructure by calling its methods
    body = request.get_json()
    if 'first_name' not in body or body['first_name'] == "":
        return 'Invalid member', 400 
    if 'age' not in body or body['age'] == "":
        return 'Invalid member', 400 
    if 'lucky_numbers' not in body or not body['lucky_numbers']:
        return 'Invalid member', 400     
    
    member = FamilyStructure(last_name='Jackson',first_name=body['first_name'], age=body['age'],lucky_numbers=body['lucky_numbers'])
    body['id'] = jackson_family._generateId()
    response = jackson_family.add_member(body)
    return jsonify(response), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def handle_del_member(id):
    # this is how you can use the Family datastructure by calling its methods
    member = jackson_family.delete_member(id)
    if member:
        return jsonify(member), 200    
    else:
        return 'member not found', 400


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
