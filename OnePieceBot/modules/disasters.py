import html
import json
import os
from typing import Optional

from OnePieceBot import (DEV_USERS, OWNER_ID, WORLD_GOVT, SUPPORT_CHAT, ADMIRALS,
                          WARLORDS, REVOLUTIONARIES, dispatcher)
from OnePieceBot.modules.helper_funcs.chat_status import (dev_plus, sudo_plus,
                                                           whitelist_plus)
from OnePieceBot.modules.helper_funcs.extraction import extract_user
from OnePieceBot.modules.log_channel import gloggable
from telegram import ParseMode, TelegramError, Update
from telegram.ext import CallbackContext, CommandHandler, run_async
from telegram.utils.helpers import mention_html

ELEVATED_USERS_FILE = os.path.join(os.getcwd(),
                                   'OnePieceBot/elevated_users.json')


def check_user_id(user_id: int, context: CallbackContext) -> Optional[str]:
    bot = context.bot
    if not user_id:
        reply = "That...is a chat! baka ka omae?"

    elif user_id == bot.id:
        reply = "This does not work that way."

    else:
        reply = None
    return reply


# This can serve as a deeplink example.
#powers =
# """ Text here """

# do not async, not a handler
#def send_powers(update):
#    update.effective_message.reply_text(
#        powers, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

### Deep link example ends


@run_async
@dev_plus
@gloggable
def addsudo(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in WORLD_GOVT:
        message.reply_text("This member is already in World Government")
        return ""

    if user_id in ADMIRALS:
        rt += "Requested Emperors to promote a Admiral to a member of World Government."
        data['supports'].remove(user_id)
        ADMIRALS.remove(user_id)

    if user_id in REVOLUTIONARIES:
        rt += "Requested Emperors to promote a Revolutionary to a member of World Government."
        data['whitelists'].remove(user_id)
        REVOLUTIONARIES.remove(user_id)

    data['sudos'].append(user_id)
    WORLD_GOVT.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + "\nSuccessfully set Disaster level of {} to a member in World Government!".format(
            user_member.first_name))

    log_message = (
        f"#SUDO\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@sudo_plus
@gloggable
def addsupport(
    update: Update,
    context: CallbackContext,
) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in WORLD_GOVT:
        rt += "Requested  Emperors to deomote this person from a member of World Government to Admiral"
        data['sudos'].remove(user_id)
        WORLD_GOVT.remove(user_id)

    if user_id in ADMIRALS:
        message.reply_text("This user is already a Admiral.")
        return ""

    if user_id in REVOLUTIONARIES:
        rt += "Requested Emperors to promote this Revolutionary to Admiral"
        data['whitelists'].remove(user_id)
        REVOLUTIONARIES.remove(user_id)

    data['supports'].append(user_id)
    ADMIRALS.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + f"\n{user_member.first_name} was added as a Admiral!")

    log_message = (
        f"#SUPPORT\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@sudo_plus
@gloggable
def addwhitelist(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in WORLD_GOVT:
        rt += "This is a member  World Government, Demoting to Revolutionary."
        data['sudos'].remove(user_id)
        WORLD_GOVT.remove(user_id)

    if user_id in ADMIRALS:
        rt += "This user is already a Admiral, Demoting to Revolutionary."
        data['supports'].remove(user_id)
        ADMIRALS.remove(user_id)

    if user_id in REVOLUTIONARIES:
        message.reply_text("This user is already a Revolutionary.")
        return ""

    data['whitelists'].append(user_id)
    REVOLUTIONARIES.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt +
        f"\nSuccessfully promoted {user_member.first_name} to a Revolutionary!")

    log_message = (
        f"#WHITELIST\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))} \n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@sudo_plus
@gloggable
def addwarlord(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in WORLD_GOVT:
        rt += "This is a member  World Government, Demoting to Warlord."
        data['sudos'].remove(user_id)
        WORLD_GOVT.remove(user_id)

    if user_id in ADMIRALS:
        rt += "This user is already a Admiral, Demoting to Warlord."
        data['supports'].remove(user_id)
        ADMIRALS.remove(user_id)

    if user_id in REVOLUTIONARIES:
        rt += "This user is already a Revolutionary power, Demoting to Warlord."
        data['whitelists'].remove(user_id)
        REVOLUTIONARIES.remove(user_id)

    if user_id in WARLORDS:
        message.reply_text("This user is already a Warlord.")
        return ""

    data['WARLORDS'].append(user_id)
    WARLORDS.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt +
        f"\nSuccessfully promoted {user_member.first_name} to a Warlord!"
    )

    log_message = (
        f"#WARLORD\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))} \n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@dev_plus
@gloggable
def removesudo(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in WORLD_GOVT:
        message.reply_text("Requested Emperors to demote this user to Civilian")
        WORLD_GOVT.remove(user_id)
        data['sudos'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNSUDO\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != 'private':
            log_message = "<b>{}:</b>\n".format(html.escape(
                chat.title)) + log_message

        return log_message

    else:
        message.reply_text("This user is not a World Government member!")
        return ""


@run_async
@sudo_plus
@gloggable
def removesupport(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in ADMIRALS:
        message.reply_text("Requested Emperors to demote this user to Civilian")
        ADMIRALS.remove(user_id)
        data['supports'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNSUPPORT\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != 'private':
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message

    else:
        message.reply_text("This user is not a Admiral level Power!")
        return ""


@run_async
@sudo_plus
@gloggable
def removewhitelist(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in REVOLUTIONARIES:
        message.reply_text("Demoting to normal user")
        REVOLUTIONARIES.remove(user_id)
        data['whitelists'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNWHITELIST\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != 'private':
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message
    else:
        message.reply_text("This user is not a Revolutionary Power!")
        return ""


@run_async
@sudo_plus
@gloggable
def removewarlord(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in WARLORDS:
        message.reply_text("Demoting to normal user")
        WARLORDS.remove(user_id)
        data['WARLORDS'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNWARLORD\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != 'private':
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message
    else:
        message.reply_text("This user is not a Warlord!")
        return ""


@run_async
@whitelist_plus
def whitelistlist(update: Update, context: CallbackContext):
    reply = "<b>Known Revolutionary powers :</b>\n"
    bot = context.bot
    for each_user in REVOLUTIONARIES:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)

            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
@whitelist_plus
def warlordlist(update: Update, context: CallbackContext):
    reply = "<b>Known Warlords:</b>\n"
    bot = context.bot
    for each_user in WARLORDS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
@whitelist_plus
def supportlist(update: Update, context: CallbackContext):
    bot = context.bot
    reply = "<b>Known Adirals:</b>\n"
    for each_user in ADMIRALS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
@whitelist_plus
def sudolist(update: Update, context: CallbackContext):
    bot = context.bot
    true_sudo = list(set(WORLD_GOVT) - set(DEV_USERS))
    reply = "<b>Known World Government members:</b>\n"
    for each_user in true_sudo:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
@whitelist_plus
def devlist(update: Update, context: CallbackContext):
    bot = context.bot
    true_dev = list(set(DEV_USERS) - {OWNER_ID})
    reply = "<b>Hero Association Members ⚡️:</b>\n"
    for each_user in true_dev:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


__help__ = f"""
*⚠️ Notice:*
Commands listed here only work for users with special access are mainly used for troubleshooting, debugging purposes.
Group admins/group owners do not need these commands. 

 ╔ *List all special users:*
 ╠ `/worldgovt`*:* Lists all World government Powers
 ╠ `/admirals`*:* Lists all Admirals powers
 ╠ `/warlords`*:* Lists all Warlords powers
 ╠ `/revolutionaries`*:* Lists all Revolutionary powers
 ╚ `/emperors`*:* Lists all Hero Association members

 ╔ *Ping:*
 ╠ `/ping`*:* gets ping time of bot to telegram server
 ╚ `/pingall`*:* gets all listed ping times

 ╔ *Broadcast: (Bot owner only)*
 ╠  *Note:* This supports basic markdown
 ╠ `/broadcastall`*:* Broadcasts everywhere
 ╠ `/broadcastusers`*:* Broadcasts too all users
 ╚ `/broadcastgroups`*:* Broadcasts too all groups

 ╔ *Groups Info:*
 ╠ `/groups`*:* List the groups with Name, ID, members count as a txt
 ╚ `/getchats`*:* Gets a list of group names the user has been seen in. Bot owner only

 ╔ *Blacklist:* 
 ╠ `/ignore`*:* Blacklists a user from 
 ╠  using the bot entirely
 ╚ `/notice`*:* Whitelists the user to allow bot usage

 ╔ *Speedtest:*
 ╚ `/speedtest`*:* Runs a speedtest and gives you 2 options to choose from, text or image output

 ╔ *Global Bans:*
 ╠ `/gban user reason`*:* Globally bans a user
 ╚ `/ungban user reason`*:* Unbans the user from the global bans list

 ╔ *Module loading:*
 ╠ `/listmodules`*:* Lists names of all modules
 ╠ `/load modulename`*:* Loads the said module to 
 ╠   memory without restarting.
 ╠ `/unload modulename`*:* Loads the said module from
 ╚   memory without restarting.memory without restarting the bot 

 ╔ *Remote commands:*
 ╠ `/rban user group`*:* Remote ban
 ╠ `/runban user group`*:* Remote un-ban
 ╠ `/rpunch user group`*:* Remote punch
 ╠ `/rmute user group`*:* Remote mute
 ╠ `/runmute user group`*:* Remote un-mute
 ╚ `/ginfo username/link/ID`*:* Pulls info panel for entire group

 ╔ *Windows self hosted only:*
 ╠ `/reboot`*:* Restarts the bots service
 ╚ `/gitpull`*:* Pulls the repo and then restarts the bots service

 ╔ *Chatbot:* 
 ╚ `/listaichats`*:* Lists the chats the chatmode is enabled in
 
 ╔ *Debugging and Shell:* 
 ╠ `/debug <on/off>`*:* Logs commands to updates.txt
 ╠ `/logs`*:* Run this in support group to get logs in pm
 ╠ `/eval`*:* Self explanatory
 ╠ `/sh`*:* Self explanator
 ╚ `/py`*:* Self explanatory

Visit @{SUPPORT_CHAT} for more information.
"""

SUDO_HANDLER = CommandHandler(("addsudo", "addworldgovt"), addsudo)
SUPPORT_HANDLER = CommandHandler(("addsupport", "addadmiral"), addsupport)
WARLORD_HANDLER = CommandHandler(("addwarlord"), addwarlord)
WHITELIST_HANDLER = CommandHandler(("addwhitelist", "addrev"), addwhitelist)
UNSUDO_HANDLER = CommandHandler(("removesudo", "removeworldgovt"), removesudo)
UNSUPPORT_HANDLER = CommandHandler(("removesupport", "removeadmiral"),
                                   removesupport)
UNWARLORD_HANDLER = CommandHandler(("removewarlord"), removewarlord)
UNWHITELIST_HANDLER = CommandHandler(("removewhitelist", "removerev"),
                                     removewhitelist)

WHITELISTLIST_HANDLER = CommandHandler(["whitelistlist", "revolutionaries"],
                                       whitelistlist)
WARLORDLIST_HANDLER = CommandHandler(["warlords"], warlordlist)
SUPPORTLIST_HANDLER = CommandHandler(["supportlist", "admirals"], supportlist)
SUDOLIST_HANDLER = CommandHandler(["sudolist", "worldgovt"], sudolist)
DEVLIST_HANDLER = CommandHandler(["devlist", "emperors"], devlist)

dispatcher.add_handler(SUDO_HANDLER)
dispatcher.add_handler(SUPPORT_HANDLER)
dispatcher.add_handler(WARLORD_HANDLER)
dispatcher.add_handler(WHITELIST_HANDLER)
dispatcher.add_handler(UNSUDO_HANDLER)
dispatcher.add_handler(UNSUPPORT_HANDLER)
dispatcher.add_handler(UNWARLORD_HANDLER)
dispatcher.add_handler(UNWHITELIST_HANDLER)

dispatcher.add_handler(WHITELISTLIST_HANDLER)
dispatcher.add_handler(WARLORDLIST_HANDLER)
dispatcher.add_handler(SUPPORTLIST_HANDLER)
dispatcher.add_handler(SUDOLIST_HANDLER)
dispatcher.add_handler(DEVLIST_HANDLER)

__mod_name__ = "Powers"
__handlers__ = [
    SUDO_HANDLER, SUPPORT_HANDLER, WARLORD_HANDLER, WHITELIST_HANDLER,
    UNSUDO_HANDLER, UNSUPPORT_HANDLER, UNWARLORD_HANDLER, UNWHITELIST_HANDLER,
    WHITELISTLIST_HANDLER, WARLORDLIST_HANDLER, SUPPORTLIST_HANDLER,
    SUDOLIST_HANDLER, DEVLIST_HANDLER
]
