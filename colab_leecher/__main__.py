# ⛏️ MiN3R × Colab Station | https://github.com/AdittyaMondal/MiN3R-Colab-Station

# Suppress SyntaxWarnings from moviepy and other libraries on Python 3.12+
import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)

import logging
import os
import asyncio
from pyrogram import filters
from datetime import datetime
from asyncio import sleep, get_event_loop
from colab_leecher import colab_bot, OWNER
from colab_leecher.utility.handler import cancelTask
from .utility.variables import BOT, MSG, BotTimes, Paths
from .utility.task_manager import taskScheduler, task_starter
from .utility.queue_manager import task_queue, queue_worker
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .utility.helper import isLink, setThumbnail, message_deleter, send_settings

# Flag to track if queue worker is started
_queue_worker_started = False


src_request_msg = None


@colab_bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.delete()
    text = "**Hey There, 👋🏼 Welcome to ⛏️ MiN3R × Colab Station**\n\n◲ I am a Powerful File Transloading Bot 🚀\n◲ I can Transfer Files To Telegram or Your Google Drive From Various Sources ⛏️"
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Repository ⛏️",
                    url="https://github.com/AdittyaMondal/MiN3R-Colab-Station",
                ),
                InlineKeyboardButton(
                    "Channel 📣",
                    url="https://t.me/minerclouds",
                ),
            ],
        ]
    )
    await message.reply_text(text, reply_markup=keyboard)


@colab_bot.on_message(filters.command("tupload") & filters.private)
async def telegram_upload(client, message):
    global BOT, src_request_msg
    BOT.Mode.mode = "leech"
    BOT.Mode.ytdl = False

    text = "<b>⚡ Send Me DOWNLOAD LINK(s) 🔗»</b>\n\n🦀 Follow the below pattern\n\n<code>https//linktofile1.mp4\nhttps//linktofile2.mp4\n[Custom name space.mp4]\n{Password for zipping}\n(Password for unzip)</code>"

    src_request_msg = await task_starter(message, text)


@colab_bot.on_message(filters.command("gdupload") & filters.private)
async def drive_upload(client, message):
    global BOT, src_request_msg
    BOT.Mode.mode = "mirror"
    BOT.Mode.ytdl = False

    text = "<b>⚡ Send Me DOWNLOAD LINK(s) 🔗»</b>\n\n🦀 Follow the below pattern\n\n<code>https//linktofile1.mp4\nhttps//linktofile2.mp4\n[Custom name space.mp4]\n{Password for zipping}\n(Password for unzip)</code>"

    src_request_msg = await task_starter(message, text)


@colab_bot.on_message(filters.command("drupload") & filters.private)
async def directory_upload(client, message):
    global BOT, src_request_msg
    BOT.Mode.mode = "dir-leech"
    BOT.Mode.ytdl = False

    text = "<b>⚡ Send Me FOLDER PATH 🔗»</b>\n\n🦀 Below is an example\n\n<code>/home/user/Downloads/bot</code>"

    src_request_msg = await task_starter(message, text)


@colab_bot.on_message(filters.command("ytupload") & filters.private)
async def yt_upload(client, message):
    global BOT, src_request_msg
    BOT.Mode.mode = "leech"
    BOT.Mode.ytdl = True

    text = "<b>⚡ Send YTDL DOWNLOAD LINK(s) 🔗»</b>\n\n🦀 Follow the below pattern\n\n<code>https//linktofile1.mp4\nhttps//linktofile2.mp4\n[Custom name space.mp4]\n{Password for zipping}</code>"

    src_request_msg = await task_starter(message, text)


@colab_bot.on_message(filters.command("settings") & filters.private)
async def settings(client, message):
    if message.chat.id == OWNER:
        await message.delete()
        await send_settings(client, message, message.id, True)


@colab_bot.on_message(filters.reply)
async def setPrefix(client, message):
    global BOT, SETTING
    if BOT.State.prefix:
        BOT.Setting.prefix = message.text
        BOT.State.prefix = False

        await send_settings(client, message, message.reply_to_message_id, False)
        await message.delete()
    elif BOT.State.suffix:
        BOT.Setting.suffix = message.text
        BOT.State.suffix = False

        await send_settings(client, message, message.reply_to_message_id, False)
        await message.delete()


@colab_bot.on_message(filters.create(isLink) & ~filters.photo)
async def handle_url(client, message):
    global BOT
    from .utility.variables import PendingTask

    if src_request_msg:
        await src_request_msg.delete()
    
    if not BOT.State.started:
        return  # User hasn't initiated a task command yet
    
    # Parse the source links and options
    temp_source = message.text.splitlines()
    custom_name = ""
    zip_pswd = ""
    unzip_pswd = ""

    # Check for arguments in message
    for _ in range(3):
        if temp_source and temp_source[-1]:
            if temp_source[-1][0] == "[":
                custom_name = temp_source[-1][1:-1]
                temp_source.pop()
            elif temp_source[-1][0] == "{":
                zip_pswd = temp_source[-1][1:-1]
                temp_source.pop()
            elif temp_source[-1][0] == "(":
                unzip_pswd = temp_source[-1][1:-1]
                temp_source.pop()
            else:
                break
        else:
            break

    # Store in PendingTask to avoid overwriting running task's global state
    PendingTask.source = temp_source.copy()
    PendingTask.mode = BOT.Mode.mode
    PendingTask.ytdl = BOT.Mode.ytdl
    PendingTask.custom_name = custom_name
    PendingTask.zip_pswd = zip_pswd
    PendingTask.unzip_pswd = unzip_pswd
    PendingTask.stream_upload = BOT.Options.stream_upload
    PendingTask.caption = BOT.Options.caption
    PendingTask.convert_video = BOT.Options.convert_video
    PendingTask.video_out = BOT.Options.video_out
    
    # Only update global state if no task is running
    if not BOT.State.task_going:
        BOT.SOURCE = temp_source
        BOT.Options.custom_name = custom_name
        BOT.Options.zip_pswd = zip_pswd
        BOT.Options.unzip_pswd = unzip_pswd
    
    # Show task type selection regardless of whether another task is running
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Regular", callback_data="normal")],
            [
                InlineKeyboardButton("Compress", callback_data="zip"),
                InlineKeyboardButton("Extract", callback_data="unzip"),
            ],
            [InlineKeyboardButton("UnDoubleZip", callback_data="undzip")],
        ]
    )
    
    # If a task is running, inform user this will be queued
    if BOT.State.task_going:
        queue_notice = f"\n\n⏳ <i>A task is currently running. This will be queued (Position: #{task_queue.pending_count + 1})</i>"
    else:
        queue_notice = ""
    
    await message.reply_text(
        text=f"<b>🐹 Select Type of {PendingTask.mode.capitalize()} You Want » </b>\n\nRegular:<i> Normal file upload</i>\nCompress:<i> Zip file upload</i>\nExtract:<i> extract before upload</i>\nUnDoubleZip:<i> Unzip then compress</i>{queue_notice}",
        reply_markup=keyboard,
        quote=True,
    )



@colab_bot.on_callback_query()
async def handle_options(client, callback_query):
    global BOT, MSG
    from .utility.variables import PendingTask

    if callback_query.data in ["normal", "zip", "unzip", "undzip"]:
        await callback_query.message.delete()
        await colab_bot.delete_messages(
            chat_id=callback_query.message.chat.id,
            message_ids=callback_query.message.reply_to_message_id,
        )
        
        # Check if a task is already running - queue instead of blocking
        if BOT.State.task_going:
            # Add to queue using PendingTask data (not global BOT which is being used by running task)
            task = await task_queue.add_task(
                source=PendingTask.source.copy(),  # Copy to avoid reference issues
                mode=PendingTask.mode,
                task_type=callback_query.data,
                ytdl=PendingTask.ytdl,
                custom_name=PendingTask.custom_name,
                zip_pswd=PendingTask.zip_pswd,
                unzip_pswd=PendingTask.unzip_pswd,
                stream_upload=PendingTask.stream_upload,
                caption_style=PendingTask.caption,
                convert_video=PendingTask.convert_video,
                video_out=PendingTask.video_out
            )
            position = task_queue.get_queue_position(task.task_id)
            await colab_bot.send_message(
                chat_id=OWNER,
                text=f"✅ **Task Queued Successfully!**\n\n"
                     f"📋 Task ID: `{task.task_id}`\n"
                     f"📦 Type: {callback_query.data.capitalize()} {PendingTask.mode.capitalize()}\n"
                     f"📊 Position in queue: #{position}\n\n"
                     f"Your task will start automatically after the current task finishes.\n"
                     f"Use /queue to see all pending tasks",
            )
            BOT.State.started = False
        else:
            # Execute immediately - set task type on global state
            BOT.Mode.type = callback_query.data
            MSG.status_msg = await colab_bot.send_message(
                chat_id=OWNER,
                text="#STARTING_TASK\n\n**Starting your task in a few Seconds...🦐**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Cancel ❌", callback_data="cancel")],
                    ]
                ),
            )
            BOT.State.task_going = True
            BOT.State.started = False
            BotTimes.start_time = datetime.now()
            event_loop = get_event_loop()
            BOT.TASK = event_loop.create_task(taskScheduler())  # type: ignore
            await BOT.TASK
            BOT.State.task_going = False


    elif callback_query.data == "video":
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Split Videos", callback_data="split-true"),
                    InlineKeyboardButton("Zip Videos", callback_data="split-false"),
                ],
                [
                    InlineKeyboardButton("Convert", callback_data="convert-true"),
                    InlineKeyboardButton(
                        "Don't Convert", callback_data="convert-false"
                    ),
                ],
                [
                    InlineKeyboardButton("To » Mp4", callback_data="mp4"),
                    InlineKeyboardButton("To » Mkv", callback_data="mkv"),
                ],
                [
                    InlineKeyboardButton("High Quality", callback_data="q-High"),
                    InlineKeyboardButton("Low Quality", callback_data="q-Low"),
                ],
                [InlineKeyboardButton("Back ⏎", callback_data="back")],
            ]
        )
        await callback_query.message.edit_text(
            f"CHOOSE YOUR DESIRED OPTION ⚙️ »\n\n╭⌬ CONVERT » <code>{BOT.Setting.convert_video}</code>\n├⌬ SPLIT » <code>{BOT.Setting.split_video}</code>\n├⌬ OUTPUT FORMAT » <code>{BOT.Options.video_out}</code>\n╰⌬ OUTPUT QUALITY » <code>{BOT.Setting.convert_quality}</code>",
            reply_markup=keyboard,
        )
    elif callback_query.data == "caption":
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Monospace", callback_data="code-Monospace"),
                    InlineKeyboardButton("Bold", callback_data="b-Bold"),
                ],
                [
                    InlineKeyboardButton("Italic", callback_data="i-Italic"),
                    InlineKeyboardButton("Underlined", callback_data="u-Underlined"),
                ],
                [InlineKeyboardButton("Regular", callback_data="p-Regular")],
            ]
        )
        await callback_query.message.edit_text(
            "CHOOSE YOUR CAPTION FONT STYLE »\n\n⌬ <code>Monospace</code>\n⌬ Regular\n⌬ <b>Bold</b>\n⌬ <i>Italic</i>\n⌬ <u>Underlined</u>",
            reply_markup=keyboard,
        )
    elif callback_query.data == "thumb":
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Delete Thumbnail", callback_data="del-thumb"),
                ],
                [
                    InlineKeyboardButton("Go Back ⏎", callback_data="back"),
                ],
            ]
        )
        thmb_ = "None" if not BOT.Setting.thumbnail else "Exists"
        await callback_query.message.edit_text(
            f"CHOOSE YOUR THUMBNAIL SETTINGS »\n\n⌬ Thumbnail » {thmb_}\n⌬ Send an Image to set as Your Thumbnail",
            reply_markup=keyboard,
        )
    elif callback_query.data == "del-thumb":
        if BOT.Setting.thumbnail:
            os.remove(Paths.THMB_PATH)
        BOT.Setting.thumbnail = False
        await send_settings(
            client, callback_query.message, callback_query.message.id, False
        )
    elif callback_query.data == "set-prefix":
        await callback_query.message.edit_text(
            "Send a Text to Set as PREFIX by REPLYING THIS MESSAGE »"
        )
        BOT.State.prefix = True
    elif callback_query.data == "set-suffix":
        await callback_query.message.edit_text(
            "Send a Text to Set as SUFFIX by REPLYING THIS MESSAGE »"
        )
        BOT.State.suffix = True
    elif callback_query.data in [
        "code-Monospace",
        "p-Regular",
        "b-Bold",
        "i-Italic",
        "u-Underlined",
    ]:
        res = callback_query.data.split("-")
        BOT.Options.caption = res[0]
        BOT.Setting.caption = res[1]
        await send_settings(
            client, callback_query.message, callback_query.message.id, False
        )
    elif callback_query.data in ["split-true", "split-false"]:
        BOT.Options.is_split = True if callback_query.data == "split-true" else False
        BOT.Setting.split_video = (
            "Split Videos" if callback_query.data == "split-true" else "Zip Videos"
        )
        await send_settings(
            client, callback_query.message, callback_query.message.id, False
        )
    elif callback_query.data in [
        "convert-true",
        "convert-false",
        "mp4",
        "mkv",
        "q-High",
        "q-Low",
    ]:
        if callback_query.data in ["convert-true", "convert-false"]:
            BOT.Options.convert_video = (
                True if callback_query.data == "convert-true" else False
            )
            BOT.Setting.convert_video = (
                "Yes" if callback_query.data == "convert-true" else "No"
            )
        elif callback_query.data in ["q-High", "q-Low"]:
            BOT.Setting.convert_quality = callback_query.data.split("-")[-1]
            BOT.Options.convert_quality = (
                True if BOT.Setting.convert_quality == "High" else False
            )
            await send_settings(
                client, callback_query.message, callback_query.message.id, False
            )
        else:
            BOT.Options.video_out = callback_query.data
        await send_settings(
            client, callback_query.message, callback_query.message.id, False
        )
    elif callback_query.data in ["media", "document"]:
        BOT.Options.stream_upload = True if callback_query.data == "media" else False
        BOT.Setting.stream_upload = (
            "Media" if callback_query.data == "media" else "Document"
        )
        await send_settings(
            client, callback_query.message, callback_query.message.id, False
        )

    elif callback_query.data == "close":
        await callback_query.message.delete()
    elif callback_query.data == "back":
        await send_settings(
            client, callback_query.message, callback_query.message.id, False
        )

    # @main Triggering Actual Leech Functions
    elif callback_query.data in ["ytdl-true", "ytdl-false"]:
        ytdl_enabled = True if callback_query.data == "ytdl-true" else False
        await callback_query.message.delete()
        await colab_bot.delete_messages(
            chat_id=callback_query.message.chat.id,
            message_ids=callback_query.message.reply_to_message_id,
        )
        
        # Check if a task is already running - queue instead of blocking
        if BOT.State.task_going:
            # Add to queue using PendingTask data
            task = await task_queue.add_task(
                source=PendingTask.source.copy(),
                mode=PendingTask.mode,
                task_type="normal",  # YTDL tasks are always "normal" type
                ytdl=ytdl_enabled,
                custom_name=PendingTask.custom_name,
                zip_pswd=PendingTask.zip_pswd,
                unzip_pswd=PendingTask.unzip_pswd,
                stream_upload=PendingTask.stream_upload,
                caption_style=PendingTask.caption,
                convert_video=PendingTask.convert_video,
                video_out=PendingTask.video_out
            )
            position = task_queue.get_queue_position(task.task_id)
            await colab_bot.send_message(
                chat_id=OWNER,
                text=f"✅ **Task Queued Successfully!**\n\n"
                     f"📋 Task ID: `{task.task_id}`\n"
                     f"📦 Type: YTDL {PendingTask.mode.capitalize()}\n"
                     f"📊 Position in queue: #{position}\n\n"
                     f"Your task will start automatically after the current task finishes.\n"
                     f"Use /queue to see all pending tasks",
            )
            BOT.State.started = False
        else:
            # Execute immediately - set ytdl mode on global state
            BOT.Mode.ytdl = ytdl_enabled
            MSG.status_msg = await colab_bot.send_message(
                chat_id=OWNER,
                text="#STARTING_TASK\n\n**Starting your task in a few Seconds...🦐**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Cancel ❌", callback_data="cancel")],
                    ]
                ),
            )
            BOT.State.task_going = True
            BOT.State.started = False
            BotTimes.start_time = datetime.now()
            event_loop = get_event_loop()
            BOT.TASK = event_loop.create_task(taskScheduler())  # type: ignore
            await BOT.TASK
            BOT.State.task_going = False

    # If user Wants to Stop The Task
    elif callback_query.data == "cancel":
        await cancelTask("User Cancelled !")
    
    # Cancel task from queue
    elif callback_query.data.startswith("cancel_queue_"):
        task_id = callback_query.data.replace("cancel_queue_", "")
        success, message = await task_queue.cancel_task(task_id)
        if success:
            await callback_query.answer(f"Task {task_id} cancelled!", show_alert=True)
            try:
                await callback_query.message.edit_text(
                    f"#TASK_CANCELLED\n\n**Task ID:** `{task_id}`\n**Status:** Cancelled by user"
                )
            except Exception:
                pass
        else:
            await callback_query.answer(message, show_alert=True)


@colab_bot.on_message(filters.photo & filters.private)
async def handle_image(client, message):
    msg = await message.reply_text("<i>Trying To Save Thumbnail...</i>")
    success = await setThumbnail(message)
    if success:
        await msg.edit_text("**Thumbnail Successfully Changed ✅**")
        await message.delete()
    else:
        await msg.edit_text(
            "🥲 **Couldn't Set Thumbnail, Please Try Again !**", quote=True
        )
    await sleep(15)
    await message_deleter(message, msg)


@colab_bot.on_message(filters.command("setname") & filters.private)
async def custom_name(client, message):
    global BOT
    if len(message.command) != 2:
        msg = await message.reply_text(
            "Send\n/setname <code>custom_fileame.extension</code>\nTo Set Custom File Name 📛",
            quote=True,
        )
    else:
        BOT.Options.custom_name = message.command[1]
        msg = await message.reply_text(
            "Custom Name Has Been Successfully Set !", quote=True
        )

    await sleep(15)
    await message_deleter(message, msg)


@colab_bot.on_message(filters.command("zipaswd") & filters.private)
async def zip_pswd(client, message):
    global BOT
    if len(message.command) != 2:
        msg = await message.reply_text(
            "Send\n/zipaswd <code>password</code>\nTo Set Password for Output Zip File. 🔐",
            quote=True,
        )
    else:
        BOT.Options.zip_pswd = message.command[1]
        msg = await message.reply_text(
            "Zip Password Has Been Successfully Set !", quote=True
        )

    await sleep(15)
    await message_deleter(message, msg)


@colab_bot.on_message(filters.command("unzipaswd") & filters.private)
async def unzip_pswd(client, message):
    global BOT
    if len(message.command) != 2:
        msg = await message.reply_text(
            "Send\n/unzipaswd <code>password</code>\nTo Set Password for Extracting Archives. 🔓",
            quote=True,
        )
    else:
        BOT.Options.unzip_pswd = message.command[1]
        msg = await message.reply_text(
            "Unzip Password Has Been Successfully Set !", quote=True
        )

    await sleep(15)
    await message_deleter(message, msg)


@colab_bot.on_message(filters.command("help") & filters.private)
async def help_command(client, message):
    msg = await message.reply_text(
        "Send /start To Check If I am alive 🤨\n\n"
        "Send /tupload and follow prompts to start transloading 🚀\n\n"
        "Send /settings to edit bot settings ⚙️\n\n"
        "Send /setname To Set Custom File Name 📛\n\n"
        "Send /zipaswd To Set Password For Zip File 🔐\n\n"
        "Send /unzipaswd To Set Password to Extract Archives 🔓\n\n"
        "📋 **Queue Commands:**\n"
        "Send /queue To View Task Queue Status 📊\n"
        "Send /cancel <task_id> To Cancel a Queued Task ❌\n\n"
        "⚠️ **You can ALWAYS SEND an image To Set it as THUMBNAIL for your files 🌄**\n\n"
        "💡 **NEW:** You can now add multiple tasks - they will be queued and processed one by one!",
        quote=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "GitHub Repository ⛏️",
                        url="https://github.com/AdittyaMondal/MiN3R-Colab-Station",
                    ),
                    InlineKeyboardButton(
                        "Channel 📣",
                        url="https://t.me/minerclouds",
                    ),
                ],
            ]
        ),
    )
    await sleep(15)
    await message_deleter(message, msg)


@colab_bot.on_message(filters.command("queue") & filters.private)
async def queue_status(client, message):
    """Display current queue status"""
    if message.chat.id == OWNER:
        await message.delete()
        status = task_queue.get_queue_status()
        msg = await message.reply_text(status)
        await sleep(30)
        await message_deleter(message, msg)


@colab_bot.on_message(filters.command("cancel") & filters.private)
async def cancel_queued_task(client, message):
    """Cancel a specific task by ID"""
    if message.chat.id != OWNER:
        return
    
    await message.delete()
    
    if len(message.command) != 2:
        msg = await message.reply_text(
            "📝 **Usage:** `/cancel <task_id>`\n\n"
            "Use /queue to see task IDs",
            quote=True
        )
        await sleep(15)
        await message_deleter(message, msg)
        return
    
    task_id = message.command[1]
    success, result_message = await task_queue.cancel_task(task_id)
    
    if success:
        msg = await message.reply_text(f"✅ {result_message}")
    else:
        msg = await message.reply_text(f"❌ {result_message}")
    
    await sleep(15)
    await message_deleter(message, msg)


logging.info("⛏️ MiN3R × Colab Station Started !")

# Start the queue worker as a background task
async def start_bot_with_queue():
    """Start bot with queue worker running in background"""
    global _queue_worker_started
    
    async with colab_bot:
        if not _queue_worker_started:
            # Start queue worker in background
            asyncio.create_task(queue_worker())
            _queue_worker_started = True
            logging.info("Queue worker started in background")
        
        # Keep the bot running
        await asyncio.Event().wait()

# Run the bot
colab_bot.run(start_bot_with_queue())

