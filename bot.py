from fbchat import log, Client
from fbchat.models import *

from data import *

import random, traceback, time, wikipedia, re

class Bot(Client):

    def __init__(self, email, password):
        Client.__init__(self, email, password)
        self.command_list = {'help':self.command_help}#'coto':self.command_coto,'dance':self.command_dance,'weeb':self.command_weeb,'zmiany':self.command_zmiany}

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):

        self.markAsDelivered(thread_id, message_object.uid)
        log.info("{} from {} of type {}".format(message_object.text, thread_id, thread_type.name))

        try:
            message_text = message_object.text.lower()
        except:
            message_text = message_object.text

        if author_id != self.uid and re.search('^!', message_text):
            message_components = re.findall(r'[\w,]+', message_text)
            command = message_components[0]
            arguments = [i for i in message_components[1:]]
            print("Command: \n"+command+"\nArguments: ")
            print(arguments)
            if command in self.command_list:
                self.command_list[command](arguments)
            else:
                self.command_unrecognized()

    def command_help(self, args):
        if args[0] in self.command_list:
            self.command_list[args[0]](['help'])

    def command_unrecognized(self):
        self.send(Message(text="Nie znam takiej komendy!"), thread_id=thread_id, thread_type=thread_type)

if __name__=="__main__":
    with open("../login.txt", 'r') as file:
        lines = file.readlines()
        email = lines[0]
        password = lines[1]

    bot = Bot(email, password)
    bot.listen()
