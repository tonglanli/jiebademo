import Image
import sys

im = Image.open(sys.argv[1])
im.save('test.png')