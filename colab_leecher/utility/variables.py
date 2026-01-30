# ⛏️ MiN3R × Colab Station | https://github.com/AdittyaMondal/MiN3R-Colab-Station


from time import time
from datetime import datetime
from pyrogram.types import Message


class BOT:
    SOURCE = []
    TASK = None
    class Setting:
        stream_upload = "Media"
        convert_video = "Yes"
        convert_quality = "Low"
        caption = "Monospace"
        split_video = "Split Videos"
        prefix = ""
        suffix = ""
        thumbnail = False

    class Options:
        stream_upload = True
        convert_video = True
        convert_quality = False
        is_split = True
        caption = "code"
        video_out = "mp4"
        custom_name = ""
        zip_pswd = ""
        unzip_pswd = ""

    class Mode:
        mode = "leech"
        type = "normal"
        ytdl = False

    class State:
        started = False
        task_going = False
        prefix = False
        suffix = False


# Temporary storage for pending task data (before user selects task type)
# This prevents overwriting running task's global state
# Use a dictionary with getter/setter to ensure data isolation between queued tasks
class PendingTask:
    _data = {}
    
    @classmethod
    def set(cls, source, mode, ytdl, custom_name, zip_pswd, unzip_pswd, 
            stream_upload, caption, convert_video, video_out):
        """Store pending task data - makes a copy of source list to avoid reference issues"""
        cls._data = {
            "source": source.copy() if isinstance(source, list) else [source],
            "mode": mode,
            "ytdl": ytdl,
            "custom_name": custom_name,
            "zip_pswd": zip_pswd,
            "unzip_pswd": unzip_pswd,
            "stream_upload": stream_upload,
            "caption": caption,
            "convert_video": convert_video,
            "video_out": video_out
        }
    
    @classmethod
    def get(cls):
        """Get a copy of pending task data"""
        return cls._data.copy()
    
    @classmethod
    def get_source(cls):
        """Get a copy of the source list"""
        return cls._data.get("source", []).copy()
    
    @classmethod
    def get_value(cls, key, default=None):
        """Get a specific value from pending task data"""
        return cls._data.get(key, default)
    
    @classmethod
    def clear(cls):
        """Clear pending task data after it's been queued"""
        cls._data = {}


class YTDL:
    header = ""
    speed = ""
    percentage = 0.0
    eta = ""
    done = ""
    left = ""


class Transfer:
    down_bytes = []  # Empty list - values get appended during processing
    up_bytes = []    # Empty list - values get appended during upload
    total_down_size = 0
    sent_file = []
    sent_file_names = []


class TaskError:
    state = False
    text = ""


class BotTimes:
    current_time = time()
    start_time = datetime.now()
    task_start = datetime.now()


class Paths:
    WORK_PATH = "/content/MiN3R-Colab-Station/BOT_WORK"
    THMB_PATH = "/content/MiN3R-Colab-Station/colab_leecher/Thumbnail.jpg"
    VIDEO_FRAME = f"{WORK_PATH}/video_frame.jpg"
    HERO_IMAGE = f"{WORK_PATH}/Hero.jpg"
    DEFAULT_HERO =  "/content/MiN3R-Colab-Station/colab_leecher/Thumbnail.jpg"
    MOUNTED_DRIVE = "/content/drive"
    down_path = f"{WORK_PATH}/Downloads"
    temp_dirleech_path = f"{WORK_PATH}/dir_leech_temp"
    mirror_dir = "/content/drive/MyDrive/MiN3R Colab Uploads"
    temp_zpath = f"{WORK_PATH}/Leeched_Files"
    temp_unzip_path = f"{WORK_PATH}/Unzipped_Files"
    temp_files_dir = f"{WORK_PATH}/leech_temp"
    thumbnail_ytdl = f"{WORK_PATH}/ytdl_thumbnails"
    access_token = "/content/token.pickle"


class Messages:
    caution_msg = "\n\n<i>💖 When I'm Doin This, Do Something Else ! <b>Because, Time Is Precious ✨</b></i>"
    download_name = ""
    task_msg = ""
    status_head = f"<b>📥 DOWNLOADING » </b>\n"
    dump_task = ""
    src_link = ""
    link_p = ""


class MSG:
    sent_msg = Message(id=1)
    status_msg = Message(id=2)



class Aria2c:
    link_info = False
    pic_dwn_url = "https://picsum.photos/900/600"


class Gdrive:
    service = None
