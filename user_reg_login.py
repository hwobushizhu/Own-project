#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql
import re
import urllib.parse
import urllib.request
import random
import sys


def check_user_name(user_name):
    '''
    函数功能：校验用户名是否合法
    函数参数：
    user_name 待校验的用户名
    返回值：校验通过返回0，校验失败返回非零（格式错误返回1，用户名已存在返回2）
    '''
    # [a-zA-Z0-9_]{6, 15}
    if not re.match("^[a-zA-Z0-9_]{6,15}$", user_name):
        return 1

    # 连接数据库，conn为Connection对象
    conn = pymysql.connect('47.103.50.75', 'wy', '123456', 'mydb')

    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            # 执行任意支持的SQL语句
            cur.execute("select uname from user where uname=%s", (user_name,))
            # 通过游标获取执行结果
            rows = cur.fetchone()
    finally:
        # 关闭数据库连接
        conn.close()

    if rows:
        return 2

    return 0


def check_uname_pwd(user_name, password):
    '''
    函数功能：校验用户名和密码是否合法
    函数参数：
    user_name 待校验的用户名
    password 待校验的密码
    返回值：校验通过返回0，校验失败返回1
    '''
    # 连接数据库，conn为Connection对象
    conn = pymysql.connect('47.103.50.75', 'wy', '123456', 'mydb')

    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            # 执行任意支持的SQL语句
            cur.execute("select uname from user where uname=%s and passwd=password(%s)", (user_name, password))
            # 通过游标获取执行结果
            rows = cur.fetchone()
    finally:
        # 关闭数据库连接
        conn.close()

    if rows:
        return 0

    return 1


def check_password(password):
    '''
    函数功能：校验用户密码是否合法
    函数参数：
    password 待校验的密码
    返回值：校验通过返回0，校验错误返回非零（密码太长或太短返回1，密码安全强度太低返回2）
    '''

    return 0


def check_phone(phone):
    '''
    函数功能：校验手机号格式是否合法
    函数参数：
    phone 待校验的手机号
    返回值：校验通过返回0，校验错误返回1
    '''

    if re.match("^1\d{10}$", phone):
        return 0

    return 1


def send_sms_code(phone):
    '''
    函数功能：发送短信验证码（6位随机数字）
    函数参数：
    phone 接收短信验证码的手机号
    返回值：发送成功返回验证码，失败返回False
    '''
    verify_code = str(random.randint(100000, 999999))

    try:
        url = "http://v.juhe.cn/sms/send"
        params = {
            "mobile": phone,  # 接受短信的用户手机号码
            "tpl_id": "",  # 您申请的短信模板ID，根据实际情况修改
            "tpl_value": "#code#=%s" % verify_code,  # 您设置的模板变量，根据实际情况修改
            "key": "75e6a08c7261612b0a3ab25e1676109f",  # 应用APPKEY(应用详细页查询)
        }
        params = urllib.parse.urlencode(params).encode()

        f = urllib.request.urlopen(url, params)
        content = f.read()
        res = json.loads(content)

        if res and res['error_code'] == 0:
            return verify_code
        else:
            return False
    except:
        return False


def send_email_code(email):
    '''
    函数功能：发送邮箱验证码（6位随机数字）
    函数参数：
    email 接收验证码的邮箱
    返回值：发送成功返回验证码，失败返回False
    '''
    verify_code = str(random.randint(100000, 999999))

    # ...

    return verify_code


def user_reg(uname, password, phone, email):
    '''
    函数功能：将用户注册信息写入数据库
    函数描述：
    uname 用户名
    password 密码
    phone 手机号
    email 邮箱
    返回值：成功返回True，失败返回False
    '''
    # 连接数据库，conn为Connection对象
    conn = pymysql.connect('47.103.50.75', 'wy', '123456', 'mydb')

    try:
        with conn.cursor() as cur:  # 获取一个游标对象(Cursor类)，用于执行SQL语句
            # 执行任意支持的SQL语句
            cur.execute("insert into user (uname, passwd, phone, email) values (%s, password(%s), %s, %s)",
                        (uname, password, phone, email))
            r = cur.rowcount
            conn.commit()
    finally:
        # 关闭数据库连接
        conn.close()

    return bool(r)


def reg_main():
    while True:
        user_name = input("请输入用户名（只能包含英文字母、数字或下划线，最短6位，最长15位）：")

        ret = check_user_name(user_name)

        if ret == 0:
            break
        elif ret == 1:
            print("用户名格式错误，请重新输入！")
        elif ret == 2:
            print("用户名已存在，请重新输入！")

    while True:
        while True:
            password = input("请输入密码：")

            ret = check_password(password)

            if ret == 0:
                break
            elif ret == 1:
                print("密码不符合长度要求，请重新输入！")
            elif ret == 2:
                print("密码太简单，请重新输入！")

        confirm_pass = input("请再次输入密码：")

        if password == confirm_pass:
            break
        else:
            print("两次输入的密码不一致，请重新输入！")

    while True:
        phone = input("请输入手机号：")

        if check_phone(phone):
            print("手机号输入错误，请重新输入！")
        else:
            break

    verify_code = send_sms_code(phone)

    if verify_code:
        print("短信验证码已发送！")
    else:
        print("短信验证码发送失败，请检查网络连接或联系软件开发商！")
        sys.exit(1)

    while True:
        verify_code2 = input("请输入短信验证码：")

        if verify_code2 != verify_code:
            print("短信验证码输入错误，请重新输入！")
        else:
            break

    email = input("请输入邮箱：")

    # 校验邮箱的合法性
    # ...

    if user_reg(user_name, password, phone, email):
        print("注册成功！")
    else:
        print("注册失败！")


def login_main():
    '''
    函数功能：用户登录验证
    函数参数：无
    返回值：登录验证成功返回用户名，失败返回False
    '''
    while True:
        user_name = input("\n用户名：")
        ret = check_user_name(user_name)
        if ret == 0:
            print("用户名不存在，请重新输入！")
        elif ret == 1:
            print("用户名格式错误，请重新输入！")
        else:
            break

    while True:
        password = input("\n密码：")
        ret = check_password(password)
        if ret == 0:
            break
        else:
            print("密码格式错误，请重新输入！")

    if check_uname_pwd(user_name, password):
        return False
    return user_name





def user_center(user_name):
    print("%s，欢迎你使用本系统！" % user_name)
    print("\n操作提示：")
    print("1：盘点库存")
    print("2：查看销售额")
    print("3：修改个人密码")
    print("0：退出")

    while True:
        op = input("\n>：")

        if op == "0":
            print("感谢你的使用，下次再见！")
            sys.exit(2)
        elif op == "1":
            # 定义仓库
            repository = dict()
            # 定义购物清单对象
            shop_list = []
            # 定义仓库里商品数量
            shangpin = [
                ["1000001", "疯狂python讲义", 69.0, 12], \
                ["1000002", "疯狂Android讲义", 108.0, 100], \
                ["1000003", "世界起源", 77.0, 122], \
                ["1000004", "香肠", 66, 5]]

            # 定义一个函数来初始化商品
            def init_repository():
                # 遍历商品生成仓库dict字典
                for i in range(len(shangpin)):
                    repository[shangpin[i][0]] = shangpin[i]

            # 显示超市的商品清单，就是遍历代表仓库的dict字典
            def show_goods():
                print("欢迎来到 哼嘿哈嘿乐园")
                print('哈嘿乐园的商品清单:')
                print("%13s%40s%10s%10s" % ("条码", "商品名称", "单价", "数量"))
                # 遍历repository的所有value来显示商品清单
                for s in repository.values():
                    s = tuple(s)
                    print("%15s%40s%12s%12s" % s)

            # 显示购物清单，就是遍历代表购物清单的list列表
            def show_list():
                print("=" * 100)
                # 如果清单不为空的时候，输出清单的内容
                if not shop_list:
                    print("还未购买商品")
                else:
                    title = "%-5s|%15s|%40s|%10s|%4s|%10s" % \
                            ("ID", "条码", "商品名称", "单价", "数量", "小计")
                    print(title)
                    print("-" * 100)
                    # 记录总计的价钱
                    sum = 0
                    # 遍历代表购物清单的list列表
                    for i, item in enumerate(shop_list, start=1):
                        # 转换id为索引加1
                        id = i
                        # 获取该购物项的第1个元素：商品条码
                        code = item[0]
                        # 获取商品条码读取商品，再获取商品的名称
                        name = repository[code][1]
                        # 获取商品条码读取商品，再获取商品的单价
                        price = repository[code][2]
                        # 获取该购物项的第2个元素：商品数量
                        number = item[1]
                        # 小计
                        amount = price * number
                        # 计算总计
                        sum = sum + amount
                        line = "%-5s|%17s|%40s|%12s|%6s|%12s" % \
                               (id, code, name, price, number, amount)
                        print(line)
                    print("-" * 100)
                    print("                          总计: ", sum)
                print("=" * 100)

            # 添加购买商品，就是向代表用户购物清单的list列表中添加一项。
            def add():
                # 等待输入条码
                code = input("请输入商品的条码:\n")
                # 没有找到对应的商品，条码错误
                if code not in repository:
                    print("条码错误，请重新输入")
                    return
                # 根据条码找商品
                goods = repository[code]
                # 等待输入数量
                number = input("请输入购买数量:\n")
                # 把商品和购买数量封装成list后加入购物清单
                shop_list.append([code, int(number)])

            # 修改购买商品的数量，就是修改代表用户购物清单的list列表的元素
            def edit():
                id = input("请输入要修改的购物明细项的ID:\n")
                # id减1得到购物明细项的索引
                index = int(id) - 1
                # 根据索引获取某个购物明细项
                item = shop_list[index]
                # 提示输入新的购买数量
                number = input("请输入新的购买数量:\n")
                # 修改item里面的number
                item[1] = int(number)

            # 删除购买的商品明细项，就是删除代表用户购物清单的list列表的一个元素。
            def delete():
                id = input("请输入要删除的购物明细项的ID: ")
                index = int(id) - 1
                # 直接根据索引从清单里面删除掉购物明细项
                del shop_list[index]

            def payment():
                # 先打印清单
                show_list()
                print('\n' * 3)
                print("欢迎下次光临")
                # 退出程序
                import os
                os._exit(0)

            # 后台添加商品函数
            def adds():
                # 获取要添加的商品信息
                a = input("请输入商品条码:")
                b = input('请输入商品名称:')
                c = input('请输入商品单价:')
                d = input('请输入商品数量:')
                # 添加到商品列表
                shangpin.append([a, b, c, d])
                # 重新打印商品清单
                init_repository()
                show_goods()

            # 后天修改商品属性函数
            def edits():
                a = input("请输入商品条码:")
                # 获取此商品条码的新的值
                if a in repository.keys():
                    e = input("请输入修改后商品名字:")
                    f = input("请输入修改后商品单价:")
                    g = input("请输入修改后商品数量:")
                    repository.update({a: [a, e, f, g]})
                    print(repository[a])
                    show_goods()
                else:
                    print('输入条码有误')

            def deletes():
                h = input('请输入您要下架商品条码:')
                # 直接根据条码从仓库里面删除掉此商品
                repository.pop(h)
                show_goods()

            # 重新打印商品清单
            def show_good():
                show_goods()

            # 后台支持的操作
            cmd_dicts = {'a': adds, 'e': edits, 'd': deletes, 's': show_good, 'q': quit}

            def root():
                # 先打印清单
                show_goods()
                print("欢迎进入超市货品管理平台")
                print("=" * 100)
                while True:
                    cmds = input("后台操作指令: \n" +
                                 "    添加商品(a)  修改商品(e)  删除商品(d)  全部商品(s)  退出(q)\n")
                    if cmds == 'q':
                        return
                    elif cmds not in cmd_dicts:
                        print("好好玩，行吗！")
                    else:
                        cmd_dicts[cmds]()

            # 用户所支持的操作
            cmd_dict = {'a': add, 'e': edit, 'd': delete, 'p': payment, 's': show_goods, 'r': root}
            # 初始仓库并展示
            init_repository()
            show_goods()

            # 显示命令提示
            def show_command():
                # 等待命令
                cmd = input("用户操作指令: \n" +
                            "    添加(a)  修改(e)  删除(d)  结算(p)  超市商品(s)  后台管理(r)\n")
                # 如果用户输入的字符没有对应的命令
                if cmd not in cmd_dict:
                    print("不要玩，好不好！")
                else:
                    cmd_dict[cmd]()

            # 显示清单和操作命令提示
            while True:
                show_list()
                show_command()


            print()
        elif op == "2":
            print("程序猿正在紧急写代码，敬请关注！")
        elif op == "3":
            print("程序猿正在紧急写代码，敬请关注！")
        else:
            print("输入错误，请重新输入！")


