import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import pickle
from os.path import exists
import time

telegram_token = '<>' # PUT HERE THE TELEGRAM TOKEN
updater = Updater(token=telegram_token, use_context=True, user_sig_handler=True)
dispatcher = updater.dispatcher

admin_group = '<>' # PUT HERE THE TELEGRAM ID OF THE ADMIN GROUP WITHOUTH THE - SIGN
allowed_groups = ['<>',   # OTTOxOTTO - GROUP ID
                  '<>',   # Help - GROUP IT
                  '<>',   # Pettegolezzi scientifici - GROUP ID
                  '<>',   # Filosofia - GROUP ID
                  '<>',   # Admin - GROUP ID
                  '<>']   # Test - GROUP ID

scientists = {'matematica': [], 'fisica': [], 'chimica': [], 'informatica': [], 'biologia': [], 'geologia': [], 'filosofia': []}

dbfile = '<somepath>/scientists.pickle' # PUT HERE THE PATH TO THE FILE TO STORE THE SCIENTISTS DICTIONARY

def load_scientists():
    global scientists
    if not exists(dbfile)
        return
    with open(dbfile, 'rb') as f:
        scientists = pickle.load(f)
    return

def save_scientists():
    with open(dbfile, 'wb') as f:
        pickle.dump(scientists, f, protocol=pickle.HIGHEST_PROTOCOL)
    return

def add_scientist(update, context):
    chat_id = update['message']['chat']['id']
    if chat_id != int('-'+admin_group) and chat_id != int('-100'+admin_group):
        return
    rawdata = update['message']['text'].split(' ')[1:]
    if len(rawdata) != 2:
        context.bot.sendMessage(chat_id=chat_id, text='Invalid Syntax.\nThe correct syntax is: /addscientist <topic> <username>')
        return
    topic, username = rawdata
    if not topic in scientists.keys():
        topics = ''
        for topic in scientists.keys():
            topics+='*'+topic+'*\n'
        context.bot.sendMessage(chat_id=chat_id, text='Invalid Topic.\nCurrently the supported topics are\n'+topics, parse_mode='markdown')
        return
    if username[0] != '@':
        context.bot.sendMessage(chat_id=chat_id, text='Username should start with *@*', parse_mode='markdown')
        return
    if username in scientists[topic]:
        context.bot.sendMessage(chat_id=chat_id, text='Username *'+username+'* is already in *'+topic+'*', parse_mode='markdown')
        return
    scientists[topic].append(username)
    save_scientists()
    context.bot.sendMessage(chat_id=chat_id, text='*'+username+'* added in *'+topic+'*', parse_mode='markdown')

def del_scientist(update, context):
    chat_id = update['message']['chat']['id']
    if chat_id != int('-'+admin_group) and chat_id != int('-100'+admin_group):
        return
    rawdata = update['message']['text'].split(' ')[1:]
    if len(rawdata) != 2:
        context.bot.sendMessage(chat_id=chat_id, text='Invalid Syntax.\nThe correct syntax is: /delscientist <topic> <username>')
        return
    topic, username = rawdata
    if not topic in scientists.keys():
        topics = ''
        for topic in scientists.keys():
            topics+='*'+topic+'*\n'
        context.bot.sendMessage(chat_id=chat_id, text='Invalid Topic.\nCurrently the supported topics are\n'+topics, parse_mode='markdown')
        return
    if not username in scientists[topic]:
        context.bot.sendMessage(chat_id=chat_id, text='Username *'+username+'* is not present in the topic *'+topic+'*', parse_mode='markdown')
        return
    scientists[topic].remove(username)
    save_scientists()
    context.bot.sendMessage(chat_id=chat_id, text='*'+username+'* deleted from *'+topic+'*', parse_mode='markdown')

def list_scientists(update, context):
    chat_id = update['message']['chat']['id']
    if chat_id != int('-'+admin_group) and chat_id != int('-100'+admin_group):
        return
    topiclist=''
    for topic in scientists:
        if len(scientists[topic]) == 0:
            topiclist+='*'+topic+'* has no scientists\n'
            continue
        topiclist += '*'+topic+'* has the scientists\n'
        for scientist in scientists[topic]:
            topiclist += '\t'+scientist+'\n'
    context.bot.sendMessage(chat_id=chat_id, text=topiclist.replace("_", "\_"), parse_mode='markdown')

def poke_scientists(update, context):
    chat_id = update['message']['chat']['id']
    allowed = False
    for group in allowed_groups:
        if chat_id == int('-'+group) or chat_id == int('-100'+group):
            allowed = True
            break
    if not allowed:
        return
   
    scientists_to_call = []
    for word in update['message']['text'].split():
        if word[0]=='#':
            topic = word[1:]
            if topic in scientists.keys():
                for scientist in scientists[topic]:
                    if scientist in scientists_to_call:
                        continue
                    scientists_to_call.append(scientist)
    if len(scientists_to_call) == 0:
        return

    call = ''
    for scientist in scientists_to_call:
        call +=scientist+' '
    context.bot.sendMessage(chat_id=chat_id, text=''+call)    

def poke_scientists_photo(update, context):
    chat_id = update['message']['chat']['id']
    allowed = False
    for group in allowed_groups:
        if chat_id == int('-'+group) or chat_id == int('-100'+group):
            allowed = True
            break
    if not allowed:
        return

    if update['message']['caption'] == None:
        return

    scientists_to_call = []
    for word in update['message']['caption'].split():
        if word[0]=='#':
            topic = word[1:]
            if topic in scientists.keys():
                for scientist in scientists[topic]:
                    if scientist in scientists_to_call:
                        continue
                    scientists_to_call.append(scientist)
    if len(scientists_to_call) == 0:
        return

    call = ''
    for scientist in scientists_to_call:
        call +=scientist+' '
    context.bot.sendMessage(chat_id=chat_id, text=''+call)    

load_scientists()
for topic in scientists:
    dispatcher.add_handler(MessageHandler(Filters.regex("#"+topic), poke_scientists)) 
dispatcher.add_handler(MessageHandler(Filters.photo, poke_scientists_photo))
dispatcher.add_handler(MessageHandler(Filters.document, poke_scientists_photo))
dispatcher.add_handler(CommandHandler("addscientist", add_scientist)) 
dispatcher.add_handler(CommandHandler("delscientist", del_scientist)) 
dispatcher.add_handler(CommandHandler("listscientists", list_scientists)) 
updater.start_polling()

