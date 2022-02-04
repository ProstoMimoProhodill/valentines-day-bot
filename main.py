import threading
from deanon_bot import main as deanon_bot
from anon_bot import main as anon_bot

if __name__ == '__main__':
    a = threading.Thread(target=anon_bot)
    d = threading.Thread(target=deanon_bot)

    a.start()
    d.start()
