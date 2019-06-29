import cv2
import socket
import subprocess
import numpy

width = 1280
height = 720
server = socket.socket()
server.bind(('0.0.0.0', 8000))
server.listen(0)

connection = server.accept()[0].makefile('rb')
try:

    command = ["ffmpeg", '-i', '-', '-pix_fmt', 'bgr24',
    '-vcodec', 'rawvideo', '-an', '-sn', '-f', 'image2pipe', '-']

    pipe = subprocess.Popen(command, stdin=connection, stdout=subprocess.PIPE, bufsize=10**8)

    while True:

        raw = pipe.stdout.read(height*width*3)

        image = numpy.frombuffer(raw, dtype='uint8')
        image = image.reshape((height, width,3))

        if image is not None:
            cv2.imshow('Video', image)
            pass
            # Put processing heres

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        pipe.stdout.flush()

    # When everything is done, release the capture
    video.release()
    cv2.destroyAllWindows()

finally:
    connection.close()
    server.close()


