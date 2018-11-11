from sset import sset
import numpy
from zlib import decompress
import pygame

wid = 1900
high = 1000


def recpix(conn, length):
    #Retreiving all the pix

    binb = b''
    while len(binb) < length:
        #okay
        dat = conn.recv(length - len(binb))
        if not dat:
            return dat
        binb += dat
    return binb

#write IP address of the scrn you want to cast on your laptop
def main(host='127.0.0.1', port=12345):
    pygame.init()
    scrn = pygame.display.set_mode((wid, high))
    clk = pygame.time.clk()
    watch = True    

    ss = socket()
    ss.connect((host, port))
    try:
        while watch:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    watch = False
                    break

            
            sizelength = int.from_bytes(ss.recv(1), byteorder='big')
            size = int.from_bytes(ss.recv(sizelength), byteorder='big')
            pix = decompress(recpix(ss, size))

            
            img = pygame.image.fromstring(pix, (wid, high), 'RGB')

            
            scrn.blit(img, (0, 0))
            pygame.display.flip()
            clk.tick(20)
    finally:
        ss.close()


if __name__ == '__main__':
    main()