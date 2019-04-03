from flask import Flask, jsonify, request
from flask_restful import reqparse, Api, Resource, abort
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json


docker_auth = "postgresql://wg_forge:42a@localhost:5432/wg_forge_db"
limit_per_minute = 600

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = docker_auth
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

api = Api(app)
db = SQLAlchemy(app)

limiter = Limiter(app, application_limits=[f'{limit_per_minute} per minute'],
                  key_func=get_remote_address)


class Cats(db.Model):

    def __init__(self, name, color, tail_length, whiskers_length):
        self.name = name
        self.color = color
        self.tail_length = tail_length
        self.whiskers_length = whiskers_length

    name = db.Column(db.String, unique=True, primary_key=True)
    color = db.Column(db.String)
    tail_length = db.Column(db.Integer)
    whiskers_length = db.Column(db.Integer)


class ApiCatsPing(Resource):
    def get(self):
        return 'Cats Service. Version 0.1', 200


class ApiCatsGet(Resource):
    def get(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('order', choices=('asc', 'desc'),
                            help='Bad order! Three is not a valid choice. '
                                 'Expecting any value from: asc, desc.')
        parser.add_argument('attribute', choices=('name',
                                                  'color',
                                                  'tail_length',
                                                  'whiskers_length'),
                            help='Bad attribute! Three is not a valid choice. '
                                 'Expecting any value from: name, color, '
                                 'tail_length, whiskers_length.')
        parser.add_argument('offset', type=int,
                            default=0, choices=range(0, 10000),
                            help='Bad offset! Three is not a valid choice. '
                                 'Expecting any value from 0 to 10000.')
        parser.add_argument('limit', type=int,
                            default=100, choices=range(1, 10000),
                            help='Bad limit! Three is not a valid choice. '
                                 'Expecting any value from 1 to 10000.')
        args = parser.parse_args(strict=True)

        if args.get('attribute'):

            if args.get('order') == 'asc':
                r = Cats.query.order_by(db.asc(args.get('attribute')))
            elif args.get('order') == 'desc':
                r = Cats.query.order_by(db.desc(args.get('attribute')))
            else:
                r = Cats.query.order_by(args.get('attribute'))
        else:
            r = Cats.query

        r = r.offset(args.get('offset')).limit(args.get('limit'))

        if r.count() == 0:
            message = "Offset is greater than the available data in database."
            return abort(400, message=message)

        response = []
        for cat in r.all():
            response.append(dict(name=cat.name,
                            color=cat.color,
                            tail_length=cat.tail_length,
                            whiskers_length=cat.whiskers_length))

        return jsonify(response)


class ApiCatsPost(Resource):
    def post(self):
        data = request.get_data().decode()

        try:
            data_json = json.loads(data)
        except json.decoder.JSONDecodeError:
            abort(400, message='Json Decode Error: '
                               'Invalid JSON data')

        avialible_colors = ['black', 'white', 'black & white',
                            'red', 'red & white', 'red & black & white']
        try:
            name = data_json.pop('name')

            if not name.isalpha():
                abort(400, message='Argument error! '
                                   'name must be is string object')
            color = data_json.pop('color')

            if color not in avialible_colors:
                abort(400, message='Argument error! '
                                   f'Expecting any value '
                                   f'from {avialible_colors}')
            tail_length = data_json.pop('tail_length')

            if tail_length not in range(1, 100):
                abort(400, message='Arguments error! '
                                   'Tail_length not in '
                                   'range from 1 to 100')
            whiskers_length = data_json.pop('whiskers_length')

            if whiskers_length not in range(1, 100):
                abort(400, message='Arguments error! '
                                   'Whiskers_length not '
                                   'in range from 1 to 100')
        except KeyError:
            abort(400, message='Arguments error! '
                               'name, color, tail_length, '
                               'whiskers_length is required!')
        if data_json:
            abort(400, message=f'Wrong arguments: {data_json}')

        if name in (cat.name for cat in Cats.query.all()):
            abort(409, message=f'Error! name {name} is already in database')

        new_cat = Cats(name=name,
                       color=color,
                       tail_length=tail_length,
                       whiskers_length=whiskers_length)

        Cats.query.session.add(new_cat)
        Cats.query.session.commit()

        return jsonify(status='ok', message='Cat added!')


api.add_resource(ApiCatsPing, '/ping')
api.add_resource(ApiCatsGet, '/cats')
api.add_resource(ApiCatsPost, '/cat')


if __name__ == '__main__':
    app.run(port=8080)
