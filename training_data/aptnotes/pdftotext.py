import chardet
import sys
import textract

filename = sys.argv[1]
text = textract.process(filename)
encoding = chardet.detect(text)['encoding']
print(text.decode(encoding))
