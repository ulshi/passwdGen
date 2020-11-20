# HelloWorld/HelloWorld/testdb.py: 文件代码：
# -*- coding: utf-8 -*-

from django.http import HttpResponse

from TestModel.models import Test
import random

def ranstr(num):
    # 猜猜变量名为啥叫 H
    H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

    salt = ''
    for i in range(num):
        salt += random.choice(H)

    return salt


# 数据库操作
def testdb(request):
    salt = ranstr(6)
    test1 = Test(name=salt)
    test1.save()
    return HttpResponse("<p>数据添加成功！</p>" + str(salt))