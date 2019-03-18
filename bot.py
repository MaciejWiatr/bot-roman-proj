from fbchat import log, Client
from fbchat.models import *

from data import *

import random, traceback, time, wikipedia, re

class Bot(Client):

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):

        self.markAsDelivered(thread_id, message_object.uid)

        log.info("{} from {} of type {}".format(message_object.text, thread_id, thread_type.name))

        try:
            message_text = message_object.text.lower()
        except:
            message_text = message_object.text

        if author_id != self.uid and message_text[0] == '!':
            


if __name__=="__main__":
    with open("../login.txt", 'r') as file:
        lines = file.readlines()
        email = lines[0]
        password = lines[1]

    bot = Bot(email, password)
    bot.listen()
