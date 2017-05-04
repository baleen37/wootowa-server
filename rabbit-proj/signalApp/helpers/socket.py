from socketio import BaseManager

class SocketManager(BaseManager):

    awaiter_list = []

    def add_awaiter(self, sid):
        if not sid in self.awaiter_list:
            return self.awaiter_list.append(sid)

    def remove_awaiter(self, sid):
        if sid in self.awaiter_list:
            return self.awaiter_list.remove(sid)

    def get_awaiter_list(self):
        return self.awaiter_list

    def get_clients(self, namespace='/'):
        return self.rooms[namespace].get(None, None)
