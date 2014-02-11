import Image
from pytesseract import image_to_string
#print image_to_string(Image.open('/Users/mac/github/python-tesseract/pytesseract/test.png'))
#im = Image.open('/Users/mac/NLTK/jiebademo/jiebademo/test.png')
#im = im.convert('RGB')
#im.save('/Users/mac/NLTK/jiebademo/jiebademo/test.png')
print image_to_string(Image.open('/Users/mac/NLTK/jiebademo/jiebademo/2.png'), lang='chi_sim')

