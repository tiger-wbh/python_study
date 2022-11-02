import os.path
import pickle
import random
import time


class Card():
    def __init__(self, cardId, cardPasswd, cardMoney):
        self.cardId = cardId
        self.cardPasswd = cardPasswd
        self.cardMoney = cardMoney
        self.cardLock = False  # 银行卡的状态

class User():
    def __init__(self, name, idCard, phone, card):
        self.name = name
        self.idCard = idCard
        self.phone = phone
        self.card = card

class Admin():
    admin = "1"
    passwd = "1"

    def printAdminView(self):
        print("**********************************************")
        print("*                                            *")
        print("*                                            *")
        print("*            欢迎登录银行系统                   *")
        print("*                                            *")
        print("*                                            *")
        print("**********************************************")

    def printSysFunctionView(self):
        print("**********************************************")
        print("*          开户（1）          查询（2）         *")
        print("*          取款（3）          存款（4）         *")
        print("*          转账（5）          改密（6）         *")
        print("*          锁定（7）          解锁（8）         *")
        print("*          补卡（9）          销户（0）         *")
        print("*                   退出（q）                  *")
        print("**********************************************")

    def adminOption(self):
        inputAdmin = input("请输入管理员账号：")
        if self.admin != inputAdmin:
            print("输入账号有误！")
            return -1
        inputPasswd = input("请输入管理员密码：")
        if self.passwd != inputAdmin:
            print("密码输入有误！")
            return -1

        # 账号和密码均正确之后
        print("操作成功，请稍后。。。")
        time.sleep(2)
        return 0

    def ban(self, allUsers):
        for key in allUsers:
            print("账号：" + key + "\n" + "姓名：" + allUsers[key].name + "\n" + "身份证号：" + allUsers[key].idCard +
                  "\n" + "电话号码：" + allUsers[key].phone + "\n" + "银行卡密码：" + allUsers[key].card.cardPasswd + "\n")

class ATM():
    def __init__(self, allUsers):
        self.allUsers = allUsers    # 用户字典

    # 开户
    def createUser(self):
        # 向用户字典中添加一对键值对（卡号->用户）
        name = input("请输入您的姓名：")
        idCard = input("请输入您的身份证号：")
        phone = input("请输入您的电话号码：")
        prestoreMoney = int(input("请输入预存款金额："))
        if prestoreMoney < 0:
            print("预存款需要大于0！开户失败")
            return -1
        onePasswd = input("请设置密码：")
         # 验证密码
        if not self.checkPasswd(onePasswd):
            print("输入密码错误， 开户失败！")
            return -1

        # 生成银行卡号
        cardStr = self.randomCardId()
        card  = Card(cardStr, onePasswd, prestoreMoney)
        user = User(name, idCard, phone, card)

        # 存到字典
        self.allUsers[cardStr] = user
        print("开户成功！请记住卡号：" + cardStr)

    # 查询
    def searchUserInfo(self):
        cardNum = input("请输入您的卡号：")
        user = self.allUsers.get(cardNum)
        if self.checkUser(user) != 0:
            return -1
        print("账号：%s 余额：%d" % (user.card.cardId, user.card.cardMoney))

    # 取款
    def getMoney(self):
        cardNum = input("请输入您的卡号：")
        user = self.allUsers.get(cardNum)
        if self.checkUser(user) != 0:
            return -1
        # 开始取款
        amount = int(input("请输入取款金额："))
        if amount > user.card.cardMoney:
            print("取款金额超过余额，取款失败！")
            return -1
        if amount <= 0:
            print("取款金额必须大于0，取款失败！")
            return -1
        user.card.cardMoney -= amount
        print("您取款%d元，余额为%d元！" % (amount, user.card.cardMoney))

    # 存款
    def saveMoney(self):
        cardNum = input("请输入您的卡号：")
        user = self.allUsers.get(cardNum)
        if self.checkUser(user) != 0:
            return -1

        # 开始存款
        amount = int(input("验证成功，请输入存款金额："))
        if amount <= 0:
            print("存款金额必须大于0，存款失败！")
            return -1
        user.card.cardMoney += amount
        print("您存款%d元，余额为%d元！" % (amount, user.card.cardMoney))

    # 转账
    def transferMoney(self):
        cardNum = input("请输入您的卡号：")
        user = self.allUsers.get(cardNum)
        if self.checkUser(user) != 0:
            return -1

        # 开始转账
        amount = int(input("请输入转账金额："))
        if amount > user.card.cardMoney:
            print("转账金额超过余额，转账失败！")
            return -1
        if amount <= 0:
            print("转账金额必须大于0，转账失败！")
            return -1

        newcard = input("请输入转入账户：")
        newuser = self.allUsers.get(newcard)
        if not newuser:
            print("该卡号不存在，转账失败！")
            return -1
            # 判断是否锁定
        if newuser.card.cardLock:
            print("该卡号已锁定！请解锁后在使用该功能！")
            return -1
        user.card.cardMoney -= amount
        newuser.card.cardMoney += amount
        time.sleep(1)
        print("转账成功，请稍后。。。")
        time.sleep(1)
        print("您转账%d元，余额为%d元！" % (amount, user.card.cardMoney))

    # 改密
    def changePasswd(self):
        cardNum = input("请输入您的卡号：")
        print("正在验证，请稍等。。。")
        user = self.allUsers.get(cardNum)
        if self.checkUser(user) != 0:
            return -1
        time.sleep(1)
        print("验证成功")
        time.sleep(1)

        # 开始改密
        newpasswd = input("请输入新密码：")
        if not self.checkPasswd(newpasswd):
            print("密码校验错误，改密失败！")
            return -1
        user.card.cardPasswd = newpasswd
        print("密码修改成功，请稍后！")

    # 锁定
    def lockUser(self):
        cardNum = input("请输入您的卡号：")
        user = self.allUsers.get(cardNum)
        if not user:
            print("该卡号不存在！")
            return -1
            # 判断是否锁定
        if user.card.cardLock:
            print("该卡号已锁定！请解锁后在使用该功能！")
            return -1
            # 验证密码
        if not self.checkPasswd(user.card.cardPasswd):
            print("密码输入有误，锁定失败")
            return -1
        tempIdCard = input("请输入您的身份证号：")
        if tempIdCard != user.idCard:
            print("身份证号验证失败，锁定失败！")
            return -1

        # 锁定
        user.card.cardLock = True
        print("锁定成功！")

    # 解锁
    def unlockUser(self):
        cardNum = input("请输入您的卡号：")
        user = self.allUsers.get(cardNum)
        if not user:
            print("该卡号不存在！")
            return -1
            # 判断是否锁定
        if not user.card.cardLock:
            print("该卡号未被锁定，无需解锁！")
            return -1
            # 验证密码
        if not self.checkPasswd(user.card.cardPasswd):
            print("密码输入有误，解锁失败")
            return -1
        tempIdCard = input("请输入您的身份证号：")
        if tempIdCard != user.idCard:
            print("身份证号验证失败，解锁失败！")
            return -1

        # 解锁
        user.card.cardLock = False
        print("解锁成功！")

    # 补卡
    def newCard(self):
        cardNum = input("请输入您的卡号：")
        user = self.allUsers.get(cardNum)
        if not user:
            print("该卡号不存在！")
            return -1
        tempname = input("请输入您的姓名：")
        tempidcard = input("请输入您的身份证号：")
        tempphone = input("请输入您的电话号码：")
        if tempname != user.name or tempidcard != user.idCard or tempphone != user.phone:
            print("信息有误，补卡失败！")
            return -1
        newpasswd = input("请输入新密码：")
        if not self.checkPasswd(newpasswd):
            print("密码校验错误，改密失败！")
            return -1
        user.card.cardPasswd = newpasswd
        time.sleep(1)
        print("补卡成功！")

    # 销户
    def killUser(self):
        cardNum = input("请输入您的卡号：")
        user = self.allUsers.get(cardNum)
        if self.checkUser(user) != 0:
            return -1

        del self.allUsers[cardNum]
        time.sleep(1)
        print("销户成功，请稍后！")


    # 验证银行卡的基本信息
    def checkUser(self, user):
        # 验证是否存在该卡号
        if not user:
            print("该卡号不存在！")
            return -1
        # 判断是否锁定
        if user.card.cardLock:
            print("该卡号已锁定！请解锁后在使用该功能！")
            return -1
        # 验证密码
        if not self.checkPasswd(user.card.cardPasswd):
            print("密码输入有误，该卡已锁定！请解锁后在使用该功能！")
            user.card.cardLock = True
            return -1
        return 0

    # 验证密码
    def checkPasswd(self, realPasswd):
        for i in range(3):
            tempPasswd = input("请输入密码：")
            if tempPasswd == realPasswd:
                return True
        return False

    # 生成卡号
    def randomCardId(self):
        while True:
            str = ""
            for i in range(6):
                ch = chr(random.randrange(ord("0"), ord("9") + 1))
                str += ch
            # 判断重复
            if not self.allUsers.get(str):
                return str

# 主函数
def main():
    # 界面对象
    admin = Admin()

    # 管理员开机
    admin.printAdminView()
    if admin.adminOption():
        return -1
    # 第一次文件为空时使用
    # allUsers = {}

    # 提款机对象
    filepath = os.path.join(os.getcwd(), "allusers.txt")
    # print(filepath)
    f = open(filepath, "rb")
    allUsers = pickle.load(f)
    atm = ATM(allUsers)

    while True:
        admin.printSysFunctionView()
        option = input("请输入您的操作：")
        if option == "1":
            atm.createUser()
        elif option == "2":
            atm.searchUserInfo()
        elif option == "3":
            atm.getMoney()
        elif option == "4":
            atm.saveMoney()
        elif option == "5":
            atm.transferMoney()
        elif option == "6":
            atm.changePasswd()
        elif option == "7":
            atm.lockUser()
        elif option == "8":
            atm.unlockUser()
        elif option == "9":
            atm.newCard()
        elif option == "0":
            atm.killUser()
        elif option == "q":
            if not admin.adminOption():
                f = open(filepath, "wb")
                pickle.dump(atm.allUsers, f, 0)
                f.close()
                return -1
        elif option == "22":
            admin.ban(allUsers)

        time.sleep(2)

if __name__ == "__main__":
    main()
