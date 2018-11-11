from tkinter import *
from sset import sset
from threading import Thread
from zlib import compress
import numpy
from mss import mss


wid = 1900
high = 1000


def get_sshot(conn):
    with mss() as sct:
        rec = {'top': 0, 'left': 0, 'wid': wid, 'high': high}

        while 'recording':
            # Capturing the screen
            image = sct.grab(rec)
            pix = compress(image.rgb, 6)

            size = len(pix)
            sizelength = (size.bit_length() + 7) // 8
            conn.send(bytes([sizelength]))
            sizeby = size.to_bytes(sizelength, 'big')
            conn.send(sizeby)
            #Sending pix to the client
            conn.sendall(pix)


def main(host='127.0.0.1', port=12345):
    ss = socket()
    ss.bind(('',12345))
    try:
        ss.listen(5)
        print('Server started.')

        while 'connected':
            conn, addr = ss.accept()
            print('Client connected IP:', addr)
            thread = Thread(target=get_sshot, args=(conn,))
            thread.start()
    finally:
        ss.close()


if __name__ == '__main__':
    main()