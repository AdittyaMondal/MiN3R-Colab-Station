# ⛏️ MiN3R × Colab Station - Instructions

## 🤖 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Check if I am Online 📲 |
| `/tupload` | Upload files to telegram 🏎️ |
| `/gdupload` | Upload files to google drive ☁️ |
| `/drupload` | Upload files from a local directory / folder 📂 |
| `/ytupload` | Upload ytdl link files (YouTube, etc.) 🐞 |
| `/settings` | Edit Bot Settings ⚙ |
| `/setname` | Set Custom File Name 📛 |
| `/zipaswd` | Set Password for Archiving 🔐 |
| `/unzipaswd` | Set Password for Extracting Archives 🔓 |
| `/queue` | **NEW!** View Task Queue Status 📊 |
| `/cancel` | Cancel a running task or queue item ❌ |
| `/help` | Get details about how to use Me 🧐 |

> ⚠️ **NOTE:** Bot will only work in private chat.

---

## ⚙️ About The Credentials

*   **API_ID**: Your Telegram API ID. [Get it here](https://my.telegram.org/apps).
*   **API_HASH**: Your Telegram API HASH. [Get it here](https://my.telegram.org/apps).
*   **BOT_TOKEN**: Create a Telegram Bot from [@BotFather](https://t.me/BotFather), then paste the Bot Token.
*   **USER_ID**: Your Own Telegram User ID. Retrievable from [@userinfobot](https://t.me/userinfobot).
*   **DUMP_ID**: Create a Channel / Group, Add Your Bot There, Then Get The Chat ID of That Channel. Make Sure The ID Starts with `-100`.

---

## 💥 Additional Tutorial

### Send Links To Bot

**For Single Link:**
```
https://filehost.com/file.mp4
```

**For Multiple Links (Bulk):**
```
https://filehost.com/file1.mp4
https://filehost.com/file2.mp4
https://filehost.com/file3.mp4
```
*Just put links in new lines, and that's it!*

**For providing passwords and custom names:**
```
https://filehost.com/file1.mp4
https://filehost.com/file2.mp4
[Custom name space.mp4]
{Password for zipping}
(Password for unzip)
```
*They should be put after links and in same order (if required).*

### Download Telegram Files
1.  Forward The File In Your Dump Channel / Group.
2.  Copy Link of The Forwarded File.
3.  Use The Copied Link As Download Link.

### Upload Directly From Drive (Dir-Leech)
1.  Mount Drive Using The Mount Cell in Colab.
2.  Expand the Folders Using File Explorer.
3.  Copy path of The Folder That You Want To upload.
4.  Use The Copied Path As The Source Link.

### Set Thumbnail For Telegram Files
*   After Starting the Bot, Send an **image** to it. It will automatically set the Thumbnail for future uploads.
*   This uses the default internal branding until you set a new one.

### Multi Part Archive Extract
*   Just Send links of all parts and select **Unzip Mode**. That's it.

### Task Queue (New Feature)
*   You can now add tasks even if the bot is busy!
*   Send a new link while a task is running, and it will be added to the queue.
*   Use `/queue` to see pending tasks.
*   Use `/cancel <task_id>` to remove a specific task from the queue.
