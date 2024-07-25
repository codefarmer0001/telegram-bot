from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update
from bot.Help import Help
from bot.Check3 import Check3
from bot.Echo import Echo
from dao.Bills import Bills
from dao.Grant import Grant
from dao.Setting import Setting
from dao.User import User
from business.OkexPrice import OkexPrice
import config
from bot.NewMember import NewMember
from flask import Flask, request
from controller.auth_controller import auth_blue
from controller.bills_controller import bills_blue
from controller.grant_controller import grant_blue

app = Flask(__name__)

app.register_blueprint(auth_blue, url_prefix='/auth')
app.register_blueprint(bills_blue, url_prefix='/bills')
app.register_blueprint(grant_blue, url_prefix='/grant')

def start(update, context):
    # print(update)
    update.message.reply_text('Hi!')

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

@app.route('/async-message', methods=['POST'])
def webhook():
    json_data = request.get_json()
    print(json_data)

    if 'my_chat_member' in json_data:
        newMember_instance = NewMember()
        my_chat_member = json_data['my_chat_member']
        from_user = my_chat_member['from']
        from_id = from_user['id']
        from_user_name = f'@{from_user["username"]}'
        # print(from_id)
        new_chat_member = my_chat_member['new_chat_member']
        user = new_chat_member['user']
        id = user['id']
        # print(id)
        chat = my_chat_member['chat']
        chat_id = chat['id']

        status = new_chat_member['status']
        # print(chat_id)
        if str(id) in config.TOKEN and 'member' == status:
            newMember_instance.new_group_grant(updater.bot, chat_id, from_id, from_user_name)


    update = Update.de_json(json_data, updater.bot)
    # print(update)
    dispatcher.process_update(update)
    return ''

if __name__ == '__main__':

    bills = Bills()
    grant = Grant()
    setting = Setting()
    user = User()

    updater = Updater(config.TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    help_instance = Help()
    check3_instance = Check3()
    echo_instance = Echo()
    okexPrice_instance = OkexPrice()
    newMember_instance = NewMember()
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_instance.help))
    dispatcher.add_handler(CommandHandler("check3", check3_instance.check3))
    dispatcher.add_handler(CommandHandler("w0", okexPrice_instance.weixinPrice))
    dispatcher.add_handler(CommandHandler("z0", okexPrice_instance.aliPrice))

    dispatcher.add_handler(MessageHandler(Filters.text, echo_instance.echo))
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, newMember_instance.handler), group=1)
    # dispatcher.add_handler(MessageHandler(Filters.group, start), group=1)

    dispatcher.add_error_handler(error)

    updater.bot.deleteWebhook()
    # Set up webhook
    updater.bot.setWebhook(url=config.WEBHOOK_URL)

    # Start the Flask web server
    app.run(port=config.PORT, debug=True)

    updater.start_polling()
    updater.idle()