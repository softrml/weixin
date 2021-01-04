from rmlHelper import *
import random

class AutoMsg(object):
    def __init__(self,name):
        self.rule = loadJson(name+'.json')

    def getName(self):
        return self.rule.get('name')

    def getRandom(self):
        return self.rule.get('random')

    def handle(self,msg):
        if self.rule.get('name') in msg.actualNickName:
            randomList = self.getRandom()
            if len(randomList) > 0:
                msg.User.send( random.choice(randomList) )