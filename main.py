import random
import re
import traceback
import wikipedia

from fbchat import log, Client

from data import *


class Bot(Client):

    def __init__(self, email, password):
        Client.__init__(self, email, password)  # call the Client class default init
        self.command_list = {
            'help': self.command_help,
            'wiki': self.command_wiki,
            'dance': self.command_dance,
            'weeb': self.command_weeb,
            'change': self.command_change,
            'zadyma': self.command_zadymiarnia,
            'calc': self.command_calc
        }  # 'coto':self.command_coto,'dance':self.command_dance,'weeb':self.command_weeb,'zmiany':self.command_zmiany}

        self.help_text = {
            'wiki': "Wiki function searches wikipedia for the definition of a given keyword",

            'dance': "Dance command sends a gif of dancing rockalone2k, you can specify the type of the dance by using 'def' or 'alter' argument after the command",

            'weeb': "Weeb command displays a random gif with an anime girl, you can specify level of your 'weebness' by using 'nsfw' keyword after !weeb ",

            'zmiany': "Zmiany command changes the overall look of chat",

            'change': "Change command changes the overall look of chat ",

            'zadyma': "A list of zadymiarnia commands: \n1. Head\n2. Szef\n3. Rafon\n4. Blowjob",

            'calc': "A simple calculator, just enter an operation of your desire :)"
        }

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):

        message_info = {'author_id': author_id, 'message_object': message_object, 'thread_id': thread_id,
                        'thread_type': thread_type}  # the dict containing all the message info; It's later passed to the command handling methods

        self.markAsDelivered(thread_id, message_object.uid)  # mark the message as delivered
        log.info("{} from {} of type {}".format(message_object.text, thread_id,
                                                thread_type.name))  # log into the console what's the message, from which thread it's from, and what's it's thread type

        try:
            message_text = message_object.text.lower()
        except:
            message_text = message_object.text

        if author_id != self.uid and re.search('^!', message_text):  # if the message begins with an '!'
            message_components = re.findall(r'[\w,]+', message_text)  # split up the message
            command = message_components[0]  # first part of the message is the command
            if command == 'calc':
                arguments = re.findall(r'[0-9]+|[\*\/\+\-]+', message_text)
            else:
                arguments = [i for i in message_components[1:]]  # the rest are the arguments
            if arguments == []:
                arguments.append(True)

            if command in self.command_list:
                # if such a command exists
                self.command_list[command](arguments, message_info)  # call it with the arguments and the message info
            else:  #
                self.command_unrecognized(message_info)  # if not, call command_unrecognized()

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
        if args[0] in self.command_list:  # if the first argument of !help is a command name
            self.command_list[args[0]](['help'],info)  # run that command with help as a first argument

    def command_wiki(self, args, info):

            if args[0] == "help":
                self.send(Message(text=self.help_text['wiki']), thread_id=info['thread_id'],
                          thread_type=info['thread_type'])
            else:
                search_text = ' '.join(args)
                wikipedia.set_lang('pl')
                """
                try:
                    try:
                        wiki_result = wikipedia.summary(search_text)  # wikipedia definition
                    self.send(Message(text="Definicja {} :\n{}".format(search_text, wiki_result)),
                              thread_id=info['thread_id'],
                              thread_type=info['thread_type'])
                    except:
                        wiki_list_search = wikipedia.search(search_text)  # wikipedia list output
                        wiki_list_result = "\n".join(wiki_list_search)
                    self.send(Message(
                        text="Nie mogłem znaleźć pasującej definicji {} :/ podobne wyszukiwania:\n{}".format(
                            search_text, wiki_list_result)), thread_id=info['thread_id'], thread_type=info['thread_type'])
                except Exception:
                        traceback.print_exc()
                """
                try:
                    try:
                        wiki_result = wikipedia.summary(search_text)
                        self.send(Message(text="Definicja {}:\n{}".format(search_text,wiki_result)),thread_id=info['thread_id'], thread_type=info['thread_type'])
                    except:
                        wiki_list_search = wikipedia.search(search_text)
                        wiki_list_result = "\n".join(wiki_list_search)
                        self.send(Message(text="Nie mogłem znaleźć pasującej definicji {} :/ podobne wyszukiwania:\n{}".format(search_text, wiki_list_result)),thread_id=info['thread_id'], thread_type=info['thread_type'])
                except Exception:
                    traceback.print_exc()




    def command_dance(self, args, info):
        if args[0] == "help":
            self.send(Message(text=self.help_text['dance']), thread_id=info['thread_id'],
                      thread_type=info['thread_type'])
        else:
            try:
                if args[0] == 'def':
                    self.sendRemoteImage('https://i.imgur.com/eTSkNmU.gif', thread_id=info['thread_id'],
                                         thread_type=info['thread_type'])
                elif args[0] == 'alter':
                    self.sendRemoteImage('https://i.imgur.com/Pcg9D5y.gif', thread_id=info['thread_id'],
                                         thread_type=info['thread_type'])
                else:
                    self.send(Message(text="This type of dance wasnt invented yet"), thread_id=info['thread_id'],
                              thread_type=info['thread_type'])
            except:
                traceback.print_exc()
                pass


    def command_weeb(self, args, info):
        if args[0] == "help":
            self.send(Message(
                text=self.help_text['weeb']),
                thread_id=info['thread_id'],
                thread_type=info['thread_type'])
        else:
            try:
                if args[0] == 'nsfw':
                    random_nsfw = random.choice(anime_nsfw)
                    self.sendRemoteImage(random_nsfw, thread_id=info['thread_id'],
                                         thread_type=info['thread_type'])
                else:
                    random_gif = random.choice(anime_gifs)
                    self.sendRemoteImage(random_gif, thread_id=info['thread_id'],
                                         thread_type=info['thread_type'])
            except:
                traceback.print_exc()
                pass


    def command_change(self, args, info):
        if args[0] == "help":
            self.send(Message(
                text=self.help_text['change']),
                thread_id=info['thread_id'],
                thread_type=info['thread_type'])
        else:
            try:
                random_color = random.choice(colours)
                random_emoji = random.choice(emojis)
                self.reactToMessage(info['message_object'].uid, MessageReaction.LOVE)
                self.send(Message(text='Great! lets make some changes! 😍😍'), thread_id=info['thread_id'],
                          thread_type=info['thread_type'])
                self.changeThreadColor(random_color, thread_id=info['thread_id'])
                self.changeThreadEmoji(random_emoji, thread_id=info['thread_id'])
            except Exception:
                traceback.print_exc()
                pass


    def command_zadymiarnia(self, args, info):
        if args[0] == "help":
            self.send(Message(
                text=self.help_text['change']),
                thread_id=info['thread_id'],
                thread_type=info['thread_type'])
        if args[0] == 'head':
            self.sendRemoteImage(zadymiarnia['head'], thread_id=info['thread_id'], thread_type=info['thread_type'])
        elif args[0] == 'szef':
            self.sendRemoteImage(zadymiarnia['szef'], thread_id=info['thread_id'], thread_type=info['thread_type'])

        elif args[0] == 'rafon':
            self.sendRemoteImage(zadymiarnia['rafon'], thread_id=info['thread_id'], thread_type=info['thread_type'] )
        elif args[0] == 'blowjob':
            self.sendRemoteImage(zadymiarnia['blow'], thread_id=info['thread_id'], thread_type=info['thread_type'])
        else:
            self.sendRemoteImage(random.choice(zadymiarnia), thread_id=info['thread_id'],
                                 thread_type=info['thread_type'])


    def command_calc(self, args, info):
        if args[0] == "help":
            self.send(Message(
                text=self.help_text['change']),
                thread_id=info['thread_id'],
                thread_type=info['thread_type'])
        else:
            to_calc = ''.join(args)
            print("To calc is " + to_calc)
            if "**" in to_calc:
                check = to_calc.split("**")[1]
                if eval(check) >= 1000:
                    self.send(Message(text='These numbers are too big! :O'), thread_id=info['thread_id'],
                              thread_type=info['thread_type'])
                else:
                    self.send(Message(text="{} is obviously {}".format(to_calc, (eval(to_calc)))),
                              thread_id=info['thread_id'],
                              thread_type=info['thread_type'])
            else:
                self.send(Message(text="{} is obviously {}".format(to_calc, (eval(to_calc)))),
                          thread_id=info['thread_id'],
                          thread_type=info['thread_type'])


    def command_unrecognized(self, info):
        self.send(Message(text="Nie znam takiej komendy!"), thread_id=info['thread_id'],
                  thread_type=info['thread_type'])


if __name__ == "__main__":
    with open("login.txt", 'r') as file:  # change this part as you desire
        lines = file.readlines()  #
        email = lines[0]  #
        password = lines[1]  #

bot = Bot(email, password)
bot.listen()
