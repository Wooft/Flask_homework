import gunicorn
from flask import Flask, request, jsonify
from flask.views import MethodView
from schema import validate_create_user
from errors import HttpError
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt

from db import Session, User, Announcement

app = Flask('server')
bcrypt = Bcrypt(app)

@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    http_response = jsonify({'status': 'error',
                             'description': error.message})
    http_response.status_code = error.status_code
    return http_response

def get_user(user_id: int, session: Session):
    user = session.query(User).get(user_id)
    if user is None:
        raise HttpError(status_code=404, message='User not found')
    return user

def is_owner(id: int, password: str, session: Session):
    user = get_user(user_id=id, session=session)
    if bcrypt.check_password_hash(user.password, password):
        return True
    else:
        raise HttpError(status_code=401, message='authorization data is not correct')


def get_announcement(id: int, session: Session):
    announcement = session.query(Announcement).get(id)
    if announcement is None:
        raise HttpError(status_code=400, message='announcement not found')
    return announcement
#Проверка наличия указания владельца объявления и пароля для запуска дальнейших действий
def check_authorization_date(json_data):
    if json_data.get('owner') == None or json_data.get('password') == None:
        raise HttpError(status_code=401, message='Need owner password for this action')
    else:
        return True

class AnnouncmentView(MethodView):

    def get(self, id: int):
        with Session() as session:
            announcement = get_announcement(id=id, session=session)
            return jsonify({
                'title': announcement.title,
                'description': announcement.description,
                'owner': get_user(user_id=announcement.owner, session=session).name,
                'created_at': announcement.creation_time
            })

    def post(self):
        json_data = request.json
        with Session() as session:
            # проверка соотвествия пароля
            if is_owner(id=json_data['owner'], password=json_data['password'], session=session):
                json_data.pop('password') #Удаление ненужных данных для создания объявления
                new_announcment = Announcement(**json_data)
                session.add(new_announcment)
                session.commit()
                return jsonify({
                    'title': new_announcment.title,
                    'description': new_announcment.description,
                    'creation_time': new_announcment.creation_time,
                    'owner': get_user(user_id=new_announcment.owner, session=session).name,
                })

    def patch(self, id: int):
        json_data = request.json
        if check_authorization_date(json_data):
            with Session() as session:
                if is_owner(id=json_data['owner'], password=json_data['password'], session=session):
                    announcement = get_announcement(id, session)
                    for field, value in json_data.items():
                        setattr(announcement, field, value)
                    session.add(announcement)
                    session.commit()
            return jsonify({'status': 'success'})

    def delete(self, id: int):
        json_data = request.json
        if check_authorization_date(json_data=json_data):
            with Session() as session:
                print(is_owner(id=json_data['owner'], password=json_data['password'], session=session))
                if is_owner(id=json_data['owner'], password=json_data['password'], session=session):
                    announcement = get_announcement(id,session)
                    session.delete(announcement)
                    session.commit()
                    return jsonify({'status': f'announcement title:"{announcement.title}" has been removed'})

class UserView(MethodView):

    def get(self, user_id: int):
        with Session() as session:
            user = get_user(user_id, session)
            return jsonify({
                'id': user.id,
                'Name': user.name
            })

    def post(self):
        json_data = validate_create_user(request.json)
        json_data['password'] = bcrypt.generate_password_hash(json_data['password'].encode()).decode()

        with Session() as session:
            new_user = User(**json_data)
            session.add(new_user)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, message='User already exists')
            return jsonify(
                {
                    'id': new_user.id,
                    'name': new_user.name,
                    'password': new_user.password
                }
            )

    def patch(self, user_id):
        json_data = request.json
        if json_data.get('password') != None:
            json_data['password'] = bcrypt.generate_password_hash(json_data['password'].encode()).decode()

        with Session() as session:
            user = get_user(user_id, session)
            for field, value in json_data.items():
                setattr(user, field, value)
            session.add(user)
            session.commit()
        return jsonify({'status': 'success'})

    def delete(self, user_id):
        with Session() as session:
            user = get_user(user_id, session)
            session.delete(user)
            session.commit()
        return jsonify({'status': 'user has been removed'})


app.add_url_rule('/users/<int:user_id>', view_func=UserView.as_view('UsersView'), methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/users', view_func=UserView.as_view('userpost'), methods=["POST"])
app.add_url_rule('/announcment', view_func=AnnouncmentView.as_view('announcment'), methods=["POST"])
app.add_url_rule('/announcment/<int:id>', view_func=AnnouncmentView.as_view('announcment_get'), methods=['GET', 'PATCH', 'DELETE'])

app.run()