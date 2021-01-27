from io import StringIO
from io import open
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, process_pdf

import sys, os
import requests # 翻译用
import json

class FileToWord(): # 用来处理一切文件，得到word_list
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file

    def split(self):
        with open(self.pdf_file, "rb") as pdf:
            # resource manager
            rsrcmgr = PDFResourceManager()
            retstr = StringIO()
            laparams = LAParams()
            # device
            device = TextConverter(rsrcmgr, retstr, laparams=laparams)
            process_pdf(rsrcmgr, device, pdf)
            device.close()
            content = retstr.getvalue()
            retstr.close()
            # 获取所有单词
            word_list = str(content).split() # 默认按“空格”和“换行”分割

        return word_list

class WordListProcess(): # 用来处理word_list，简化去重等
    def __init__(self, easy_dict_json):
        with open(easy_dict_json, 'r', encoding='utf-8') as f:
            self.easy_dict = json.load(f)

    def simply_word_list(self, word_list):

        if len(word_list) > sys.maxsize:
            raise "lenth of lines out of range" 

        # 去除word里的特殊字符
        special_char = {'"', '(', ')', '\'', ',', '，','“','”', '.','‘','’', ';', ':', '?'}
        for i in range(len(word_list)-1,-1,-1):
            for s in special_char:
                word_list[i] = word_list[i].replace(s, '')

        delete_list = list() # 被删除的word，看看是否符合要求
        # 涉及删除元素，使用倒序遍历
        for i in range(len(word_list)-1,-1,-1):
            if not self._is_word(word_list[i]): 
                pop_word = word_list.pop(i)
                delete_list.append(pop_word)
            elif word_list[i] in self.easy_dict:
                pop_word = word_list.pop(i)
                delete_list.append(pop_word)                

        return word_list, delete_list

    def _is_word(self, word):
        
        MIN_WORD_LEN = 4
        if len(word) < MIN_WORD_LEN: # 长度过短
            return False

        for char in word: #  not('A'~'Z' or 'a'~'z') and 
            if ( not((char >= 'A' and char <= 'Z') or (char >= 'a' and char <= 'z')) 
                and (char != '-') ):   
                return False

        return True

    def analyze_frequency(self, word_list):
        import collections
        dic = collections.Counter(word_list) # 统计
        dic= sorted(dic.items(), key=lambda d:d[1], reverse = True)
        print(dic)

class Translator(): # 翻译word
    def __init__(self):
        self.query_cnt = 0
        pass

    def translate_from_outside(self, word):
        url = "http://fanyi.youdao.com/translate"
        data = {
            'doctype': 'json',
            'type':    'AUTO',
            'i':       "word"
        }

        data['i'] = word
        r = requests.get(url,params=data)
        try:
            result = r.json()['translateResult']
            trans = result[0][0]['tgt']
            self.query_cnt = self.query_cnt + 1
            print(f'已从url查询{self.query_cnt}次')
        except (json.decoder.JSONDecodeError):
            print('请求过于频繁，有道API一天只能1000次')
            trans = None

        return trans
        
    def translate_a_word(self, word, local_dict=None, update_dict=False):
        trans = None
        if (local_dict != None) and (word in local_dict):
            trans = local_dict[word]['trans']
        else:
            while trans == None:
                trans = self.translate_from_outside(word)
                if trans != None and update_dict == True:
                    local_dict.update({word :{'trans': trans}})

        return trans

class WordDict(): # 字典加载及更新
    def __init__(self, json_file):
        self.json_file = json_file
        self.my_dict = dict()
        with open(self.json_file, 'r', encoding='utf-8') as f:
            self.my_dict = json.load(f)
    
    def save_dict(self, new_dict):
        with open(self.json_file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(new_dict, indent=4, ensure_ascii=False))

    def get_dict(self):
        return self.my_dict

class WordXml():
    def __init__(self, xml_file):
        self.xml_file = xml_file

    def output_xml(self, word_todo, output_trans=False, book_name='book1'):
        with open(self.xml_file,'w', encoding='utf-8') as f:
            f.write('<wordbook>')
            for word in word_todo:
                f.write('<item>')
                f.write('    <word>' + word + '</word>\n')
                if output_trans == True:
                    f.write('    <trans>' + '<![CDATA[' + word_todo[word]['trans'] + ']]>' + '</trans>\n')
                f.write('    <tags>'+ book_name +'</tags>\n') 
                f.write('    <progress>1</progress>\n')
                f.write('</item>')
            f.write('</wordbook>')


DEBUG = True
translate_word_num = 1000
OUTPUT_TRANS = True # 是否输出翻译

if __name__ == '__main__':
    abs_path = os.path.dirname(__file__)  #返回当前文件所在的目录
    FileToWord = FileToWord(abs_path + '\\input\\input.pdf')
    word_list = FileToWord.split()

    WordListProcess = WordListProcess(abs_path + '\\locat_dict\\easy_dict_common.json')
    word_list, delete_list = WordListProcess.simply_word_list(word_list)
    
    WordDict = WordDict(abs_path + '\\locat_dict\\robot_dict.json')
    Translator = Translator()

    word_todo = dict()
    for word in word_list:
        if OUTPUT_TRANS == True:
            trans = Translator.translate_a_word(word, local_dict=WordDict.get_dict(), update_dict=True)
        else:
            trans = ''
        word_todo.update({word :{'trans': trans}})
        if DEBUG and translate_word_num:
            translate_word_num = translate_word_num - 1
            if not translate_word_num:
                break

    WordDict.save_dict(WordDict.my_dict)

    WordXml = WordXml(abs_path + '\\output\\output.xml')
    WordXml.output_xml(word_todo, output_trans=OUTPUT_TRANS, book_name='robot_todo')
