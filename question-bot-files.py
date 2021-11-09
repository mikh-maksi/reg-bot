import logging

# Состояние 0 - регистрация. Проверяется через то - полная ли строка: id; все параметры регистрации
# Делаем все действия - с сохранением в файл (регистрация и "В чем помочь")
# telegram_id;question_code;question_value

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters

reg_list = ["","",""]

account = 0
condition = -1

check_strings = ["Your input is correct","Your input is empty","Parameter of command is not digit"]
reg_title = ["ФИО","Роль","Позиция"]
reg_code = ["name","role","position"]
reg_status = [0,0,0]

roles_title = ["Менеджмент","КХМ","Преподватель тех","Преподаватель софт"]
roles_code = ["role_management","role_chm","role_teacher_tech","role_teacher_soft"]

check_strings1 = ["Your input is correct","Your input is empty","Parameter of command is not digit"]
question_title = ["% выаолнения OKR","Удовлетворенность","Желание рекомендовать компанию"]
question_code = ["OKR","sutisfaction","NPS"]
reg_status1 = [0,0,0]

reg_title11 = ["Не понятно"]
reg_code11 = ["notunderstand"]

reg_title12 = ["Предложите"]
reg_code12 = ["propose"]


def check(string_in):
    n=0
    elements = string_in.split(' ')

    if not len(string_in) > 0:
        n=1
    elif not string_in.isdigit():
        n=2
    return n


def reg(update, context):
    string_out = '-->'
    for regs in reg_list:
        string_out += regs+' '
    update.message.reply_text(string_out)


def key_buttons():
    key_lst = []    
    for i in range(len(reg_title)):
        if reg_status[i]==0:
            key_lst.append(InlineKeyboardButton(reg_title[i], callback_data=reg_code[i]))
    kb = [key_lst]
    return kb

def key_buttons1():
    key_lst = []   
    kb = [] 
    for i in range(len(question_title)):
        key_lst = [InlineKeyboardButton(question_title[i], callback_data=question_code[i])]
        kb.append(key_lst)
    return kb


def key_buttons_role():
    key_lst = []   
    kb = [] 
    for i in range(len(roles_title)):
        key_lst = [InlineKeyboardButton(roles_title[i], callback_data=roles_code[i])]
        kb.append(key_lst)
    return kb
    return kb


def need_reg():
    isreg = False
    for reg in reg_status:
        if reg==0:
            return True
    return isreg

def start(update: Update, context: CallbackContext) -> None:
    if need_reg():
        keyboard = key_buttons()
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Выберите один из вариантов:', reply_markup=reply_markup)
    else:
        keyboard = key_buttons1()
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('В чем нужна помощь:', reply_markup=reply_markup)



def button(update: Update, context: CallbackContext) -> None:
    global condition
    query = update.callback_query
    query.answer()
    if query.data == 'role':
        keyboard = key_buttons_role()
        reply_markup = InlineKeyboardMarkup(keyboard)
        chat = update.effective_chat
        query.edit_message_text(text=f"Выберите вашу роль в компании:",reply_markup=reply_markup)

        print("role")
    elif query.data in roles_code:
        for i in range(len(roles_code)):
            if query.data == roles_code[i]:
                query.edit_message_text(text=f"Выбрали: {roles_title[i]}")
                print(condition)
                reg_status[1]=1
    else:
        for i in range(len(reg_code)):
            if query.data == reg_code[i]:
                query.edit_message_text(text=f"Введите {reg_title[i]}")
                condition = i
                print(condition)

def echo(update, context):
    global condition, account
    string_in = update.message.text

    if string_in == '/start':
        string_out = 'Hello! This is own finances bot!'
    elif condition != -1:
        reg_list[condition] = string_in
        reg_status[condition] = 1
        chat = update.effective_chat
        f = open('users_data.csv','a')
        file_out = f"{chat.id};{reg_code[condition]};{string_in};"
        f.write(file_out+'\n')
        f.close()
        print(chat.id,reg_code[condition],string_in)
        string_out = "Записано"
        condition = -1
    else:
        string_out = string_in

    if need_reg():
        keyboard = key_buttons()
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(string_out,reply_markup=reply_markup)
    else:
        update.message.reply_text('Регистрация заверена')

        keyboard = key_buttons1()
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('В чем нужна помощь:', reply_markup=reply_markup)

        # update.message.reply_text(string_out,reply_markup=reply_markup)

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Use /start to test this bot.")


def main() -> None:
    updater = Updater("2129076685:AAG9NDUjjHlhXW7HD0gJ7cAId1z3nacInks")

    updater.dispatcher.add_handler(CommandHandler('reg', reg))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    updater.dispatcher.add_handler(MessageHandler(Filters.all, echo))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
