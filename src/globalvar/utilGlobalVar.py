# -*- coding:utf-8 -*-
'''
Created on 2013年11月8日

@author: Hyphen.Liu
'''

mtrPath = '../../material/'
DATAPATH = '../../data/'
URLTEMPF = '-temp-url-dict.txt'                             #暂存获取到的url链接，文件里的保存格式是分离后的url地址
OUTURLTEMPF = '-temp-outurl-dict.txt'                       #暂存获取到的网站广度扫描url链接，文件里的保存格式是分离后的url地址
ENGURLTEMPF = '-temp-engurl.txt'                            #暂存已经确认为搜索语言的网站链接
DBNAME = 'minorwebsites.db'                                 #数据库名字
boCoding = ['latin', 'gbk', 'unicode']
mnCoding = ['fz', 'gbk', 'unicode']
# 蒙古文字符集编码范围
mnCode1 = [u'\u1800', u'\u18AF']
mnCode2 = [u'\uE236', u'\uE377']
mnCode = [mnCode1, mnCode2]
# 藏文字符集编码范围
boCode1 = [u'\u0F00', u'\u0FFF']                            #unicode编码范围1
boCode2 = [u'\uF300', u'\uF8FF']                            #unicode编码范围2
boCode3 = [u'\u7E5E', u'\u7F53']
boCodety = [u'\u7E71', u'\u7E71', u'\u7E72', u'\u7E72', u'\u7E73', u'\u7E73', u'\u7E74', 
            u'\u7E74', u'\u7E75', u'\u7E75', u'\u7E76', u'\u7E76', u'\u7E77', u'\u7E77', 
            u'\u7E78', u'\u7E78', u'\u7E79', u'\u7E79', u'\u7E7A', u'\u7E7A', u'\u7E7B', 
            u'\u7E7B', u'\u7E7C', u'\u7E7C', u'\u7E7D', u'\u7E7D', u'\u7E7E', u'\u7E7E', 
            u'\u7E7F', u'\u7E7F', u'\u7E80', u'\u7E80', u'\u7E81', u'\u7E81', u'\u7E83', 
            u'\u7E84', u'\u7E84', u'\u7E85', u'\u7E86', u'\u7E86', u'\u7E87', u'\u7E87', 
            u'\u7E88', u'\u7E88', u'\u7E89', u'\u7E89', u'\u7E8A', u'\u7E8A', u'\u7E8B', 
            u'\u7E8B', u'\u7E8C', u'\u7E8C', u'\u7E8D', u'\u7E8D', u'\u7E8E', u'\u7E8F', 
            u'\u7E8F', u'\u7F51', u'\u7F51', u'\u7F5C', u'\u7F5C', u'\u7F5E', u'\u7F63', 
            u'\u7F63', u'\u7F64', u'\u7F64', u'\u7F65', u'\u7F65', u'\u7F66', u'\u7F67', 
            u'\u7F67', u'\u7F6B', u'\u7F6B', u'\u7F6F', u'\u7F6F', u'\u7F76', u'\u7F76', 
            u'\u7F77', u'\u7F78', u'\u7F78', u'\u7F7A', u'\u7F7A', u'\u7F7B', u'\u7F7B', 
            u'\u7F7D', u'\u7F7D', u'\u7F7F', u'\u7F80', u'\u7F80', u'\u7F81', u'\u7F82', 
            u'\u7F83', u'\u7F83', u'\u7F84', u'\u7F84', u'\u7F85', u'\u7F85', u'\u7F86', 
            u'\u7F86', u'\u7F87', u'\u7F87', u'\u7F88', u'\u7F88', u'\u7F89', u'\u7F89', 
            u'\u7F8B', u'\u7F8B', u'\u7F8D', u'\u7F8D', u'\u7F8F', u'\u7F8F', u'\u7F91', 
            u'\u7F92', u'\u7F92', u'\u7F93', u'\u7F93', u'\u7F95', u'\u7F95', u'\u7F96', 
            u'\u7F96', u'\u7F97', u'\u7F97', u'\u7F98', u'\u7F99', u'\u7F99', u'\u7F9B', 
            u'\u7F9B', u'\u7F9C', u'\u7F9C', u'\u7FA0', u'\u7FA0', u'\u7FA2', u'\u7FA2', 
            u'\u7FA8', u'\u7FA9', u'\u7FA9', u'\u7FAB', u'\u7FAB', u'\u7FAD', u'\u7FE7', 
            u'\u7FEC', u'\u7FEC', u'\u7FED', u'\u7FED', u'\u7FEF', u'\u7FEF', u'\u7FF2', 
            u'\u7FF2', u'\u7FF4', u'\u7FF4', u'\u7FF5', u'\u7FF8', u'\u7FF9', u'\u7FF9', 
            u'\u7FFD', u'\u7FFD', u'\u7FFE', u'\u7FFE', u'\u7FFF', u'\u7FFF', u'\u8002', 
            u'\u8002', u'\u8007', u'\u8007', u'\u8008', u'\u8009', u'\u8009', u'\u8011', 
            u'\u8011', u'\u801F', u'\u801F', u'\u8021', u'\u8021', u'\u8023', u'\u8023', 
            u'\u8024', u'\u802B', u'\u802B', u'\u802C', u'\u802C', u'\u802D', u'\u802D', 
            u'\u802F', u'\u8032', u'\u8032', u'\u8034', u'\u8034', u'\u803A', u'\u803A', 
            u'\u803E', u'\u8040', u'\u8040', u'\u8041', u'\u8044', u'\u804F', u'\u8050', 
            u'\u8053', u'\u8053', u'\u8055', u'\u8056', u'\u8056', u'\u807E', u'\u807E', 
            u'\u808A', u'\u808D', u'\u808D', u'\u808E', u'\u808E', u'\u808F', u'\u808F', 
            u'\u8090', u'\u8090', u'\u8091', u'\u8092', u'\u8095', u'\u80A7', u'\u80A7', 
            u'\u80B3', u'\u80B5', u'\u80B5', u'\u80B9', u'\u80BB', u'\u80D0', u'\u80D0', 
            u'\u80D1', u'\u80D1', u'\u80DF', u'\u80E0', u'\u80E0', u'\u80E6', u'\u80FE', 
            u'\u8100', u'\u8100', u'\u8101', u'\u8103', u'\u8104', u'\u8105', u'\u8105', 
            u'\u810B', u'\u810B', u'\u8140', u'\u8140', u'\u8141', u'\u8142', u'\u8142', 
            u'\u8147', u'\u8147', u'\u815D', u'\u816A', u'\u816A', u'\u816F', u'\u816F', 
            u'\u8175', u'\u8175', u'\u8176', u'\u8177', u'\u8177', u'\u8178', u'\u8178', 
            u'\u8186', u'\u818E', u'\u8190', u'\u8195', u'\u8195', u'\u8196', u'\u8196', 
            u'\u81A0', u'\u81B5', u'\u81B5', u'\u81D7', u'\u81D7', u'\u81D8', u'\u81D8', 
            u'\u81D9', u'\u81DA', u'\u81DB', u'\u81DB', u'\u81DC', u'\u81DC', u'\u81DD', 
            u'\u81DE', u'\u81DE', u'\u81DF', u'\u81DF', u'\u81E4', u'\u81E4', u'\u81E5', 
            u'\u81E5', u'\u81E6', u'\u81E6', u'\u81E8', u'\u81E9', u'\u81E9', u'\u81EB', 
            u'\u81EB', u'\u81EE', u'\u81EE', u'\u81F0', u'\u81F0', u'\u81F1', u'\u81F1', 
            u'\u81F2', u'\u81F2', u'\u81F5', u'\u81F5', u'\u81F6', u'\u81F6', u'\u81F7', 
            u'\u81F9', u'\u81FD', u'\u81FF', u'\u81FF', u'\u8203', u'\u8203', u'\u8207', 
            u'\u8207', u'\u8208', u'\u8208', u'\u8209', u'\u8209', u'\u820A', u'\u820A', 
            u'\u820B', u'\u820B', u'\u820E', u'\u820E', u'\u8217', u'\u8217', u'\u8218', 
            u'\u8218', u'\u8219', u'\u8219', u'\u821A', u'\u821A', u'\u821D', u'\u8220', 
            u'\u8220', u'\u8225', u'\u8226', u'\u8226', u'\u8227', u'\u822E', u'\u823A', 
            u'\u823D', u'\u823D', u'\u85CF', u'\u85CF', u'\u8CED', u'\u8CEE', u'\u8CEE', 
            u'\u8D00', u'\u8D00', u'\u8D01', u'\u8D02', u'\u8D02', u'\u8D03', u'\u8D09', 
            u'\u8D09', u'\u8D0C', u'\u8D0C', u'\u8D0E', u'\u8D0F', u'\u8D0F', u'\u8D10', 
            u'\u8D12', u'\u8D12', u'\u8D14', u'\u8D15', u'\u8D18', u'\u8D1A', u'\u8D1C', 
            u'\u8E96', u'\u8EC7', u'\u8ED4', u'\u8ED4', u'\u8ED6', u'\u8ED7', u'\u8ED8', 
            u'\u8ED8', u'\u8EDB', u'\u8EDB', u'\u8EDE', u'\u8EDF', u'\u8EDF', u'\u8EE0', 
            u'\u8EE0', u'\u8EE1', u'\u8EE1', u'\u8EE2', u'\u8EE2', u'\u8EE4', u'\u8EE4', 
            u'\u8EE6', u'\u8EE6', u'\u8EE7', u'\u8EE7', u'\u8EEC', u'\u8EF1', u'\u8EF2', 
            u'\u8EF3', u'\u8EF3', u'\u8EF4', u'\u8EF4', u'\u8EF6', u'\u8EF6', u'\u8EF7', 
            u'\u8EF7', u'\u8EF8', u'\u8EF8', u'\u8EF9', u'\u8EF9', u'\u8EFA', u'\u8EFA', 
            u'\u8EFB', u'\u8EFB', u'\u8F01', u'\u8F02', u'\u8F02', u'\u8F03', u'\u8F03', 
            u'\u8F04', u'\u8F04', u'\u8F05', u'\u8F05', u'\u8F06', u'\u8F06', u'\u8F07', 
            u'\u8F07', u'\u8F08', u'\u8F09', u'\u8F0A', u'\u8F0A', u'\u8F0C', u'\u8F0C', 
            u'\u8F0E', u'\u8F10', u'\u8F13', u'\u8F14', u'\u8F14', u'\u8F15', u'\u8F15', 
            u'\u8F16', u'\u8F16', u'\u8F17', u'\u8F17', u'\u8F18', u'\u8F18', u'\u8F19', 
            u'\u8F19', u'\u8F1A', u'\u8F1A', u'\u8F1B', u'\u8F1C', u'\u8F1C', u'\u8F1D', 
            u'\u8F1D', u'\u8F1E', u'\u8F1E', u'\u8F1F', u'\u8F1F', u'\u8F20', u'\u8F20', 
            u'\u8F21', u'\u8F21', u'\u8F23', u'\u8F23', u'\u8F25', u'\u8F25', u'\u8F26', 
            u'\u8F26', u'\u8F27', u'\u8F27', u'\u8F28', u'\u8F28', u'\u8F29', u'\u8F29', 
            u'\u8F2A', u'\u8F2A', u'\u8F2B', u'\u8F2B', u'\u8F2C', u'\u8F2C', u'\u8F2D', 
            u'\u8F2D', u'\u8F32', u'\u8F32', u'\u8F33', u'\u8F34', u'\u8F35', u'\u8F35', 
            u'\u8F36', u'\u8F38', u'\u8F38', u'\u8F39', u'\u8F39', u'\u8F3F', u'\u8F3F', 
            u'\u8F40', u'\u8F40', u'\u8F41', u'\u8F41', u'\u8F42', u'\u8F43', u'\u8F43', 
            u'\u8F44', u'\u8F44', u'\u8F45', u'\u8F45', u'\u8F46', u'\u8F46', u'\u8F47', 
            u'\u8F47', u'\u8F48', u'\u8F48', u'\u8F49', u'\u8F4B', u'\u8F4B', u'\u8F4D', 
            u'\u8F4F', u'\u8F53', u'\u8F54', u'\u8F56', u'\u8F58', u'\u8F58', u'\u8F5A', 
            u'\u8F5A', u'\u8F5C', u'\u8F5C', u'\u8F5E', u'\u8F5E', u'\u8F5F', u'\u8F5F', 
            u'\u8F60', u'\u8F60', u'\u8F64', u'\u8FB4', u'\u8FB5', u'\u8FCF', u'\u8FCF', 
            u'\uFE3D', u'\uFE40']
boCodebz = [u'\u886C', u'\u6382', u'\u5DEE', u'\u556A', u'\u7B7E', u'\u541B', u'\u8FEA', 
            u'\u7248', u'\u5C94', u'\u540A', u'\u7840', u'\u573A', u'\u8FAB', u'\u7C27', 
            u'\u508D', u'\u94B5', u'\u51A0', u'\u4E01', u'\u4E32', u'\u4E58', u'\u4EBA', 
            u'\u4ECE', u'\u4ED3', u'\u4EE3', u'\u4F20', u'\u4F2F', u'\u4F34', u'\u4F43', 
            u'\u4F46', u'\u4F70', u'\u4F97', u'\u4FA7', u'\u4FAF', u'\u4FBF', u'\u4FDD', 
            u'\u4FFA', u'\u5012', u'\u5021', u'\u507F', u'\u50A8', u'\u5145', u'\u5151', 
            u'\u515A', u'\u5175', u'\u5178', u'\u5185', u'\u518C', u'\u51AC', u'\u51B2', 
            u'\u51BB', u'\u51CB', u'\u51F3', u'\u5200', u'\u5201', u'\u521B', u'\u521D', 
            u'\u529E', u'\u5317', u'\u5319', u'\u534A', u'\u5355', u'\u535C', u'\u535E', 
            u'\u5382', u'\u53A8', u'\u53C9', u'\u53D8', u'\u53EE', u'\u53FC', u'\u540E', 
            u'\u5427', u'\u5435', u'\u5439', u'\u5446', u'\u5448', u'\u54C4', u'\u5507', 
            u'\u5530', u'\u5531', u'\u5598', u'\u56F1', u'\u5730', u'\u575D', u'\u5782', 
            u'\u57AB', u'\u57CE', u'\u5821', u'\u58C1', u'\u5907', u'\u5927', u'\u5939', 
            u'\u5954', u'\u5A6A', u'\u5AE1', u'\u5B58', u'\u5B9A', u'\u5B9D', u'\u5BC4', 
            u'\u5C1D', u'\u5C42', u'\u5C9B', u'\u5CB8', u'\u5CFB', u'\u5D14', u'\u5DDD', 
            u'\u5DE2', u'\u5E03', u'\u5E1B', u'\u5E1D', u'\u5E2E', u'\u5E87', u'\u5E8A', 
            u'\u5E95', u'\u5EA6', u'\u5F0A', u'\u5F1B', u'\u5F1F', u'\u5F53', u'\u5F69', 
            u'\u5F6A', u'\u5F6C', u'\u5F7B', u'\u5F7C', u'\u5F85', u'\u5F97', u'\u5FC5', 
            u'\u5FF1', u'\u606B', u'\u60B2', u'\u60E8', u'\u60E9', u'\u60ED', u'\u60EE', 
            u'\u618B', u'\u61C2', u'\u6210', u'\u6233', u'\u6234', u'\u6241', u'\u624D', 
            u'\u6253', u'\u626E', u'\u626F', u'\u6273', u'\u628A', u'\u62B5', u'\u62C6', 
            u'\u62CC', u'\u62CD', u'\u62D2', u'\u62DC', u'\u6321', u'\u6355', u'\u6363', 
            u'\u6376', u'\u6389', u'\u63A3', u'\u63B8', u'\u63BA', u'\u63D2', u'\u63E3', 
            u'\u640F', u'\u642C', u'\u642D', u'\u643D', u'\u6446', u'\u6448', u'\u6467', 
            u'\u64A4', u'\u64E6', u'\u654C', u'\u655D', u'\u655E', u'\u658C', u'\u6591', 
            u'\u65A5', u'\u65E6', u'\u6602', u'\u660C', u'\u6625', u'\u6668', u'\u66F9', 
            u'\u676F', u'\u677F', u'\u67B7', u'\u67C4', u'\u67CF', u'\u67E5', u'\u67F4', 
            u'\u6807', u'\u680B', u'\u6863', u'\u6886', u'\u693D', u'\u693F', u'\u695A', 
            u'\u69FD', u'\u6A0A', u'\u6A59', u'\u6A71', u'\u6B8B', u'\u6BBF', u'\u6BD4', 
            u'\u6BD5', u'\u6C60', u'\u6C89', u'\u6CCA', u'\u6CE2', u'\u6CF5', u'\u6D1E', 
            u'\u6D5A', u'\u6DA4', u'\u6DE1', u'\u6DEC', u'\u6DF3', u'\u6EC7', u'\u6F88', 
            u'\u6FB3', u'\u706F', u'\u707F', u'\u708A', u'\u7092', u'\u70B9', u'\u70BD', 
            u'\u7238', u'\u725B', u'\u72C4', u'\u72EC', u'\u73ED', u'\u74E3', u'\u7535', 
            u'\u7545', u'\u7574', u'\u75AE', u'\u75F9', u'\u7601', u'\u762A', u'\u767B', 
            u'\u767D', u'\u767E', u'\u7684', u'\u76D7', u'\u776C', u'\u7779', u'\u77AA', 
            u'\u77D7', u'\u7889', u'\u7898', u'\u78A7', u'\u78B4', u'\u78CB', u'\u7977', 
            u'\u79E4', u'\u7A17', u'\u7A3B', u'\u7A7F', u'\u7A97', u'\u7B06', u'\u7B14', 
            u'\u7B1B', u'\u7B2C', u'\u7B49', u'\u7B79', u'\u7BE1', u'\u7C97', u'\u7CB9', 
            u'\u7CD9', u'\u7E73', u'\u7E74', u'\u7E7B', u'\u7E7D', u'\u7E7F', u'\u7E80', 
            u'\u7E8D', u'\u7EAF', u'\u7EAF', u'\u7EAF', u'\u7ECA', u'\u7EF0', u'\u7F14', 
            u'\u7F16', u'\u7F20', u'\u7F62', u'\u7F8C', u'\u7FDF', u'\u7FE0', u'\u8019',
            u'\u8021', u'\u803B', u'\u80A0', u'\u80AF', u'\u80C6', u'\u80CC', u'\u8106', 
            u'\u8116', u'\u818A', u'\u8198', u'\u81C2', u'\u822C', u'\u8231', u'\u8236', 
            u'\u8239', u'\u82CD', u'\u8327', u'\u8336', u'\u8361', u'\u83E0', u'\u8482', 
            u'\u84D6', u'\u866B', u'\u8695', u'\u8776', u'\u8822', u'\u8868', u'\u89E6', 
            u'\u8BE7', u'\u8C03', u'\u8C79', u'\u8C7A', u'\u8D22', u'\u8D25', u'\u8D2C', 
            u'\u8D81', u'\u8D85', u'\u8E29', u'\u8E48', u'\u8E6C', u'\u8E6D', u'\u8E7F', 
            u'\u8E87', u'\u8F66', u'\u8F86', u'\u8F9F', u'\u8FA8', u'\u8FA9', u'\u8FB0', 
            u'\u8FB1', u'\u8FB9', u'\u8FF8', u'\u9017', u'\u904D', u'\u9053', u'\u907F', 
            u'\u9093', u'\u90A6', u'\u90F4', u'\u90F8', u'\u9119', u'\u9187', u'\u91C7', 
            u'\u9493', u'\u9504', u'\u9524', u'\u952D', u'\u957F', u'\u95ED', u'\u95EF', 
            u'\u9610', u'\u965B', u'\u9661', u'\u96CC', u'\u96CF', u'\u96D5', u'\u96F9', 
            u'\u9738', u'\u975B', u'\u97AD', u'\u9881', u'\u98A4', u'\u9910', u'\u9971', 
            u'\u9A73', u'\u9C8D', u'\u9CD6', u'\u9F3B', u'\uFE3D', u'\uFE40']
boCode = [boCode1, boCode2,boCodety,boCodebz]
# 维吾尔文、柯尔克孜文、哈萨克文字符集编码范围
ugCode = [u'\u062E', u'\u063A', u'\u0698', u'\uFB8A', u'\uFB8B',  u'\uFEA5', u'\uFEA6', 
          u'\uFEA7', u'\uFEA8', u'\uFECD', u'\uFECE', u'\uFECF', u'\uFED0']
ugcCode = [u'\u0626\u06D5', u'\u0626\u0648', u'\u0626\u06C7', u'\u0626\u06C6', u'\u0626\u06C8', 
           u'\u0626\u06D0', u'\u0626\u0649']
kkCode = [u'\u0674', u'\u0675', u'\u0676', u'\u0677', u'\u0678', u'\u067E', u'\uFBD9', 
          u'\uFBDA', u'\uFBDD', u'\uFEEE']
kyCode = [u'\u06C5', u'\u06C9', u'\uFBE0', u'\uFBE1', u'\uFBE2', u'\uFBE3', u'\uFBF8', 
          u'\uFE89', u'\uFE8A', u'\uFE8B', u'\uFE8C', u'\uFEEF']
arCode = [u'\u0620', u'\u0622', u'\u0623', u'\u0624', u'\u0625', u'\u062B', u'\u0630', 
          u'\u0636', u'\u0637', u'\u0638', u'\u063B', u'\u063C', u'\u063D', u'\u063E', 
          u'\u063F', u'\u0647', u'\u064B', u'\u064C', u'\u064D', u'\u064E', u'\u064F']
totalCode = [u'\u00AB', u'\u00BB', u'\u060C', u'\u061B', u'\u061F', u'\u0621', u'\u0625', 
             u'\u0626', u'\u0627', u'\u0628', u'\u062A', u'\u062C', u'\u062D', u'\u062E', 
             u'\u062F', u'\u0631', u'\u0632', u'\u0633', u'\u0634', u'\u0639', u'\u063A', 
             u'\u0640', u'\u0641', u'\u0642', u'\u0643', u'\u0644', u'\u0645', u'\u0646', 
             u'\u0648', u'\u0649', u'\u064A', u'\u0674', u'\u0675', u'\u0676', u'\u0677', 
             u'\u0678', u'\u067E', u'\u0686', u'\u0698', u'\u06AD', u'\u06AF', u'\u06BE', 
             u'\u06C5', u'\u06C6', u'\u06C7', u'\u06C8', u'\u06C9', u'\u06CB', u'\u06D0', 
             u'\u06D5', u'\uFB56', u'\uFB57', u'\uFB58', u'\uFB59', u'\uFB7A', u'\uFB7B', 
             u'\uFB7C', u'\uFB7D', u'\uFB8A', u'\uFB8B', u'\uFB92', u'\uFB93', u'\uFB94', 
             u'\uFB95', u'\uFBAA', u'\uFBAB', u'\uFBAC', u'\uFBAD', u'\uFBD3', u'\uFBD4', 
             u'\uFBD5', u'\uFBD6', u'\uFBD7', u'\uFBD8', u'\uFBD9', u'\uFBDA', u'\uFBDB', 
             u'\uFBDC', u'\uFBDD', u'\uFBDE', u'\uFBDF', u'\uFBE0', u'\uFBE1', u'\uFBE2', 
             u'\uFBE3', u'\uFBE4', u'\uFBE5', u'\uFBE6', u'\uFBE7', u'\uFBE8', u'\uFBE9', 
             u'\uFBEA', u'\uFBEB', u'\uFBEC', u'\uFBED', u'\uFBEE', u'\uFBEF', u'\uFBF0', 
             u'\uFBF1', u'\uFBF2', u'\uFBF3', u'\uFBF4', u'\uFBF5', u'\uFBF6', u'\uFBF7', 
             u'\uFBF9', u'\uFBFA', u'\uFBFB', u'\uFE89', u'\uFE8A', u'\uFE8B', u'\uFE8C', 
             u'\uFE8D', u'\uFE8E', u'\uFE8F', u'\uFE90', u'\uFE91', u'\uFE92', u'\uFE95', 
             u'\uFE96', u'\uFE97', u'\uFE98', u'\uFE9D', u'\uFE9E', u'\uFE9F', u'\uFEA0', 
             u'\uFEA1', u'\uFEA2', u'\uFEA3', u'\uFEA4', u'\uFEA5', u'\uFEA6', u'\uFEA7', 
             u'\uFEA8', u'\uFEA9', u'\uFEAA', u'\uFEAD', u'\uFEAE', u'\uFEAF', u'\uFEB0', 
             u'\uFEB1', u'\uFEB2', u'\uFEB3', u'\uFEB4', u'\uFEB5', u'\uFEB6', u'\uFEB7', 
             u'\uFEB8', u'\uFEC9', u'\uFECA', u'\uFECB', u'\uFECC', u'\uFECD', u'\uFECE', 
             u'\uFECF', u'\uFED0', u'\uFED1', u'\uFED2', u'\uFED3', u'\uFED4', u'\uFED5', 
             u'\uFED6', u'\uFED7', u'\uFED8', u'\uFED9', u'\uFEDA', u'\uFEDB', u'\uFEDC', 
             u'\uFEDD', u'\uFEDE', u'\uFEDF', u'\uFEE0', u'\uFEE1', u'\uFEE2', u'\uFEE3', 
             u'\uFEE4', u'\uFEE5', u'\uFEE6', u'\uFEE7', u'\uFEE8', u'\uFEE9', u'\uFEEA', 
             u'\uFEED', u'\uFEEE', u'\uFEEF', u'\uFEF0', u'\uFEF1', u'\uFEF2', u'\uFEF3', 
             u'\uFEF4', u'\uFEFB', u'\uFEFC']
ugkkCode = [u'\u06BE', u'\u06C6', u'\uFBAA', u'\uFBAB', u'\uFBAC', u'\uFBAD', u'\uFBD7', 
            u'\uFBD9', u'\uFBDA', u'\uFE8E', u'\uFEED', u'\uFEEE']
ugkyCode = [u'\u0626', u'\u0649', u'\uFBE8', u'\uFE8B', u'\uFE8C', u'\uFEEF']
kkkyCode = [u'\u0627', u'\u062D', u'\u0639', u'\u0648', u'\u06C7', u'\u06D5', u'\uFBD7', 
            u'\uFBE9', u'\uFE8D', u'\uFE8E', u'\uFEA1', u'\uFEA2', u'\uFEA3', u'\uFEA4', 
            u'\uFEC9', u'\uFECA', u'\uFECB', u'\uFECC', u'\uFEE9', u'\uFEEA', u'\uFEED', 
            u'\uFEEE', u'\FEF0']
sameCode = [u'\u00AB', u'\u00BB', u'\u060C', u'\u061B', u'\u061F', u'\u0621', u'\u0628', 
            u'\u062A', u'\u062C', u'\u062F', u'\u0631', u'\u0632', u'\u0633', u'\u0634', 
            u'\u0641', u'\u0642', u'\u0643', u'\u0644', u'\u0645', u'\u0646', u'\u064A', 
            u'\u067E', u'\u0685', u'\u06AD', u'\u06AF', u'\u06CB', u'\uFB56', u'\uFB57', 
            u'\uFB58', u'\uFB59', u'\uFB7A', u'\uFB7B', u'\uFB7C', u'\uFB7D', u'\uFB92', 
            u'\uFB93', u'\uFB94', u'\uFB95', u'\uFBD3', u'\uFBD4', u'\uFBD5', u'\uFBD6', 
            u'\uFBD8', u'\uFBDE', u'\uFBDF', u'\uFBE9', u'\uFE8D', u'\uFE8F', u'\uFE90', 
            u'\uFE91', u'\uFE92', u'\uFE95', u'\uFE96', u'\uFE97', u'\uFE98', u'\uFE9D', 
            u'\uFE9E', u'\uFE9F', u'\uFEA0', u'\uFEA9', u'\uFEAA', u'\uFEAD', u'\uFEAE', 
            u'\uFEAF', u'\uFEB0', u'\uFEB1', u'\uFEB2', u'\uFEB3', u'\uFEB4', u'\uFEB5', 
            u'\uFEB6', u'\uFEB7', u'\uFEB8', u'\uFED1', u'\uFED2', u'\uFED3', u'\uFED4', 
            u'\uFED5', u'\uFED6', u'\uFED7', u'\uFED8', u'\uFED9', u'\uFEDA', u'\uFEDB', 
            u'\uFEDC', u'\uFEDD', u'\uFEDE', u'\uFEDF', u'\uFEE0', u'\uFEE1', u'\uFEE2', 
            u'\uFEE3', u'\uFEE4', u'\uFEE5', u'\uFEE6', u'\uFEE7', u'\uFEE8', u'\uFEF1', 
            u'\uFEF2', u'\uFEF3', u'\uFEF4', u'\uFEFB', u'\uFEFC']
# 朝鲜文字符集编码范围
koCode1 = [u'\u3130', u'\u318F']
koCode2 = [u'\uAC00', u'\uD7AF']
koCode = [koCode1, koCode2]
iiCode = [u'\uA000', u'\uA4CF']                             # 彝文字符集编码范围
tlCode = [u'\u1950', u'\u19DF']                             # 傣文字符集编码范围
# 各种标点符号的编码范围
punct1 = [u'\u0020', u'\u0040']
punct2 = [u'\u005B', u'\u005F']
punct3 = [u'\u007B', u'\u007E']
punct4 = [u'\u00A0', u'\u00BB']
punct5 = [u'\u2010', u'\u203C']
punct6 = [u'\u2460', u'\u2473']
punct7 = [u'\u3008', u'\u301F']
punct8 = [u'\uFF01', u'\uFF20']
puctuation = [punct1, punct2, punct3, punct4, punct5, punct6, punct7, punct8]