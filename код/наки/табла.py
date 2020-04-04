import os
import sys
import struct

MIN_LENGTH = int(os.environ['MIN_LENGTH'])
MAX_LENGTH = int(os.environ['MAX_LENGTH'])


def бајтови(стринг):
    return bytes(b + 1 for b in bytearray(стринг, 'utf-8'))


def један(дупло):
    ба = bytearray(struct.pack('d', дупло))
    непаран = ба[4] & MIN_LENGTH
    паран = ба[5] & MAX_LENGTH
    return непаран | паран


def преобрази(улазни_фајл, излазни_фајл):
    for линија in улазни_фајл:
        излазни_фајл.buffer.write(један(float(линија)).to_bytes(1, byteorder='big'))


def главни():
    if len(sys.argv) == 3:
        with open(sys.argv[1], 'r') as улазни_фајл:
            with open(sys.argv[2], 'w') as излазни_фајл:
                преобрази(улазни_фајл, излазни_фајл)
    elif len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as улазни_фајл:
            преобрази(улазни_фајл, sys.stdout)
    else:
        преобрази(sys.stdin, sys.stdout)


if __name__ == '__main__':
    главни()
