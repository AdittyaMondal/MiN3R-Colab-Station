<div align="center">

# ⛏️ MiN3R × Colab Station

### *Ultimate File Transfer & Cloud Mining Bot for Telegram*

[![License](https://img.shields.io/badge/License-GPL--3.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://core.telegram.org/bots)
[![Channel](https://img.shields.io/badge/Channel-minerclouds-blue.svg)](https://t.me/minerclouds)
[![GitHub](https://img.shields.io/badge/GitHub-AdittyaMondal-black.svg)](https://github.com/AdittyaMondal/MiN3R-Colab-Station)

**A powerful Pyrogram-based Telegram bot that seamlessly transfers files between multiple sources and destinations with advanced automation features**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Credits](#-credits)

</div>

---

## ✨ Features

### 🎯 Core Capabilities
- **Multi-Source Downloads** - Support for direct links, Google Drive, Telegram, and 2000+ video sites
- **Intelligent Upload** - Automatic upload to Telegram or Google Drive with smart splitting
- **Task Management** - Add multiple tasks anytime during execution with queue system 🔥
- **Video Processing** - Convert videos to MP4/MKV with custom settings
- **Archive Handling** - Extract multi-part archives of all formats automatically
- **Custom Thumbnails** - Auto-generate or set custom thumbnails for videos

### 🛠️ Advanced Features
- **Smart File Naming** - Custom file naming with pattern support
- **Task Queue System** - Queue multiple downloads and process them efficiently
- **Restricted Content** - Access restricted Telegram content (Beta)
- **Auto-Splitting** - Intelligent file splitting for 2GB/4GB limits
- **Compression** - Zip folders/files before upload
- **Real-time Progress** - Live progress tracking with ETA

### 🔗 Supported Sources
| Source Type | Status | Notes |
|-------------|--------|-------|
| Direct Links | ✅ | HTTP/HTTPS downloads |
| Google Drive | ✅ | Auto-authentication |
| Telegram Files | ✅ | Including restricted content |
| YouTube & Video Sites | ✅ | 2000+ supported platforms |
| Mega.nz | ✅ | Full support |
| Terabox | ✅ | Supported |
| Torrents/Magnets | ⚠️ | Use with caution (Colab policy) |

---

## 🚀 Quick Start

### Deploy in 3 Easy Steps

<div align="center">

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/YOUR_NOTEBOOK_LINK_HERE?usp=sharing)

</div>

1. **Click the badge above** to open the notebook
2. **Configure your settings** (API_ID, API_HASH, BOT_TOKEN, etc.)
3. **Run the bot** and start transferring!

---

## 💎 Why Choose MiN3R × Colab Station?

<table>
<tr>
<td width="50%">

### ⚡ Performance
- **200 MB/s** download speed
- **30 MB/s** upload speed
- Google's blazing-fast infrastructure

</td>
<td width="50%">

### 💰 Cost-Effective
- No VPS/RDP needed
- Free Google Colab tier
- Unlimited Telegram storage

</td>
</tr>
<tr>
<td width="50%">

### 🎛️ Flexibility
- Upload files up to 2GB (4GB premium)
- ~84GB temporary storage
- Multiple concurrent tasks with queue

</td>
<td width="50%">

### 🔒 Security
- OAuth 2.0 for Google Drive
- Secure Telegram API
- No data retention

</td>
</tr>
</table>

---

## 🎮 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Initialize the bot |
| `/tupload` | Upload files to Telegram |
| `/gdupload` | Upload files to Google Drive |
| `/ytupload` | Download from YouTube and upload |
| `/settings` | Configure bot preferences |
| `/queue` | View task queue status |
| `/cancel <id>` | Cancel a specific queued task |
| `/help` | Show all available commands |

---

## ⚙️ Configuration

```python
# Required Configuration
API_ID = "your_api_id"
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"
USER_ID = your_telegram_user_id
DUMP_ID = your_dump_channel_id
```

---

## ⚠️ Important Notes

### Google Colab Policy Compliance

This tool is designed for **personal, interactive use** within Google Colab's acceptable use policy:

- ✅ **Allowed**: Personal file management, format conversion, legitimate backups
- ❌ **Prohibited**: Bulk downloads, copyright infringement, torrent abuse
- ⚠️ **Caution**: Respect content ownership and licensing

> **Disclaimer**: Downloading copyrighted content without permission may violate laws in your jurisdiction. Use responsibly and at your own risk.

### Known Limitations

- 🔄 **Runtime Disconnections**: Colab may disconnect after prolonged inactivity
- 💾 **Storage Limits**: ~84GB in free tier (varies)
- ⏱️ **Session Duration**: Free tier has usage limits

---

## 🛣️ Roadmap

- [x] Multi-task queue system
- [x] Python 3.12+ compatibility
- [ ] Advanced video processing options
- [ ] Custom plugins system
- [ ] Web UI dashboard

---

## 🙏 Credits

<div align="center">

### Original Project

This project is a **customized and rebranded version** built upon the excellent work of:

**[Telegram-Leecher](https://github.com/XronTrix10/Telegram-Leecher)** by **[XronTrix10](https://github.com/XronTrix10)**

</div>

A huge thank you to **XronTrix10** for creating and sharing the original **Telegram-Leecher** project! This project would not be possible without their incredible foundation and contribution to the open-source community.

### Enhancements in MiN3R × Colab Station

| Enhancement | Description |
|-------------|-------------|
| 🔧 Event Loop Fix | Fixed Python 3.12+ compatibility issues |
| 📋 Task Queue System | Add multiple tasks while one is running |
| 🎨 Rebranding | Custom branding and UI improvements |
| 📖 Documentation | Extended documentation and guides |

---

## 📄 License

This project is licensed under the [GPL-3.0 License](LICENSE) - see the LICENSE file for details.

As per the GPL-3.0 license, this project maintains all original licensing terms and provides proper attribution to the original author.

---

## 🌟 Star History

If this project helped you, please consider giving it a star! ⭐

Your support motivates us to keep improving and adding new features.

---

<div align="center">

### 💝 Pull Requests Welcome!

We welcome contributions! Feel free to submit PRs for bug fixes or new features.

---

**⛏️ MiN3R × Colab Station**

*Built with ❤️ for the Telegram community*

*Based on [Telegram-Leecher](https://github.com/XronTrix10/Telegram-Leecher) by [XronTrix10](https://github.com/XronTrix10)*

</div>