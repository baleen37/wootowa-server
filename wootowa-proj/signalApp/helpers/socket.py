from socketio import BaseManager

class SocketManager(BaseManager):

    awaiter_list = []
    sid_dict = {} #{'uid': 'sid'}

    def add_awaiter(self, sid):
        '''
        대기열에 넣어둠
        '''
        if not sid in self.awaiter_list:
            return self.awaiter_list.append(sid)

    def remove_awaiter(self, sid):
        '''
        대기열에서 뻄.
        '''
        if sid in self.awaiter_list:
            return self.awaiter_list.remove(sid)

    def clear(self, sid):
        '''
        메모리 릭 안나게 정리
        '''
        print('manager.clear')
        self.remove_awaiter(sid)
        self.remove_uid(sid)

    def add_uid(self, uid, sid):
        self.sid_dict[uid] = sid

    def remove_uid(self, uid):
        return self.sid_dict.pop(uid, None)

    def get_sid(self, uid):
        return self.sid_dict.get(uid, None)

    def get_uid(self, sid):
        for uid, target_sid in self.sid_dict.items():
            if target_sid == sid:
                return uid

    def get_awaiter_list(self):
        return self.awaiter_list

    def get_clients(self, namespace='/'):
        if self.rooms.get(namespace, None):
            return self.rooms[namespace].get(None, None)
        return []
