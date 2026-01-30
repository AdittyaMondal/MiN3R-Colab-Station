# ⛏️ MiN3R × Colab Station | https://github.com/AdittyaMondal/MiN3R-Colab-Station


# @title ⛏️ MiN3R × Colab Station - Main Code

# @title Main Code
# @markdown <div><center><h2>⛏️ MiN3R × Colab Station</h2></center></div>
# @markdown <center><h4><a href="https://github.com/AdittyaMondal/MiN3R-Colab-Station">GitHub Repository</a></h4></center>

# @markdown <br>

API_ID = 0  # @param {type: "integer"}
API_HASH = ""  # @param {type: "string"}
BOT_TOKEN = ""  # @param {type: "string"}
USER_ID = 0  # @param {type: "integer"}
DUMP_ID = 0  # @param {type: "integer"}


import subprocess, time, json, shutil, os
from IPython.display import clear_output
from threading import Thread

Working = True

banner = '''

  ███╗   ███╗██╗███╗   ██╗██████╗ ██████╗ 
  ████╗ ████║██║████╗  ██║╚════██╗██╔══██╗
  ██╔████╔██║██║██╔██╗ ██║ █████╔╝██████╔╝
  ██║╚██╔╝██║██║██║╚██╗██║ ╚═══██╗██╔══██╗
  ██║ ╚═╝ ██║██║██║ ╚████║██████╔╝██║  ██║
  ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝
                                           
      ⛏️ MiN3R × Colab Station ⛏️
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        Cloud Mining & Leeching
                                                 

'''

print(banner)

def Loading():
    white = 37
    black = 0
    while Working:
        print("\r" + "░"*white + "▒▒"+ "▓"*black + "▒▒" + "░"*white, end="")
        black = (black + 2) % 75
        white = (white -1) if white != 0 else 37
        time.sleep(2)
    clear_output()


_Thread = Thread(target=Loading, name="Prepare", args=())
_Thread.start()

if len(str(DUMP_ID)) == 10 and "-100" not in str(DUMP_ID):
    n_dump = "-100" + str(DUMP_ID)
    DUMP_ID = int(n_dump)

if os.path.exists("/content/sample_data"):
    shutil.rmtree("/content/sample_data")

cmd = "git clone https://github.com/AdittyaMondal/MiN3R-Colab-Station"
proc = subprocess.run(cmd, shell=True)
cmd = "apt update && apt install ffmpeg aria2"
proc = subprocess.run(cmd, shell=True)
cmd = "pip3 install -r /content/MiN3R-Colab-Station/requirements.txt"
proc = subprocess.run(cmd, shell=True)

credentials = {
    "API_ID": API_ID,
    "API_HASH": API_HASH,
    "BOT_TOKEN": BOT_TOKEN,
    "USER_ID": USER_ID,
    "DUMP_ID": DUMP_ID,
}

with open('/content/MiN3R-Colab-Station/credentials.json', 'w') as file:
    file.write(json.dumps(credentials))

Working = False

if os.path.exists("/content/MiN3R-Colab-Station/my_bot.session"):
    os.remove("/content/MiN3R-Colab-Station/my_bot.session") # Remove previous bot session
    
print("\rStarting ⛏️ MiN3R × Colab Station....")

os.system("cd /content/MiN3R-Colab-Station/ && python3 -m colab_leecher")

