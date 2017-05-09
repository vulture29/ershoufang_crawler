import threading
import os
def restartTor():
        os.system("""(echo authenticate '"mypassword"'; echo signal newnym; echo quit) | nc localhost 9051""")
        global t
        t = threading.Timer(60.0, restartTor)
        t.start()

t = threading.Timer(5.0, restartTor)
t.start()

