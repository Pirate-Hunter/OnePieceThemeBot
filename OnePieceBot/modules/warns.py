import html
import re
from typing import Optional

import telegram
from OnePieceBot import BAN_STICKER, WARLORDS, REVOLUTIONARIES, dispatcher
from OnePieceBot.modules.disable import DisableAbleCommandHandler
from OnePieceBot.modules.helper_funcs.chat_status import (bot_admin,
                                                           can_restrict,
                                                           is_user_admin,
                                                           user_admin,
                                                           user_admin_no_reply)
from OnePieceBot.modules.helper_funcs.extraction import (extract_text,
                                                          extract_user,
                                                          extract_user_and_text)
from OnePieceBot.modules.helper_funcs.filters import CustomFilters
from OnePieceBot.modules.helper_funcs.misc import split_message
from OnePieceBot.modules.helper_funcs.string_handling import split_quotes
from OnePieceBot.modules.log_channel import loggable
from OnePieceBot.modules.sql import warns_sql as sql
from telegram import (CallbackQuery, Chat, InlineKeyboardButton,
                      InlineKeyboardMarkup, Message, ParseMode, Update, User)
from telegram.error import BadRequest
from telegram.ext import (CallbackContext, CallbackQueryHandler, CommandHandler,
                          DispatcherHandlerStop, Filters, MessageHandler,
                          run_async)
from telegram.utils.helpers import mention_html

WARN_HANDLER_GROUP = 9
CURRENT_WARNING_FILTER_STRING = "<b>Current warning filters in this chat:</b>\n"


# Not async
def warn(user: User,
         chat: Chat,
<<<<<<< HEAD
=======
         bot: any,
>>>>>>> 0f0e4204d9fb34b53f2324f4b671338fd9713012
         reason: str,
         message: Message,
         warner: User = None) -> str:
    if is_user_admin(chat, user.id):
        # message.reply_text("Damn admins, They are too far to be One Punched!")
        return

    if user.id in WARLORDS:
        if warner:
            message.reply_text("WARLORDS cant be warned.")
        else:
            message.reply_text(
                "Tiger triggered an auto warn filter!\n I can't warn WARLORDS but they should avoid abusing this."
            )
        return

    if user.id in REVOLUTIONARIES:
        if warner:
            message.reply_text("Wolf disasters are warn immune.")
        else:
            message.reply_text(
                "Wolf Disaster triggered an auto warn filter!\nI can't warn REVOLUTIONARIES but they should avoid abusing this."
            )
        return

    if warner:
        warner_tag = mention_html(warner.id, warner.first_name)
    else:
        warner_tag = "Automated warn filter."

<<<<<<< HEAD
    limit, soft_warn = sql.get_warn_setting(chat.id)
=======
    limit, warn_setting = sql.get_warn_setting(chat.id)
>>>>>>> 0f0e4204d9fb34b53f2324f4b671338fd9713012
    num_warns, reasons = sql.warn_user(user.id, chat.id, reason)
    if num_warns >= limit:
        sql.reset_warns(user.id, chat.id)
        if soft_warn:  # punch
            chat.unban_member(user.id)
            reply = (
                f"<code>❕</code><b>Punch Event</b>\n"
                f"<code> </code><b>•  User:</b> {mention_html(user.id, user.first_name)}\n"
                f"<code> </code><b>•  Count:</b> {limit}")

        else:  # ban
            chat.kick_member(user.id)
            reply = (
                f"<code>❕</code><b>Ban Event</b>\n"
                f"<code> </code><b>•  User:</b> {mention_html(user.id, user.first_name)}\n"
                f"<code> </code><b>•  Count:</b> {limit}")

        for warn_reason in reasons:
            reply += f"\n - {html.escape(warn_reason)}"

        # message.bot.send_sticker(chat.id, BAN_STICKER)  # Saitama's sticker
        keyboard = None
        log_reason = (f"<b>{html.escape(chat.title)}:</b>\n"
                      f"#WARN_BAN\n"
                      f"<b>Admin:</b> {warner_tag}\n"
                      f"<b>User:</b> {mention_html(user.id, user.first_name)}\n"
                      f"<b>Reason:</b> {reason}\n"
                      f"<b>Counts:</b> <code>{num_warns}/{limit}</code>")

    else:
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton(
                "🔘 Remove warn", callback_data="rm_warn({})".format(user.id))
        ]])

        reply = (
            f"<code>❕</code><b>Warn Event</b>\n"
            f"<code> </code><b>•  User:</b> {mention_html(user.id, user.first_name)}\n"
            f"<code> </code><b>•  Count:</b> {num_warns}/{limit}")
        if reason:
            reply += f"\n<code> </code><b>•  Reason:</b> {html.escape(reason)}"

        log_reason = (f"<b>{html.escape(chat.title)}:</b>\n"
                      f"#WARN\n"
                      f"<b>Admin:</b> {warner_tag}\n"
                      f"<b>User:</b> {mention_html(user.id, user.first_name)}\n"
                      f"<b>Reason:</b> {reason}\n"
                      f"<b>Counts:</b> <code>{num_warns}/{limit}</code>")

    try:
        message.reply_text(
            reply, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            message.reply_text(
                reply,
                reply_markup=keyboard,
                parse_mode=ParseMode.HTML,
                quote=False)
        else:
            raise
    return log_reason

<<<<<<< HEAD
=======
def swarn(user: User,
          chat: Chat,
          bot: any,
          reason: str,
          message: Message,
          warner: User = None) -> str:
    if is_user_admin(chat, user.id):
      return

    if user.id in WARLORDS:
      if warner:
        message.reply_text('Warlords cant be warned.')
      else:
        message.reply_text(
          'A Warlord triggered an auto warn filter.\nI cant warn Warlords but they have to stop abusing this.')
      return

    if user.id in REVOLUTIONARIES:
      if warner:
        message.reply_text('Revolutionearies are warn immune.')
      else:
        message.reply_text('A revolutionary triggered an auto warn filter.\nI cant warn revolutionaries but they have to stop abusing this.')
      return

    if warner:
        warner_tag = mention_html(warner.id, warner.first_name)
    else :
        warner_tag = 'Automated warn filter.'

    limit, warn_setting = sql.get_warn_setting(chat.id)
    num_warns, reasons = sql.warn_user(user.id, chat.id, reason)
    if num_warns >= limit:
        sql.reset_warns(user.id, chat.id)
        if warn_setting.lower() == 'punch':  # punch
            chat.unban_member(user.id)
            reply = (
                f"<code>❕</code><b>Punch Event</b>\n"
                f"<code> </code><b>•  User:</b> {mention_html(user.id, user.first_name)}\n"
                f"<code> </code><b>•  Count:</b> {limit}")

        elif warn_setting.lower() == 'ban':  # ban
            chat.kick_member(user.id)
            reply = (
                f"<code>🔨</code><b>Ban Event</b>\n"
                f"<code> </code><b>•  User:</b> {mention_html(user.id, user.first_name)}\n"
                f"<code> </code><b>•  Count:</b> {limit}")

        elif warn_setting.lower() == 'mute': # mute
          usr = chat.get_member(user.id)
          ChatPerms = ChatPermissions(can_send_messages=False)
          if usr.can_send_messages is None or usr.can_send_messages:
            bot.restict_chat_member(chat.id, user.id, ChatPerms)
            reply = (
              f"<code>❕</code><b>Mute Event</b>\n"
              f"<code> </code><b>•  User:</b> {mention_html(user.id, user.first_name)}"
              f"<code> </code><b>•  Count:</b> {limit}"
            )

        for warn_reason in reasons:
            reply += f"\n - {html.escape(warn_reason)}"

        # message.bot.send_sticker(chat.id, BAN_STICKER)  # Saitama's sticker
        keyboard = None
        log_reason = (f"<b>{html.escape(chat.title)}:</b>\n"
                      f"#WARN_BAN\n"
                      f"<b>Admin:</b> {warner_tag}\n"
                      f"<b>User:</b> {mention_html(user.id, user.first_name)}\n"
                      f"<b>Reason:</b> {reason}\n"
                      f"<b>Counts:</b> <code>{num_warns}/{limit}</code>")

    else:
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton(
                "🔘 Remove warn", callback_data="rm_warn({})".format(user.id))
        ]])

        reply = (
            f"<code>❕</code><b>Warn Event</b>\n"
            f"<code> </code><b>•  User:</b> {mention_html(user.id, user.first_name)}\n"
            f"<code> </code><b>•  Count:</b> {num_warns}/{limit}")
        if reason:
            reply += f"\n<code> </code><b>•  Reason:</b> {html.escape(reason)}"

        log_reason = (f"<b>{html.escape(chat.title)}:</b>\n"
                      f"#WARN\n"
                      f"<b>Admin:</b> {warner_tag}\n"
                      f"<b>User:</b> {mention_html(user.id, user.first_name)}\n"
                      f"<b>Reason:</b> {reason}\n"
                      f"<b>Counts:</b> <code>{num_warns}/{limit}</code>")

    try:
        message.reply_text(reply, reply_markup=keyboard, parse_mode=ParseMode.HTML)
        bot.deleteMessage(chat.id, message.reply_to_message.message_id)
    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            message.reply_text(
                reply,
                reply_markup=keyboard,
                parse_mode=ParseMode.HTML,
                quote=False)
        else:
            raise
    return log_reason

def sdwarn(user: User,
          chat: Chat,
          bot: any,
          reason: str,
          message: Message,
          warner: User = None) -> str:
    if is_user_admin(chat, user.id):
      return

    if user.id in WARLORDS:
      if warner:
        message.reply_text('Warlords cant be warned.')
      else:
        message.reply_text(
          'A Warlord triggered an auto warn filter.\nI cant warn Warlords but they have to stop abusing this.')
      return

    if user.id in REVOLUTIONARIES:
      if warner:
        message.reply_text('Revolutionearies are warn immune.')
      else:
        message.reply_text('A revolutionary triggered an auto warn filter.\nI cant warn revolutionaries but they have to stop abusing this.')
      return

    if warner:
        warner_tag = mention_html(warner.id, warner.first_name)
    else :
        warner_tag = 'Automated warn filter.'

    limit, warn_setting = sql.get_warn_setting(chat.id)
    num_warns, reasons = sql.warn_user(user.id, chat.id, reason)
    if num_warns >= limit:
        sql.reset_warns(user.id, chat.id)
        if warn_setting.lower() == 'punch':  # punch
            chat.unban_member(user.id)
            reply = (
                f"<code>❕</code><b>Punch Event</b>\n"
                f"<code> </code><b>•  User:</b> {mention_html(user.id, user.first_name)}\n"
                f"<code> </code><b>•  Count:</b> {limit}")

        elif warn_setting.lower() == 'ban':  # ban
            chat.kick_member(user.id)
            reply = (
                f"<code>🔨</code><b>Ban Event</b>\n"
                f"<code> </code><b>•  User:</b> {mention_html(user.id, user.first_name)}\n"
                f"<code> </code><b>•  Count:</b> {limit}")

        elif warn_setting.lower() == 'mute': # mute
          usr = chat.get_member(user.id)
          ChatPerms = ChatPermissions(can_send_messages=False)
          if usr.can_send_messages is None or usr.can_send_messages:
            bot.restict_chat_member(chat.id, user.id, ChatPerms)
            reply = (
              f"<code>❕</code><b>Mute Event</b>\n"
              f"<code> </code><b>•  User:</b> {mention_html(user.id, user.first_name)}"
              f"<code> </code><b>•  Count:</b> {limit}"
            )

        for warn_reason in reasons:
            reply += f"\n - {html.escape(warn_reason)}"

        # message.bot.send_sticker(chat.id, BAN_STICKER)  # Saitama's sticker
        keyboard = None
        log_reason = (f"<b>{html.escape(chat.title)}:</b>\n"
                      f"#WARN_BAN\n"
                      f"<b>Admin:</b> {warner_tag}\n"
                      f"<b>User:</b> {mention_html(user.id, user.first_name)}\n"
                      f"<b>Reason:</b> {reason}\n"
                      f"<b>Counts:</b> <code>{num_warns}/{limit}</code>")

    else:
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton(
                "🔘 Remove warn", callback_data="rm_warn({})".format(user.id))
        ]])

        reply = (
            f"<code>❕</code><b>Warn Event</b>\n"
            f"<code> </code><b>•  User:</b> {mention_html(user.id, user.first_name)}\n"
            f"<code> </code><b>•  Count:</b> {num_warns}/{limit}")
        if reason:
            reply += f"\n<code> </code><b>•  Reason:</b> {html.escape(reason)}"

        log_reason = (f"<b>{html.escape(chat.title)}:</b>\n"
                      f"#WARN\n"
                      f"<b>Admin:</b> {warner_tag}\n"
                      f"<b>User:</b> {mention_html(user.id, user.first_name)}\n"
                      f"<b>Reason:</b> {reason}\n"
                      f"<b>Counts:</b> <code>{num_warns}/{limit}</code>")

    msg_id = message.message_id
    reply_msg_id = message.reply_to_message.message_id
    to_delete = [msg_id, reply_msg_id]
    try:
        message.reply_text(reply, reply_markup=keyboard, parse_mode=ParseMode.HTML)
        for x in to_delete:
            try:
                bot.deleteMessage(chat.id, int(x))
            except BadRequest as err:
                return
    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            message.reply_text(
                reply,
                reply_markup=keyboard,
                parse_mode=ParseMode.HTML,
                quote=False)
        else:
            raise
    return log_reason

def dwarn(user: User,
          chat: Chat,
          bot: any,
          reason: str,
          message: Message,
          warner: User = None) -> str:
    if is_user_admin(chat, user.id):
      return

    if user.id in WARLORDS:
      if warner:
        message.reply_text('Warlords cant be warned.')
      else:
        message.reply_text(
          'A Warlord triggered an auto warn filter.\nI cant warn Warlords but they have to stop abusing this.')
      return

    if user.id in REVOLUTIONARIES:
      if warner:
        message.reply_text('Revolutionearies are warn immune.')
      else:
        message.reply_text('A revolutionary triggered an auto warn filter.\nI cant warn revolutionaries but they have to stop abusing this.')
      return

    if warner:
        warner_tag = mention_html(warner.id, warner.first_name)
    else :
        warner_tag = 'Automated warn filter.'

    limit, warn_setting = sql.get_warn_setting(chat.id)
    num_warns, reasons = sql.warn_user(user.id, chat.id, reason)
    if num_warns >= limit:
        sql.reset_warns(user.id, chat.id)
        if warn_setting.lower() == 'punch':  # punch
            chat.unban_member(user.id)
            reply = (
                f"<code>❕</code><b>Punch Event</b>\n"
                f"<code> </code><b>•  User:</b> {mention_html(user.id, user.first_name)}\n"
                f"<code> </code><b>•  Count:</b> {limit}")

        elif warn_setting.lower() == 'ban':  # ban
            chat.kick_member(user.id)
            reply = (
                f"<code>🔨</code><b>Ban Event</b>\n"
                f"<code> </code><b>•  User:</b> {mention_html(user.id, user.first_name)}\n"
                f"<code> </code><b>•  Count:</b> {limit}")

        elif warn_setting.lower() == 'mute': # mute
          usr = chat.get_member(user.id)
          ChatPerms = ChatPermissions(can_send_messages=False)
          if usr.can_send_messages is None or usr.can_send_messages:
            bot.restict_chat_member(chat.id, user.id, ChatPerms)
            reply = (
              f"<code>❕</code><b>Mute Event</b>\n"
              f"<code> </code><b>•  User:</b> {mention_html(user.id, user.first_name)}"
              f"<code> </code><b>•  Count:</b> {limit}"
            )

        for warn_reason in reasons:
            reply += f"\n - {html.escape(warn_reason)}"

        # message.bot.send_sticker(chat.id, BAN_STICKER)  # Saitama's sticker
        keyboard = None
        log_reason = (f"<b>{html.escape(chat.title)}:</b>\n"
                      f"#WARN_BAN\n"
                      f"<b>Admin:</b> {warner_tag}\n"
                      f"<b>User:</b> {mention_html(user.id, user.first_name)}\n"
                      f"<b>Reason:</b> {reason}\n"
                      f"<b>Counts:</b> <code>{num_warns}/{limit}</code>")

    else:
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton(
                "🔘 Remove warn", callback_data="rm_warn({})".format(user.id))
        ]])

        reply = (
            f"<code>❕</code><b>Warn Event</b>\n"
            f"<code> </code><b>•  User:</b> {mention_html(user.id, user.first_name)}\n"
            f"<code> </code><b>•  Count:</b> {num_warns}/{limit}")
        if reason:
            reply += f"\n<code> </code><b>•  Reason:</b> {html.escape(reason)}"

        log_reason = (f"<b>{html.escape(chat.title)}:</b>\n"
                      f"#WARN\n"
                      f"<b>Admin:</b> {warner_tag}\n"
                      f"<b>User:</b> {mention_html(user.id, user.first_name)}\n"
                      f"<b>Reason:</b> {reason}\n"
                      f"<b>Counts:</b> <code>{num_warns}/{limit}</code>")

    try:
        message.reply_text(reply, reply_markup=keyboard, parse_mode=ParseMode.HTML)
        bot.deleteMessage(chat.id, message.message_id)
    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            message.reply_text(
                reply,
                reply_markup=keyboard,
                parse_mode=ParseMode.HTML,
                quote=False)
        else:
            raise
    return log_reason
      
>>>>>>> 0f0e4204d9fb34b53f2324f4b671338fd9713012

@run_async
@user_admin_no_reply
@bot_admin
@loggable
def button(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"rm_warn\((.+?)\)", query.data)
    if match:
        user_id = match.group(1)
        chat: Optional[Chat] = update.effective_chat
        res = sql.remove_warn(user_id, chat.id)
        if res:
            update.effective_message.edit_text(
                "Warn removed by {}.".format(
                    mention_html(user.id, user.first_name)),
                parse_mode=ParseMode.HTML)
            user_member = chat.get_member(user_id)
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"#UNWARN\n"
                f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
                f"<b>User:</b> {mention_html(user_member.user.id, user_member.user.first_name)}"
            )
        else:
            update.effective_message.edit_text(
                "User already has no warns.", parse_mode=ParseMode.HTML)

    return ""


@run_async
@user_admin
@can_restrict
@loggable
def warn_user(update: Update, context: CallbackContext) -> str:
    args = context.args
<<<<<<< HEAD
=======
    bot = context.bot
>>>>>>> 0f0e4204d9fb34b53f2324f4b671338fd9713012
    message: Optional[Message] = update.effective_message
    chat: Optional[Chat] = update.effective_chat
    warner: Optional[User] = update.effective_user

    user_id, reason = extract_user_and_text(message, args)

    if user_id:
        if message.reply_to_message and message.reply_to_message.from_user.id == user_id:
<<<<<<< HEAD
            return warn(message.reply_to_message.from_user, chat, reason,
                        message.reply_to_message, warner)
        else:
            return warn(
                chat.get_member(user_id).user, chat, reason, message, warner)
=======
            return warn(message.reply_to_message.from_user, chat, bot,  reason,
                        message.reply_to_message, warner)
        else:
            return warn(
                chat.get_member(user_id).user, chat, bot, reason, message, warner)
>>>>>>> 0f0e4204d9fb34b53f2324f4b671338fd9713012
    else:
        message.reply_text("That looks like an invalid User ID to me.")
    return ""

<<<<<<< HEAD
=======
@run_async
@user_admin
@can_restrict
@loggable
def dwarn_user(update: Update, context: CallbackContext) -> str:
  args = context.args
  bot = context.bot
  message: Optional[Message] = update.effective_message
  chat: Optional[Chat] = update.effective_chat
  warner: Optional[User] = update.effective_user
  
  user_id, reason = extract_user_and_text(message, args)
  
  if user_id:
    if mesaage.reply_to_message and message.reply_to_message.from_user.id == user_id:
      return dwarn(message.reply_to_message.from_user, bot, chat, reason,
        message.reply_to_message,  warner)
    else: 
      return dwarn(
        chat.get_member(user_id).user, chat, bot, reason, message, warner)
      
  else:
    message.reply_text('That looks like an invalid User ID to me.')

@run_async
@user_admin
@can_restrict
@loggable
def swarn_user(update: Update, context: CallbackContext) -> str:
  args = context.args
  bot = context.bot
  message: Optional[Message] = update.effective_message
  chat: Optional[Chat] = update.effective_chat
  warner: Optional[User] = update.effective_user
  
  user_id, reason = extract_user_and_text(message, args)
  
  if user_id:
    if mesaage.reply_to_message and message.reply_to_message.from_user.id == user_id:
      return dwarn(message.reply_to_message.from_user, bot, chat, reason,
        message.reply_to_message,  warner)
    else: 
      return dwarn(
        chat.get_member(user_id).user, chat, bot, reason, message, warner)
      
  else:
    message.reply_text('That looks like an invalid User ID to me.')

@run_async
@user_admin
@can_restrict
@loggable
def sdwarn_user(update: Update, context: CallbackContext) -> str:
  args = context.args
  bot = context.bot
  message: Optional[Message] = update.effective_message
  chat: Optional[Chat] = update.effective_chat
  warner: Optional[User] = update.effective_user
  
  user_id, reason = extract_user_and_text(message, args)
  
  if user_id:
    if mesaage.reply_to_message and message.reply_to_message.from_user.id == user_id:
      return dwarn(message.reply_to_message.from_user, bot, chat, reason,
        message.reply_to_message,  warner)
    else: 
      return dwarn(
        chat.get_member(user_id).user, chat, bot, reason, message, warner)
      
  else:
    message.reply_text('That looks like an invalid User ID to me.')

@run_async
def rm_warn(
    chat: Chat,
    update: Update,
    user: User,
    context: CallbackContext) -> str:
    bot = context.bot
    args = context.args
    msg = update.effective_message
    limit, warn_setting = sql.get_warn_setting(chat.id)

    if is_user_admin(chat, user.id):
        user_id = extract_user(msg, args)
        if not user_id:
            msg.reply_text("Provide a user to check his/her warns and remove them.")
        else:
            warns = sql.get_warns(user_id, chat.id)
            if warns and warns[0] != 0:
                num_warns, reasons = warns
                if num_warns >= limit:
                    msg.reply_text("This user has already been punished.")
                else:
                    keyboard = InlineKeyboardMarkup([[
                        InlineKeyboardButton(
                        "🔘 Remove warn", callback_data="rm_warn({})".format(user_id))
                    ]])
                    try:
                        msg.reply_text(
                            f"This user has {num_warns}/{limit} warns.",
                            reply_markup=keyboard
                        )
                    except BadRequest as err:
                        msg.reply_text(
                            f"This user has {num_warns}/{limit} warns.",
                            reply_markup=keyboard,
                            quote=False
                        )
            else:
                msg.reply_text("This user doesn't have any warns.")

    else:
        mg.reply_text('Who dis non-admin guy telling me to remove his/her warn.')
            
>>>>>>> 0f0e4204d9fb34b53f2324f4b671338fd9713012

@run_async
@user_admin
@bot_admin
@loggable
def reset_warns(update: Update, context: CallbackContext) -> str:
    args = context.args
    message: Optional[Message] = update.effective_message
    chat: Optional[Chat] = update.effective_chat
    user: Optional[User] = update.effective_user

    user_id = extract_user(message, args)

    if user_id:
        sql.reset_warns(user_id, chat.id)
        message.reply_text("Warns have been reset!")
        warned = chat.get_member(user_id).user
        return (f"<b>{html.escape(chat.title)}:</b>\n"
                f"#RESETWARNS\n"
                f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
                f"<b>User:</b> {mention_html(warned.id, warned.first_name)}")
    else:
        message.reply_text("No user has been designated!")
    return ""


@run_async
def warns(update: Update, context: CallbackContext):
    args = context.args
    message: Optional[Message] = update.effective_message
    chat: Optional[Chat] = update.effective_chat
    user_id = extract_user(message, args) or update.effective_user.id
    result = sql.get_warns(user_id, chat.id)

    if result and result[0] != 0:
        num_warns, reasons = result
        limit, warn_setting = sql.get_warn_setting(chat.id)

        if reasons:
            text = f"This user has {num_warns}/{limit} warns, for the following reasons:"
            for reason in reasons:
                text += f"\n • {reason}"

            msgs = split_message(text)
            for msg in msgs:
                update.effective_message.reply_text(msg)
        else:
            update.effective_message.reply_text(
                f"User has {num_warns}/{limit} warns, but no reasons for any of them."
            )
    else:
        update.effective_message.reply_text("This user doesn't have any warns!")


# Dispatcher handler stop - do not async
@user_admin
def add_warn_filter(update: Update, context: CallbackContext):
    chat: Optional[Chat] = update.effective_chat
    msg: Optional[Message] = update.effective_message

    args = msg.text.split(
        None,
        1)  # use python's maxsplit to separate Cmd, keyword, and reply_text

    if len(args) < 2:
        return

    extracted = split_quotes(args[1])

    if len(extracted) >= 2:
        # set trigger -> lower, so as to avoid adding duplicate filters with different cases
        keyword = extracted[0].lower()
        content = extracted[1]

    else:
        return

    # Note: perhaps handlers can be removed somehow using sql.get_chat_filters
    for handler in dispatcher.handlers.get(WARN_HANDLER_GROUP, []):
        if handler.filters == (keyword, chat.id):
            dispatcher.remove_handler(handler, WARN_HANDLER_GROUP)

    sql.add_warn_filter(chat.id, keyword, content)

    update.effective_message.reply_text(f"Warn handler added for '{keyword}'!")
    raise DispatcherHandlerStop


@user_admin
def remove_warn_filter(update: Update, context: CallbackContext):
    chat: Optional[Chat] = update.effective_chat
    msg: Optional[Message] = update.effective_message

    args = msg.text.split(
        None,
        1)  # use python's maxsplit to separate Cmd, keyword, and reply_text

    if len(args) < 2:
        return

    extracted = split_quotes(args[1])

    if len(extracted) < 1:
        return

    to_remove = extracted[0]

    chat_filters = sql.get_chat_warn_triggers(chat.id)

    if not chat_filters:
        msg.reply_text("No warning filters are active here!")
        return

    for filt in chat_filters:
        if filt == to_remove:
            sql.remove_warn_filter(chat.id, to_remove)
            msg.reply_text("Okay, I'll stop warning people for that.")
            raise DispatcherHandlerStop

    msg.reply_text(
        "That's not a current warning filter - run /warnlist for all active warning filters."
    )


@run_async
def list_warn_filters(update: Update, context: CallbackContext):
    chat: Optional[Chat] = update.effective_chat
    all_handlers = sql.get_chat_warn_triggers(chat.id)

    if not all_handlers:
        update.effective_message.reply_text(
            "No warning filters are active here!")
        return

    filter_list = CURRENT_WARNING_FILTER_STRING
    for keyword in all_handlers:
        entry = f" - {html.escape(keyword)}\n"
        if len(entry) + len(filter_list) > telegram.MAX_MESSAGE_LENGTH:
            update.effective_message.reply_text(
                filter_list, parse_mode=ParseMode.HTML)
            filter_list = entry
        else:
            filter_list += entry

    if filter_list != CURRENT_WARNING_FILTER_STRING:
        update.effective_message.reply_text(
            filter_list, parse_mode=ParseMode.HTML)


@run_async
@loggable
def reply_filter(update: Update, context: CallbackContext) -> str:
    chat: Optional[Chat] = update.effective_chat
    message: Optional[Message] = update.effective_message
    user: Optional[User] = update.effective_user

    if not user:  #Ignore channel
        return

    if user.id == 777000:
        return

    chat_warn_filters = sql.get_chat_warn_triggers(chat.id)
    to_match = extract_text(message)
    if not to_match:
        return ""

    for keyword in chat_warn_filters:
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, to_match, flags=re.IGNORECASE):
            user: Optional[User] = update.effective_user
            warn_filter = sql.get_warn_filter(chat.id, keyword)
            return warn(user, chat, warn_filter.reply, message)
    return ""


@run_async
@user_admin
@loggable
def set_warn_limit(update: Update, context: CallbackContext) -> str:
    args = context.args
    chat: Optional[Chat] = update.effective_chat
    user: Optional[User] = update.effective_user
    msg: Optional[Message] = update.effective_message

    if args:
        if args[0].isdigit():
            if int(args[0]) < 3:
                msg.reply_text("The minimum warn limit is 3!")
            else:
                sql.set_warn_limit(chat.id, int(args[0]))
                msg.reply_text("Updated the warn limit to {}".format(args[0]))
                return (
                    f"<b>{html.escape(chat.title)}:</b>\n"
                    f"#SET_WARN_LIMIT\n"
                    f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
                    f"Set the warn limit to <code>{args[0]}</code>")
        else:
            msg.reply_text("Give me a number as an arg!")
    else:
        limit, soft_warn = sql.get_warn_setting(chat.id)

        msg.reply_text("The current warn limit is {}".format(limit))
    return ""


@run_async
@user_admin
def set_warn_strength(update: Update, context: CallbackContext):
    args = context.args
    chat: Optional[Chat] = update.effective_chat
    user: Optional[User] = update.effective_user
    msg: Optional[Message] = update.effective_message

    if args:
        if args[0].lower() in ("on", "yes"):
            sql.set_warn_strength(chat.id, False)
            msg.reply_text("Too many warns will now result in a Ban!")
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
                f"Has enabled strong warns. Users will be seriously punched.(banned)"
            )

        elif args[0].lower() in ("off", "no"):
            sql.set_warn_strength(chat.id, True)
            msg.reply_text(
                "Too many warns will now result in a normal punch! Users will be able to join again after."
            )
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
                f"Has disabled strong punches. I will use normal punch on users."
            )

        else:
            msg.reply_text("I only understand on/yes/no/off!")
    else:
        limit, soft_warn = sql.get_warn_setting(chat.id)
        if soft_warn:
            msg.reply_text(
                "Warns are currently set to *punch* users when they exceed the limits.",
                parse_mode=ParseMode.MARKDOWN)
        else:
            msg.reply_text(
                "Warns are currently set to *Ban* users when they exceed the limits.",
                parse_mode=ParseMode.MARKDOWN)
    return ""


def __stats__():
    return (
        f"• {sql.num_warns()} overall warns, across {sql.num_warn_chats()} chats.\n"
        f"• {sql.num_warn_filters()} warn filters, across {sql.num_warn_filter_chats()} chats."
    )


def __import_data__(chat_id, data):
    for user_id, count in data.get('warns', {}).items():
        for x in range(int(count)):
            sql.warn_user(user_id, chat_id)


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id, user_id):
    num_warn_filters = sql.num_warn_chat_filters(chat_id)
    limit, soft_warn = sql.get_warn_setting(chat_id)
    return (
        f"This chat has `{num_warn_filters}` warn filters. "
        f"It takes `{limit}` warns before the user gets *{'kicked' if soft_warn else 'banned'}*."
    )


__help__ = """
 • `/warns <userhandle>`*:* get a user's number, and reason, of warns.
 • `/warnlist`*:* list of all current warning filters

*Admins only:*
 • `/warn <userhandle>`*:* warn a user. After 3 warns, the user will be banned from the group. Can also be used as a reply.
 • `/resetwarn <userhandle>`*:* reset the warns for a user. Can also be used as a reply.
 • `/addwarn <keyword> <reply message>`*:* set a warning filter on a certain keyword. If you want your keyword to \
be a sentence, encompass it with quotes, as such: `/addwarn "very angry" This is an angry user`. 
 • `/nowarn <keyword>`*:* stop a warning filter
 • `/warnlimit <num>`*:* set the warning limit
<<<<<<< HEAD
 • `/strongwarn <on/yes/off/no>`*:* If set to on, exceeding the warn limit will result in a ban. Else, will just punch.
=======
 • `/maxwarnaction `*:* If set to on, exceeding the warn limit will result in a ban by default. Else, the custom action the chat has set.

*Note*:
 • `/warnaction`*:* Works the same `/maxwarnaction`.
 • `/dswarn`*:* Works as the same as `/sdwarn`.
>>>>>>> 0f0e4204d9fb34b53f2324f4b671338fd9713012
"""

__mod_name__ = "Warnings"

WARN_HANDLER = CommandHandler("warn", warn_user, filters=Filters.group)
<<<<<<< HEAD
=======
SWARN_HANDLER = CommandHandler("swarn", swarn_user, filters=Filters.group)
DWARN_HANDLER = CommandHandler("dwarn", dwarn_user, filters=Filters.group)
SDWARN_HANDLER = CommandHandler(["sdwarn", "dswarn"], sdwarn_user, filters=Filters.group)
RM_WARN_CMD_HANDLER = CommandHandler("rmwarn", rm_warn, filters=Filters.group)

>>>>>>> 0f0e4204d9fb34b53f2324f4b671338fd9713012
RESET_WARN_HANDLER = CommandHandler(["resetwarn", "resetwarns"],
                                    reset_warns,
                                    filters=Filters.group)
CALLBACK_QUERY_HANDLER = CallbackQueryHandler(button, pattern=r"rm_warn")
MYWARNS_HANDLER = DisableAbleCommandHandler(
    "warns", warns, filters=Filters.group)
ADD_WARN_HANDLER = CommandHandler(
    "addwarn", add_warn_filter, filters=Filters.group)
RM_WARN_HANDLER = CommandHandler(["nowarn", "stopwarn"],
                                 remove_warn_filter,
                                 filters=Filters.group)
LIST_WARN_HANDLER = DisableAbleCommandHandler(["warnlist", "warnfilters"],
                                              list_warn_filters,
                                              filters=Filters.group,
                                              admin_ok=True)
WARN_FILTER_HANDLER = MessageHandler(CustomFilters.has_text & Filters.group,
                                     reply_filter)
WARN_LIMIT_HANDLER = CommandHandler(
    "warnlimit", set_warn_limit, filters=Filters.group)
WARN_STRENGTH_HANDLER = CommandHandler(
    "strongwarn", set_warn_strength, filters=Filters.group)

dispatcher.add_handler(WARN_HANDLER)
<<<<<<< HEAD
=======
dispatcher.add_handler(DWARN_HANDLER)
dispatcher.add_handler(SWARN_HANDLER)
dispatcher.add_handler(SDWARN_HANDLER)
dispatcher.add_handler(RM_WARN_CMD_HANDLER)

>>>>>>> 0f0e4204d9fb34b53f2324f4b671338fd9713012
dispatcher.add_handler(CALLBACK_QUERY_HANDLER)
dispatcher.add_handler(RESET_WARN_HANDLER)
dispatcher.add_handler(MYWARNS_HANDLER)
dispatcher.add_handler(ADD_WARN_HANDLER)
dispatcher.add_handler(RM_WARN_HANDLER)
dispatcher.add_handler(LIST_WARN_HANDLER)
dispatcher.add_handler(WARN_LIMIT_HANDLER)
dispatcher.add_handler(WARN_STRENGTH_HANDLER)
dispatcher.add_handler(WARN_FILTER_HANDLER, WARN_HANDLER_GROUP)