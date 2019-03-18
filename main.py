from fbchat import log, Client
from fbchat.models import *
from data import colours, emojis, anime_gifs
import random
import traceback
import time
import wikipedia

thread = ""
type = ""


class EchoBot(Client):

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        random_color = random.choice(colours)
        random_emoji = random.choice(emojis)
        random_girl = random.choice(anime_gifs)

        self.markAsDelivered(thread_id, message_object.uid)


        log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))
        try:
            messagetext = message_object.text.lower()
        except:
            messagetext = message_object.text

        def zmiany(color, emoji):
            client.reactToMessage(message_object.uid, MessageReaction.LOVE)
            client.send(Message(text='Great! lets make some changes! 😍😍'), thread_id=thread_id,
                        thread_type=thread_type)
            client.changeThreadColor(color, thread_id=thread_id)
            client.changeThreadEmoji(emoji, thread_id=thread_id)

        def simple_calc():
            try:
                client.send(
                    Message(text="👨🏻‍🏫 " + str(messagetext[5:]) + " is obviously: " + str(
                        eval(messagetext[5:])) + " :D"),
                    thread_id=thread_id,
                    thread_type=thread_type)
            except:
                client.send(Message(text='An error has occured! :('), thread_id=thread_id,
                            thread_type=thread_type)

        always_true = True

        # if thread_type != ThreadType.GROUP:
        if always_true and author_id != client.uid and "!" in messagetext:
            self.markAsRead(thread_id)
            try:
                if messagetext == None or "":
                    pass
                elif "!change" in messagetext:
                    zmiany(random_color, random_emoji)
                elif "!tu sie puknij" in messagetext:
                    client.sendLocalImage('rocky.gif', thread_id=thread_id, thread_type=thread_type)
                elif "!dance def" in messagetext:
                    client.sendRemoteImage('https://i.imgur.com/eTSkNmU.gif',
                                           thread_id=thread_id, thread_type=thread_type)
                elif "!dance alter" in messagetext:
                    client.sendRemoteImage('https://i.imgur.com/Pcg9D5y.gif', thread_id=thread_id,
                                           thread_type=thread_type)
                elif "!weeb" in messagetext:
                    try:
                        client.sendRemoteImage(random_girl, thread_id=thread_id,
                                               thread_type=thread_type)
                    except Exception:
                        traceback.print_exc()
                        client.send(Message(text='An error has occured! :('), thread_id=thread_id,
                                    thread_type=thread_type)

                elif "!calc" in messagetext:
                    if "**" in messagetext:
                        do_obliczen = messagetext[5:]
                        check = do_obliczen.split("**")[1]
                        if eval(check) >= 1000:
                            client.send(Message(text='These numbers are too big! :O'), thread_id=thread_id,
                                        thread_type=thread_type)
                        else:
                            simple_calc()
                    else:
                        simple_calc()

                elif "!help" in messagetext:
                    client.send(Message(
                        text='''
                        List of commands:
1.calc ( simple calculator )
2.change ( changes te look of the chat )
3.tu sie puknij ( offensive gif of RockAlone2k )
4.dance <def or alter> ( dancing gif of RockAlone )
6.weeb ( something nice for all of our weebs out there ;) )
7.rafon
8.head  ( i cannot find any better photo of Fala64 )
9.coto  ( search for wikipedia results )
                        \n*To activate function use "!" key before function name!*
                        \n\nThanks for using bot roman! 😊

                            '''),thread_id=thread_id, thread_type=thread_type)

                elif("!szef" or "!krolewicz" or "!szefuncio") in messagetext:
                    client.sendLocalImage('gabriel.jpg', thread_id=thread_id, thread_type=thread_type)

                elif "!head" in messagetext:
                    client.sendLocalImage('head.jpg',thread_id=thread_id,thread_type=thread_type)

                elif "!rafon" in messagetext:
                    client.sendRemoteImage('https://i.imgur.com/PvqkiyL.gif', thread_id=thread_id,
                                           thread_type=thread_type)

                elif "!coto"  in messagetext:
                    try:
                        searching_for = messagetext[5:]
                        wikipedia.set_lang("pl")
                        try:
                            wiki = wikipedia.summary(searching_for)
                            client.send(Message(text='📖Według wikipedii📖{} to:\n{}...'.format(searching_for,wiki[:400])), thread_id=thread_id,thread_type=thread_type)
                        except:
                            try:
                                wikipedia.set_lang("en")
                                wiki = wikipedia.summary(searching_for)
                            except:
                                wikipedia.set_lang("pl")
                                list_wiki = wikipedia.search(searching_for)
                                wikipedia.set_lang("en")
                                list_wiki_en = wikipedia.search(searching_for)
                                final_result = []

                                if len(list_wiki) != (0 or []):
                                    final_result += list_wiki

                                if len(list_wiki_en) != (0 or []):
                                    final_result += list_wiki_en

                                client.send(Message(text='Nie mogłem znaleźć definicji dla {} :/\nmoże chodziło ci o któreś z poniższych?\n{}'.format(searching_for, final_result)),thread_id=thread_id,thread_type=thread_type)
                    except:
                        client.send(Message(text='An error has occured! :('), thread_id=thread_id,
                                    thread_type=thread_type)


                #elif "!spadaj" in messagetext:
                    #client.send(Message(text='Bye :('), thread_id=thread_id,thread_type=thread_type)
                    #time.sleep(1)
                    #exit()


                #https://i.imgur.com/PvqkiyL.gif

                else:
                    pass
            except Exception:
                 traceback.print_exc()

        # head
        # https://i.makeagif.com/media/5-19-2015/Qtxbgj.gif
        # https://i.imgur.com/sjukLYg.gif
        # https://thumbs.gfycat.com/CleverDiligentAardvark-size_restricted.gif

        """
        # and author_id != client.uid
        if message_object.text == "zmiany" and thread_type != ThreadType.GROUP:
            odpowiedz(random_color, random_emoji)
        """


client = EchoBot("#", "#")
client.listen()
