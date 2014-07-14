# -*- coding:utf-8 -*-
'''
Created on 2013年11月26日

@author: Hyphen.Liu
'''
import xlsxwriter
import os
import globalvar.guiGlobalVar as ggv

headings = ggv.siteInfo

class ExcelWriter():
    '''
    :对电子表格进行写的操作不进行读的操作
    '''
    def __init__(self,filename,worksheetname,lists=[]):
        '''
        :初始化参数
        :param filename:需要保存为的电子表格文件名
        :param worksheetname:表格的名字
        :param lists:传入数据，二维列表
        '''
        self.filename = filename
        self.worksheetname = worksheetname
        self.data = lists
        
        workbook = xlsxwriter.Workbook(self.filename)
        #设置表格属性信息，作者、公司等信息
        workbook.set_properties({'title':u'网站收集查询结果',
                                 'subject':self.worksheetname,
                                 'author':u'Hyphen.Liu(刘海峰)',
                                 'company':'Minzu University of China',
                                 'manager':'Hyphen.Liu',
                                 'comments':'Created with Python and XlsWriter'})
        worksheet = workbook.add_worksheet(self.worksheetname)
        
        #head_format = workbook.add_format({'bold': True,'bg_color':'yellow','font_color':'red'})
        ct_format = workbook.add_format()
        ct_format.set_align('left')
        #ct_format.set_text_wrap()
        #设置列宽
        worksheet.set_column('A1:A2', 6, ct_format)         #序号 0
        worksheet.set_column('B1:B2', 12, ct_format)        #域名 1
        worksheet.set_column('C1:C2', 15, ct_format)        #名称 2
        worksheet.set_column('D1:D2', 18, ct_format)        #首页地址 3
        worksheet.set_column('E1:E2', 12, ct_format)        #单位名称 4
        worksheet.set_column('F1:F2', 10, ct_format)        #单位性质 5
        worksheet.set_column('G1:G2', 10, ct_format)        #审核时间 6
        worksheet.set_column('H1:H2', 18, ct_format)        #备案号 7
        worksheet.set_column('I1:I2', 15, ct_format)        #服务器地址 8
        worksheet.set_column('J1:J2', 20, ct_format)        #服务器位置 9
        worksheet.set_column('K1:K2', 10, ct_format)        #全球排名 10
        worksheet.set_column('L1:L2', 8, ct_format)         #中文排名 11
        worksheet.set_column('M1:M2', 6, ct_format)         #编码12
        worksheet.set_column('N1:N2', 12, ct_format)        #信度 13
        worksheet.set_column('O1:O2', 20, ct_format)        #链接 14
        worksheet.freeze_panes(1, 3)
        #worksheet.write_row('A1', headings, head_format)
        headinglist = []
        for h in headings:
            headinglist.append({'header':h})
        worksheet.add_table('A1:O%d'%(len(self.data)+1), 
                            {'data':self.data, 
                             'columns':headinglist})
        
        #for row, row_data in enumerate(data):
        #    worksheet.write_row(row+1,1,row_data,ct_format)
        
        workbook.close()
