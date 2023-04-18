'''
@Author: 洪建
@Date 2023/1/4 14:17
'''

'''
文档转换工具
'''

import office

def word_conversion_pdf():
    '''
    wor转pdf
    '''
    path = '../data'
    office.word.docx2pdf(path=path)

