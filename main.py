import random
import time
import json
import threading


class Global(object):
    """Global var"""
    __global = None

    def __init__(self):
        self.data = {}  # 保存数据
        self.mutex = False  # 线程间安全锁
        self.process = 15  # 开启线程数量
        self.total_times = 100000 	# 总次数
        self.change_times = 0		# 执行换次数
        self.unchange_times = 0		# 执行不换次数
        self.change_wins = 0  	 	# 换胜利次数
        self.unchange_wins = 0  	# 不换胜利次数

    def stop(self):
        return self.change_times + self.unchange_times + self.process > self.total_times

    def save(self):
        data = {
            'total_times': self.total_times,
            'change_times': self.change_times,
            'unchange_times': self.unchange_times,
            'change_wins': self.change_wins,
            'unchange_wins': self.unchange_wins,
            'change_pro': self.change_wins * 1.0 / self.change_times,
            'unchange_pro': self.unchange_wins * 1.0 / self.unchange_times,
        }
        with open("data.json", 'w', encoding='utf-8') as w:
            json.dump(data, w, ensure_ascii=False)

    @staticmethod
    def get_instance():
        if Global.__global is None:
            Global.__global = Global()
        return Global.__global


_global = Global.get_instance


def getRand(_list):
    return random.sample(_list, 1)[0]


def run():
    while True:
        _list = [0, 1, 2]
        winner_door = getRand(_list)  # 有奖品的门 0,1,2
        player_door = getRand(_list)  # 玩家选择的门 0,1,2
        # delete_door 主持人打开的门 0,1,2
        if winner_door == player_door:
            _list.pop(winner_door)
            delete_door = getRand(_list)
        else:
            if winner_door > player_door:
                _list.pop(winner_door)
                _list.pop(player_door)
            else:
                _list.pop(player_door)
                _list.pop(winner_door)
            delete_door = _list[0]
        change = getRand([True, False])
        while _global().mutex:
            time.sleep(1)
        _global().mutex = True
        if change:
            _global().change_times += 1
            _global().change_wins += 1 if player_door != winner_door else 0
        else:
            _global().unchange_times += 1
            _global().unchange_wins += 1 if player_door == winner_door else 0
        _global().mutex = False
        if _global().stop():
            break


if __name__ == '__main__':
    threads = []
    for i in range(_global().process):
        t = threading.Thread(target=run)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    _global().save()
    print('finish')
