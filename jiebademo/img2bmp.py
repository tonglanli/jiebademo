from PIL import Image
file_in = "test1.png"
img = Image.open(file_in)
file_out = "test.bmp"
img.save(file_out)