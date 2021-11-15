#!/usr/bin/env python
#-*- coding:utf-8 -*-

#author:maxiunan
from decimal import *
import pyexcel as p
import pymysql
import os
from pyexcel.cookbook import merge_all_to_a_book
import glob

class DbHandler:

    def __init__(self,host,port,user,password,database,charset,**kwargs):

        self.conn = pymysql.connect(host=host,port=port,user=user,password=password,database=database,
                                    cursorclass=pymysql.cursors.DictCursor,charset=charset,**kwargs)

        self.cursor = self.conn.cursor()


    def query(self,sql,args=None,one=True):
        numbers = self.cursor.execute(sql,args)
        # print(numbers)
        self.conn.commit()
        if one:
            return self.cursor.fetchone()
        else:
            return  self.cursor.fetchall()

    def showResult(self,datalist):
        for data in datalist:
            print(data)

    def save_data(self,datalist):
        p.save_as(records=datalist,dest_file_name='result40.xlsx')
    #     # p.get_book()
    #     p.save_book_as(bookdict = a_dictionary_of_two_dimensional_arrays,dest_file_name = "book.xls")

    def close(self):
        self.cursor.close()
        self.conn.close()

def result_paidType():
    # 支付方式分别统计
    cash_num = 0
    cash_sum = 0.00
    zhifubao_num = 0
    zhifubao_sum = 0.00
    wx_num = 0
    wx_sum = 0.00
    card_num = 0
    card_sum = 0.00

    for i in range(1,11):
        # sql = "select count(*) as co,sum(realincome_amount) as sum_cont ,paid_type_id=1 as '现金',paid_type_id=3 as '支付宝',paid_type_id=12 as '银行卡',paid_type_id=4 as '微信' from trade.2019_trading_fuelling_pay_order_" + str(i) + " where substring(CREATEd_time,1,10)='2021-11-13' and station_id  in (select station_id from erp_station.station where IS_NORMAL=0) and pay_status=1 and paid_type_id in(1,3,4) and vol<5000 and hq_id not in('16548', '16586', '16843', '16777') GROUP BY paid_type_id ;"
        sql = "select count(*) as co,sum(realincome_amount) as sum_cont ,paid_type_id=1 as '现金',paid_type_id=3 as '支付宝',paid_type_id=12 as '银行卡',paid_type_id=4 as '微信' from trade.2019_trading_fuelling_pay_order_" + str(i) + " where substring(CREATEd_time,1,10)='2021-11-07'  and pay_status=1 and paid_type_id in(1,3,4) and vol<5000 and hq_id not in('16548', '16586', '16843', '16777') GROUP BY paid_type_id ;"
        datalist = db.query(sql, one=False)
        for it in datalist:
            print(i)
            print(it)
            # print(it)
            if (it[u'现金'] == 1):
                cash_num = cash_num + it['co']
                cash_sum = Decimal(str(cash_sum)) + it['sum_cont']

            if (it[u'支付宝'] == 1):
                zhifubao_num = zhifubao_num + it['co']
                zhifubao_sum = Decimal(str(zhifubao_sum)) + it['sum_cont']

            if (it[u'微信'] == 1):
                wx_num = wx_num + it['co']
                wx_sum = Decimal(str(wx_sum)) + it['sum_cont']

            if (it[u'银行卡'] == 1):
                card_num = card_num + it['co']
                card_sum = Decimal(str(card_sum)) + it['sum_cont']

        if not os.path.exists(".\\paitype_result1"):
            os.makedirs(".\\paitype_result1")
        p.save_as(records=datalist, dest_file_name='.\\paitype_result1\\newpaidType' + str(i) + '.xlsx')
    print("现金：" + "%s,%s" % (cash_num, cash_sum))
    print("支付宝：" + "%s,%s" % (zhifubao_num, zhifubao_sum))
    print("微信：" + "%s,%s" % (wx_num, wx_sum))
    print("银行卡" + "%s,%s" % (card_num, card_sum))

    with open("data.txt", "a+") as f:
        f.write("\n\n现金：" + "%s,%s"  %(cash_num, cash_sum))
        f.write("\n支付宝：" + "%s,%s" % (zhifubao_num, zhifubao_sum))
        f.write("\n微信：" + "%s,%s" % (wx_num, wx_sum))
        f.write(("\n银行卡" + "%s,%s" % (card_num, card_sum)))


if __name__=="__main__":
    # gasoline_count = 0
    # gasoline_vol = 0.00
    # gasoline_sum = 0.00
    #
    # diesel_count = 0
    # diesel_vol = 0.00
    # diesel_sum = 0.00
    #
    #
    # a_dictionary_of_two_dimensional_arrays = {}
    # dict12= {}
    # list2 = []
    # for i in range(1,41):
    #     # print(i)
    #     list2.append(str(i))
    #
    #
    # a_dictionary_of_two_dimensional_arrays = dict12.fromkeys(list2, [])
    #
    #
    #
    db = DbHandler(host='rr-bp1t44218cx95mpeb3o.mysql.rds.aliyuncs.com',port=3306,user='yzg',password='RaiN1q2w3e4r5t',database='trade',charset='utf8')
    result_paidType()
    # for i in range(1,11):
    #     sql = "select count(*) as co ,sum(vol) as vo ,sum(realincome_amount) as sum_cont ,RIGHT(PR_NAME,2)='汽油' as '汽油',RIGHT(PR_NAME,2)='柴油' as'柴油' from trade.2019_trading_fuelling_pay_order_"+str(i) +" where substring(CREATEd_time,1,10)='2021-11-13' and pay_status=1  and station_id  in (select station_id from erp_station.station where IS_NORMAL=0) and hq_id not in('16548', '16586', '16843', '16777') GROUP BY RIGHT(PR_NAME,2) ;"
    #
    #     datalist = db.query(sql,one=False)
    # # db.save_data(datalist)
    #     for it in datalist:
    #         # print(it)
    #         if(it[u'汽油']==1):
    #             gasoline_count = gasoline_count + it['co']
    #             gasoline_vol = Decimal(str(gasoline_vol)) + it['vo']
    #             gasoline_sum = Decimal(str(gasoline_sum)) + it['sum_cont']
    #         else:
    #             if(it[u'柴油']==1):
    #                 diesel_count = Decimal(str(diesel_count)) + it['co']
    #                 diesel_vol = Decimal(str(diesel_vol)) + it['vo']
    #                 diesel_sum = Decimal(str(diesel_sum)) + it['sum_cont']
    #         #     gasoline_count =
    #     if not os.path.exists(".\\newresult1"):
    #         os.makedirs(".\\newresult1")
    #     p.save_as(records=datalist, dest_file_name='.\\newresult1\\newoil'+str(i)+'.xlsx')
    # print("汽油：" + "笔数为%s,升数为%s,总价为%s" % (gasoline_count, gasoline_vol, gasoline_sum))
    # print("柴油：" + "%s,%s,%s" % (diesel_count, diesel_vol, diesel_sum))
    # with open("data.txt","a+") as f:
    #     f.write("汽油：" + "%s,%s,%s\n" % (gasoline_count, gasoline_vol, gasoline_sum))
    #     f.write("柴油：" + "%s,%s,%s\n\n" % (diesel_count, diesel_vol, diesel_sum))



    # merge_all_to_a_book(glob.glob(r"D:\Users\ASUS\PycharmProjects\\apiTest\\result\*.*"), "oil.xlsx")
    #
    # a_dictionary_of_two_dimensional_arrays['1'].extend(datalist)
    #
    # p.save_book_as(bookdict = a_dictionary_of_two_dimensional_arrays,dest_file_name = "ebook.xlsx")

    db.close()
