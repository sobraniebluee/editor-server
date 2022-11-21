class RoomUser:
    id_user: str
    sid_user: str
    is_owner: bool

    def __init__(self, id_user, sid_user, is_owner):
        self.id_user = id_user
        self.sid_user = sid_user
        self.is_owner = is_owner

    def __repr__(self):
        return f"<UserRoom id_user={self.id_user} sid_user={self.sid_user} is_owner={self.is_owner}>"


class Room:
    id_room: str
    id_owner: str
    users: list[RoomUser] = []

    def __init__(self, id_room, id_owner):
        self.id_room = id_room
        self.id_owner = id_owner

    def join(self, id_user, sid_user, is_owner):
        try:
            user = list(filter(lambda u: u.id_user == id_user, self.users))[0]
            user.sid_user = sid_user
        except IndexError:
            self.users.append(RoomUser(id_user=id_user, sid_user=sid_user, is_owner=is_owner))

    def leave(self, sid_user):
        self.users = list(filter(lambda x: x.sid_user != sid_user, self.users))

    def len(self):
        return len(self.users)

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

# r = Room(id_room=1, id_owner=12)
# r.join(id_user='1', sid_user='dkdk', is_owner=True)
# r.join(id_user='1', sid_user='fkfkfk', is_owner=False)
# print(r.len())
#
# r.leave(sid_user='fkfkfk')
#
# print(r.users)
# print(r.len())