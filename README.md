# 打造任何领域的单词本

本项目实现从英文文献pdf分割单词，自动翻译，输出为有道云的单词本xml格式，可以导入到有道云中进行学习。

可以用在刚入门某一领域，不认识文献中的大多数词汇时，把这些文献中的词汇批处理导入到有道云中进行集中背诵。

之后还可以考虑根据词频等属性得到某一专业的专业词汇，就像有道云中商务词汇等等，如果可以打造任何一个领域的单词本，那是极好的。



## Version

+ **v1.0** date: 2021/01/25 简单实现英文文献pdf转换为有道云xml，可以满足基本要求
+ **v1.1** date: 2021/01/27 增加easy_dict_common.json，包含小学和初一词汇，如果单词在该文件中，则会被去除



## 环境要求

+ 系统：windows10
+ 基于python3.8
+ 需要安装requests包
  `pip install requests==2.25.1 -i https://pypi.tuna.tsinghua.edu.cn/simple`
+ 需要安装pdfminer3k包
  `pip install pdfminer3k -i https://pypi.tuna.tsinghua.edu.cn/simple`



## 使用方法

1. 把想要处理的pdf放入`input`文件夹中，并命名为`input.pdf`
2. 如果不输出翻译（默认不输出），直接运行`mian.py`
3. 如果要输出翻译，需要把`mian.py`文件中的全局变量`OUTPUT_TRANS`赋值为`True`
4. 输出的`xml`文件在`output`中

**注意：** 由于当前从远程获取翻译限制为1000次/天，所以如果pdf中的word超过1000个，只能分多天运行请求翻译（已请求过的会保存在本地词典中，所以分次运行是可行的）；或者把翻译关闭，不输出翻译：把`mian.py`文件中的全局变量`OUTPUT_TRANS`赋值为`False`



## TODO

+ python编程规范  date:2021/01/25
+ 从有道云url每天只能请求1000次，找找其他方法 date:2021/01/25
+ UI界面 date:2021/01/25
+ 去掉更多过于简单的单词，提供更加贴切的领域词汇 date:2021/01/25
+ 把local_dict的单词本分文件储存，一个文件可能太大了 date:2021/01/25
+ 查询单词while循环的超时处理 date:2021/01/25
+ 更新单词本时是否需要考虑'trans'为空的状态？ date:2021/01/25
+ 自动扫描`input`文件夹中所有文件 date:2021/01/26

## DONE
+ 增加easy_dict date:2021/01/25->2021/01/27



