import re
import pyvi 
from pyvi import ViTokenizer


print(ViTokenizer.tokenize(u"ngôn ngữ học ngữ liệu"))

'''
path = './train/Train_gold.txt'
f = open(path, 'r', encoding="utf8")
data = f.read()
vocab = data.replace("_ ", " ").split()

output_path = './Train_gold.txt'
op_txt = open(output_path, 'w', encoding='utf8')
for word in vocab:
    op_txt.write("{} ".format(word))
    '''