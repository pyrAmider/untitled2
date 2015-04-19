#!\python34 python

import os
import sys

sys.stderr.write(('Bad!' * 8) + '\n')

print('Bad!' * 8, file=sys.stderr)

x = 1; y = 2
print(x, y)

sys.stdout.write(str(x) + " " + str(y) + '\n')

print(x, y, file=open('temp1.txt', 'w'))

open('temp2.txt', 'w').write(str(x) + " " + str(y) + '\n')

print(open('temp1.txt', 'r').readline())

print(open('temp2.txt', 'r').readline())

P = os.popen('dir')
print(P.__next__())
P.__next__()
next(P)