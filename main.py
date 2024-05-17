import pyrogram
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, InviteHashExpired, UsernameNotOccupied
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import time
import os
import threading
import json
from os import environ

# Environment variables
bot_token = environ.get("TOKEN", "") 
api_hash = environ.get("HASH", "") 
api_id = environ.get("ID", "")
bot = Client("mybot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

ss = environ.get("STRING", "")
if ss is not None:
    acc = Client("myacc" ,api_id=api_id, api_hash=api_hash, session_string=ss)
    acc.start()
else:
    acc = None

# Load language preferences
if os.path.exists("user_languages.json"):
    with open("user_languages.json", "r") as f:
        user_languages = json.load(f)
else:
    user_languages = {}

# Save language preferences
def save_user_languages():
    with open("user_languages.json", "w") as f:
        json.dump(user_languages, f)

# Get user language
def get_user_language(user_id):
    return user_languages.get(str(user_id), None)

# Set user language
def set_user_language(user_id, language):
    user_languages[str(user_id)] = language
    save_user_languages()

# Download status
def downstatus(statusfile, message):
    while True:
        if os.path.exists(statusfile):
            break

    time.sleep(3)
    while os.path.exists(statusfile):
        with open(statusfile, "r") as downread:
            txt = downread.read()
        try:
            bot.edit_message_text(message.chat.id, message.id, f"__Downloaded__ : **{txt}**")
            time.sleep(10)
        except:
            time.sleep(5)

# Upload status
def upstatus(statusfile, message):
    while True:
        if os.path.exists(statusfile):
            break

    time.sleep(3)
    while os.path.exists(statusfile):
        with open(statusfile, "r") as upread:
            txt = upread.read()
        try:
            bot.edit_message_text(message.chat.id, message.id, f"__Uploaded__ : **{txt}**")
            time.sleep(10)
        except:
            time.sleep(5)

# Progress writer
def progress(current, total, message, type):
    with open(f'{message.id}{type}status.txt', "w") as fileup:
        fileup.write(f"{current * 100 / total:.1f}%")

# Start command
@bot.on_message(filters.command(["start"]))
def send_start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    user_id = message.from_user.id
    user_language = get_user_language(user_id)
    if user_language is None:
        bot.send_message(message.chat.id, "__ choose your language  /  اختار لغه البوت __",
                         reply_markup=InlineKeyboardMarkup([
                             [InlineKeyboardButton("English 💞", callback_data="lang_en"),
                              InlineKeyboardButton(" 💙 عربي", callback_data="lang_ar")]
                         ]), reply_to_message_id=message.id)
    else:
        if user_language == "en":
            bot.send_message(message.chat.id, f"**👋 Hi {message.from_user.mention}, I am Save Restricted Bot, I can send you restricted content by its post link**\n\n{USAGE}",
                             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Channel ᏔᎯ ᏞᎬᎠ ᏢᎡᏫ", url="https://t.me/S_D_C_D")]]), reply_to_message_id=message.id)
        elif user_language == "ar":
            bot.send_message(message.chat.id, f"**👋 مرحبًا {message.from_user.mention}، أنا بوت حفظ المحتوى المقيد، يمكنني إرسال المحتوى المقيد لك عبر رابط المنشور**\n\n{USAGE_AR}",
                             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(" قناة ᏔᎯ ᏞᎬᎠ ᏢᎡᏫ", url="https://t.me/S_D_C_D")]]), reply_to_message_id=message.id)

@bot.on_callback_query(filters.regex("lang_"))
def language_callback(client, callback_query):
    user_id = callback_query.from_user.id
    language = callback_query.data.split("_")[1]
    set_user_language(user_id, language)
    if language == "en":
        bot.send_message(callback_query.message.chat.id, f"**👋 Hi {callback_query.from_user.mention}, I am Save Restricted Bot, I can send you restricted content by its post link**\n\n{USAGE}",
                         reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Channel ᏔᎯ ᏞᎬᎠ ᏢᎡᏫ", url="https://t.me/S_D_C_D")]]), reply_to_message_id=callback_query.message.id)
    elif language == "ar":
        bot.send_message(callback_query.message.chat.id, f"**👋 مرحبًا {callback_query.from_user.mention}، أنا بوت حفظ المحتوى المقيد، يمكنني إرسال المحتوى المقيد لك عبر رابط المنشور**\n\n{USAGE_AR}",
                         reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("قناة ᏔᎯ ᏞᎬᎠ ᏢᎡᏫ", url="https://t.me/S_D_C_D")]]), reply_to_message_id=callback_query.message.id)
    callback_query.answer()

@bot.on_message(filters.text)
def save(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    user_language = get_user_language(message.from_user.id)
    if user_language is None:
        bot.send_message(message.chat.id, "__ choose your language  /  اختار لغه البوت __",
                         reply_markup=InlineKeyboardMarkup([
                             [InlineKeyboardButton("English 💞", callback_data="lang_en"),
                              InlineKeyboardButton(" 💙 عربي", callback_data="lang_ar")]
                         ]), reply_to_message_id=message.id)
        return

    print(message.text)
    # Joining chats
    if "https://t.me/+" in message.text or "https://t.me/joinchat/" in message.text:
        if acc is None:
            if user_language == "en":
                bot.send_message(message.chat.id, "**String Session is not Set**", reply_to_message_id=message.id)
            elif user_language == "ar":
                bot.send_message(message.chat.id, "**جلسة السلسلة غير مضبوطة**", reply_to_message_id=message.id)
            return

        try:
            try:
                acc.join_chat(message.text)
            except Exception as e:
                bot.send_message(message.chat.id, f"**Error** : __{e}__", reply_to_message_id=message.id)
                return
            if user_language == "en":
                bot.send_message(message.chat.id, "**Chat Joined**", reply_to_message_id=message.id)
            elif user_language == "ar":
                bot.send_message(message.chat.id, "**تم الانضمام إلى الدردشة**", reply_to_message_id=message.id)
        except UserAlreadyParticipant:
            if user_language == "en":
                bot.send_message(message.chat.id, "**Chat already Joined**", reply_to_message_id=message.id)
            elif user_language == "ar":
                bot.send_message(message.chat.id, "**تم الانضمام إلى الدردشة مسبقاً**", reply_to_message_id=message.id)
        except InviteHashExpired:
            if user_language == "en":
                bot.send_message(message.chat.id, "**Invalid Link**", reply_to_message_id=message.id)
            elif user_language == "ar":
                bot.send_message(message.chat.id, "**رابط غير صالح**", reply_to_message_id=message.id)

    # Getting message
    elif "https://t.me/" in message.text:
        datas = message.text.split("/")
        temp = datas[-1].replace("?single", "").split("-")
        fromID = int(temp[0].strip())
        try:
            toID = int(temp[1].strip())
        except:
            toID = fromID

        for msgid in range(fromID, toID + 1):
            # Private
            if "https://t.me/c/" in message.text:
                chatid = int("-100" + datas[4])

                if acc is None:
                    if user_language == "en":
                        bot.send_message(message.chat.id, "**String Session is not Set**", reply_to_message_id=message.id)
                    elif user_language == "ar":
                        bot.send_message(message.chat.id, "**جلسة السلسلة غير مضبوطة**", reply_to_message_id=message.id)
                    return

                handle_private(message, chatid, msgid)

            # Bot
            elif "https://t.me/b/" in message.text:
                username = datas[4]

                if acc is None:
                    if user_language == "en":
                        bot.send_message(message.chat.id, "**String Session is not Set**", reply_to_message_id=message.id)
                    elif user_language == "ar":
                        bot.send_message(message.chat.id, "**جلسة السلسلة غير مضبوطة**", reply_to_message_id=message.id)
                    return
                try:
                    handle_private(message, username, msgid)
                except Exception as e:
                    bot.send_message(message.chat.id, f"**Error** : __{e}__", reply_to_message_id=message.id)

            # Public
            else:
                username = datas[3]

                try:
                    msg = bot.get_messages(username, msgid)
                except UsernameNotOccupied:
                    if user_language == "en":
                        bot.send_message(message.chat.id, "**The username is not occupied by anyone**", reply_to_message_id=message.id)
                    elif user_language == "ar":
                        bot.send_message(message.chat.id, "**اسم المستخدم غير مشغول من قبل أي شخص**", reply_to_message_id=message.id)
                    return

                try:
                    bot.copy_message(message.chat.id, msg.chat.id, msg.id, reply_to_message_id=message.id)
                except:
                    if acc is None:
                        if user_language == "en":
                            bot.send_message(message.chat.id, "**String Session is not Set**", reply_to_message_id=message.id)
                        elif user_language == "ar":
                            bot.send_message(message.chat.id, "**جلسة السلسلة غير مضبوطة**", reply_to_message_id=message.id)
                        return
                    try:
                        handle_private(message, username, msgid)
                    except Exception as e:
                        bot.send_message(message.chat.id, f"**Error** : __{e}__", reply_to_message_id=message.id)

            # Wait time
            time.sleep(3)

# Handle private messages
def handle_private(message: pyrogram.types.messages_and_media.message.Message, chatid: int, msgid: int):
    msg: pyrogram.types.messages_and_media.message.Message = acc.get_messages(chatid, msgid)
    msg_type = get_message_type(msg)

    if "Text" == msg_type:
        bot.send_message(message.chat.id, msg.text, entities=msg.entities, reply_to_message_id=message.id)
        return

    smsg = bot.send_message(message.chat.id, '__Downloading__', reply_to_message_id=message.id)
    dosta = threading.Thread(target=lambda: downstatus(f'{message.id}downstatus.txt', smsg), daemon=True)
    dosta.start()
    file = acc.download_media(msg, progress=progress, progress_args=[message, "down"])
    os.remove(f'{message.id}downstatus.txt')

    upsta = threading.Thread(target=lambda: upstatus(f'{message.id}upstatus.txt', smsg), daemon=True)
    upsta.start()

    if "Document" == msg_type:
        try:
            thumb = acc.download_media(msg.document.thumbs[0].file_id)
        except:
            thumb = None

        bot.send_document(message.chat.id, file, thumb=thumb, caption=msg.caption, caption_entities=msg.caption_entities,
                          reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])
        if thumb is not None:
            os.remove(thumb)

    elif "Video" == msg_type:
        try:
            thumb = acc.download_media(msg.video.thumbs[0].file_id)
        except:
            thumb = None

        bot.send_video(message.chat.id, file, duration=msg.video.duration, width=msg.video.width, height=msg.video.height,
                       thumb=thumb, caption=msg.caption, caption_entities=msg.caption_entities,
                       reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])
        if thumb is not None:
            os.remove(thumb)

    elif "Animation" == msg_type:
        bot.send_animation(message.chat.id, file, reply_to_message_id=message.id)

    elif "Sticker" == msg_type:
        bot.send_sticker(message.chat.id, file, reply_to_message_id=message.id)

    elif "Voice" == msg_type:
        bot.send_voice(message.chat.id, file, caption=msg.caption, thumb=thumb, caption_entities=msg.caption_entities,
                       reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])

    elif "Audio" == msg_type:
        try:
            thumb = acc.download_media(msg.audio.thumbs[0].file_id)
        except:
            thumb = None

        bot.send_audio(message.chat.id, file, caption=msg.caption, caption_entities=msg.caption_entities,
                      reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])
        if thumb is not None:
            os.remove(thumb)

    elif "Photo" == msg_type:
        bot.send_photo(message.chat.id, file, caption=msg.caption, caption_entities=msg.caption_entities,
                       reply_to_message_id=message.id)

    os.remove(file)
    if os.path.exists(f'{message.id}upstatus.txt'):
        os.remove(f'{message.id}upstatus.txt')
    bot.delete_messages(message.chat.id, [smsg.id])

# Get the type of message
def get_message_type(msg: pyrogram.types.messages_and_media.message.Message):
    try:
        msg.document.file_id
        return "Document"
    except:
        pass

    try:
        msg.video.file_id
        return "Video"
    except:
        pass

    try:
        msg.animation.file_id
        return "Animation"
    except:
        pass

    try:
        msg.sticker.file_id
        return "Sticker"
    except:
        pass

    try:
        msg.voice.file_id
        return "Voice"
    except:
        pass

    try:
        msg.audio.file_id
        return "Audio"
    except:
        pass

    try:
        msg.photo.file_id
        return "Photo"
    except:
        pass

    try:
        msg.text
        return "Text"
    except:
        pass

USAGE = """**FOR PUBLIC CHATS**

**__just send post/s link__**

**FOR PRIVATE CHATS**

**__first send invite link of the chat (unnecessary if the account of string session already member of the chat)
then send post/s link__**

**FOR BOT CHATS**

**__send link with** '/b/', **bot's username and message id, you might want to install some unofficial client to get the id like below__**

```
https://t.me/b/botusername/4321
```

**MULTI POSTS**

**__send public/private posts link as explained above with formate "from - to" to send multiple messages like below__**

```
https://t.me/xxxx/1001-1010

https://t.me/c/xxxx/101 - 120
```

**__note that space in between doesn't matter__**
"""

USAGE_AR = """- **للدردشات العامة**

**__ارسل رابط الرساله فقط لتحويلها__**

- **للدردشات الخاصة**

**__أرسل أولاً رابط دعوة للدردشة (غير ضروري إذا كان حساب جلسة السلسلة عضوًا بالفعل في الدردشة)
ثم أرسل رابط المشاركة/المنشورات__**

**لمحادثات الروبوت**

**__أرسل رابطًا يحتوي على "/b/"، واسم مستخدم الروبوت ومعرف الرسالة، وقد ترغب في تثبيت عميل غير رسمي للحصول على المعرف كما هو موضح أدناه__**

```
https://t.me/b/botusername/4321
```

**تحويل متعدد**

**__إرسال رابط المشاركات العامة/الخاصة كما هو موضح أعلاه بصيغة "من - إلى" لإرسال رسائل متعددة كما هو موضح أدناه__**

```
https://t.me/xxxx/1001-1010

https://t.me/c/xxxx/101 - 120
```

**__لاحظ أن المسافة بينهما لا يهم__**
"""


# infinty polling
bot.run()
