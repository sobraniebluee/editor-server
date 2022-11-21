from flask import Blueprint, request
from flask_socketio import join_room, leave_room, emit, send

from src import socketio
from src.middlewares.auth_required import auth_required, UserIdentify
from src.schemas.Websocket import UserRoomSchema
from src.services.websocket.RoomService import RoomsService

websocket = Blueprint('websocket', __name__)


@socketio.on('connect')
def connect():
    print('-------- Connect --------')


@socketio.on('disconnect')
def disconnect():
    sid = request.sid
    user, room = RoomsService.get_user(sid)
    if user and room:
        room.leave(sid_user=sid)
        leave_room(sid)
        schema = UserRoomSchema(many=True)
        socketio.emit("LEAVE_CODE:MESSAGE", schema.dump(room.users), broadcast=True, to=room.id_room)


@socketio.on('JOIN_CODE')
@auth_required(request=request)
def join(data: dict, identify: UserIdentify):
    sid = request.sid
    room_id = data.get('room', None)
    is_owner = data.get('is_owner', None)

    if room_id is None or is_owner is None:
        print('join error')
        return

    room = RoomsService.get(room_id)

    if not room:
        if not is_owner:
            print("error owner")
            return
        room = RoomsService.create(room_id=room_id, id_user=identify.id_user, sid_user=sid)
    else:
        room.join(id_user=identify.id_user, sid_user=sid, is_owner=is_owner)

    join_room(room=room_id, sid=sid)
    schema = UserRoomSchema(many=True)
    socketio.emit('JOIN_CODE:MESSAGE', schema.dump(room.users), broadcast=True, to=room_id)


@socketio.on('LEAVE_CODE')
@auth_required(request=request, optional=True)
def leave(data: dict, identify: UserIdentify):
    sid = data.get('sid', request.sid)
    room_id = data.get('room', None)
    is_owner = data.get('is_owner', None)

    if room_id is None or is_owner is None:
        print('leave error')
        return

    room = RoomsService.get(room_id)
    if not room:
        return

    room.leave(sid)
    leave_room(room_id, sid)
    schema = UserRoomSchema(many=True)
    socketio.emit("LEAVE_CODE:MESSAGE", schema.dump(room.users), broadcast=True, to=room_id)


@socketio.on('SET_VALUE')
@auth_required(request=request)
def set_value(data, identify: UserIdentify):
    value = data.get('value', None)

    user, room = RoomsService.get_user(id_user=identify.id_user)
    if value and user and room:
        # emit("SET_VALUE:MESSAGE", {"value": value},include_self=False, broadcast=True, to=room.id_room)
        send({"value": value}, include_self=False, broadcast=True, to=room.id_room)


@socketio.on('JOIN_CODE:MESSAGE')
def join_msg(data):
    socketio.send(data)


@socketio.on('LEAVE_CODE:MESSAGE')
def leave_msg(data):
    socketio.send(data)


@socketio.on('SET_VALUE:MESSAGE')
def set_value_msg(data):
    socketio.send(data)


@socketio.on('ERROR:MESSAGE')
def error_msg(data):
    socketio.send(data)

# @socketio.on('DESTROY_ROOM')



