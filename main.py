from fbchat import log, Client
from fbchat.models import *

from data import *

import random, traceback, time, wikipedia, re, time, atexit

class Bot(Client):


    # ACTIVE THREADS ARE STORED AS THREAD_ID:LAST_BOT_CALL IN THE DICT


    def __init__(self, email, password):
        Client.__init__(self, email, password)  #call the Client class default init
        self.active_threads = {}                        #create the active threads dict
        with open('active_threads.txt', 'r') as file:   #open the file containing threads
            lines = file.readlines()                    #read it
            for e, v in enumerate(lines):               #enumerate through every line
                if e%2==0:                              #if the line is even
                    self.active_threads[v]=lines[e+1]   #add it as thisline:nextline key-value pair
        print(self.active_threads)
        self.set_status()  #this method goes through every thread and updates the bot nickname
        self.command_list = {'help':self.command_help}#'coto':self.command_coto,'dance':self.command_dance,'weeb':self.command_weeb,'zmiany':self.command_zmiany}

#############################################################################

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):

        if thread_type == ThreadType.GROUP:                 #update this thread's last bot call time
            self.active_threads[thread_id] = time.time()
            print("updated the active_threads")

        message_info = {'author_id':author_id,'message_object':message_object,'thread_id':thread_id,'thread_type':thread_type} #the dict containing all the message info; It's later passed to the command handling methods

        self.markAsDelivered(thread_id, message_object.uid)                                         #mark the message as delivered
        log.info("{} from {} of type {}".format(message_object.text, thread_id, thread_type.name))  #log into the console what's the message, from which thread it's from, and what's it's thread type

        try:
            message_text = message_object.text.lower()
        except:
            message_text = message_object.text

        if author_id != self.uid and re.search('^!', message_text):  #if the message begins with an '!'
            message_components = re.findall(r'[\w,]+', message_text) #split up the message
            command = message_components[0]                          #first part of the message is the command
            if command == 'calc':
                arguments = re.findall(r'[0-9]+|[\*\/\+\-]+')
            else:
                arguments = [i for i in message_components[1:]]          #the rest are the arguments

            if command in self.command_list:                         #if such a command exists
                self.command_list[command](arguments, message_info)  #call it with the arguments and the message info
            else:                                                    #
                self.command_unrecognized(message_info)                          #if not, call command_unrecognized()

    # Command syntax rules
    #
    # 1. Every command must have exactly two arguments except of self:
    #
    #       def command_example(self, args, info):
    # 
    # When calling the command in the parsing phase, the parser
    # calls the command with a list of commands arguments as the first argument,
    # and a dict of message info such as thread_id as the second argument.
    #
    # The commands arguments shall then be parsed inside of the command method.
    #
    #
    #
    # 2. Every command must have it's own help handling in that form:
    #       
    #        def command_example(self, args, info)
    #           if args[0] == 'help':
    #               <send message with help>
    #
    #

    def command_help(self, args, info):
        if args[0] in self.command_list: #if the first argument of !help is a command name
            self.command_list[args[0]](['help']) #run that command with help as a first argument

    def command_unrecognized(self, info):
        self.send(Message(text="Nie znam takiej komendy!"), thread_id=info['thread_id'], thread_type=info['thread_type'])

    ########## active threads handling ##########

    def set_status(self, offline=''):       #this method goeas through every thread and updates the bot nickname
        for k, v in self.active_threads.items():
            if time.time() - v > 604800:
                del self.active_threads[k]  #if the bot was called on this thread more than a week ago, delete the thread from the active threads
            else:
                self.changeNickname("Bot Apolinary"+offline, self.uid, k, ThreadType.GROUP)
        print("set_status executed!")

    def exit(self):
        self.set_status(' (offline)')
        with open('active_threads.txt', 'w') as file:
            for k, v in self.active_threads.items():
                file.write(k+'\n'+v+'\n')
        self.logout()
        print("logout successful!")


#######################################################################################


if __name__=="__main__":
    with open("../login.txt", 'r') as file: #change this part as you desire
        lines = file.readlines()            #
        email = lines[0]                    #
        password = lines[1]                 #
        
        bot = Bot(email, password)
        bot.listen()
