from src.schemas.Websocket import UserRoomSchema


class RoomUser:
    id_user: str
    sid_user: str
    is_owner: bool

    def __init__(self, id_user, sid_user, is_owner):
        self.id_user = id_user
        self.sid_user = sid_user
        self.is_owner = is_owner

    def __repr__(self):
        return f"<RoomUser id_user={self.id_user} sid_user={self.sid_user} is_owner={self.is_owner}>"


class Room:
    id_room: str
    id_owner: str
    users: list[RoomUser]

    def __init__(self, id_room, id_owner):
        self.id_room = id_room
        self.id_owner = id_owner
        self.users = []

    def join(self, id_user, sid_user, is_owner):
        self.users.append(RoomUser(id_user=id_user, sid_user=sid_user, is_owner=is_owner))

    def leave(self, sid_user):
        self.users = list(filter(lambda user: user.sid_user != sid_user, self.users))

    def len(self):
        return len(self.users)

    def get_users(self):
        uniq_users: list[RoomUser] = []
        for user in self.users:
            is_uniq = True
            for uniq_user in uniq_users:
                if uniq_user.id_user == user.id_user:
                    is_uniq = False
                    break
            if is_uniq:
                uniq_users.append(user)
        schema = UserRoomSchema(many=True, exclude=('sid_user',))
        return schema.dump(uniq_users)

    def __repr__(self):
        return f"<Room id_room={self.id_room} id_owner={self.id_owner}>"


class RoomsService:
    rooms: list[Room] = []

    @classmethod
    def create(cls, room_id, id_user, sid_user):
        room = Room(id_room=room_id, id_owner=id_user)
        room.join(id_user=id_user, sid_user=sid_user, is_owner=True)
        RoomsService.add(room)
        return room

    @classmethod
    def add(cls, room: Room):
        cls.rooms.append(room)

    @classmethod
    def remove(cls, room_id):
        cls.rooms = list(filter(lambda room: room.id_room != room_id, cls.rooms))

    @classmethod
    def get(cls, room_id):
        try:
            return list(filter(lambda room: room.id_room == room_id, cls.rooms))[0]
        except IndexError:
            return None

    @classmethod
    def get_user(cls, sid=None, id_user=None) -> tuple[RoomUser | None, Room | None]:
        for room in RoomsService.rooms:
            for user in room.users:
                if user.sid_user == sid or user.id_user == id_user:
                    return user, room
        return None, None
