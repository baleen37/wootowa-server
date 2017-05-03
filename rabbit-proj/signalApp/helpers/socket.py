from socketio import BaseManager

class SocketManager(BaseManager):

    def get_clients(self, namespace='/'):
        return self.rooms[namespace].get(None, None)
