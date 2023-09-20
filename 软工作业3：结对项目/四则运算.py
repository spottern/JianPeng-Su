import random
from fractions import Fraction
from memory_profiler import profile
import time
import os
import glob
from tkinter
num = []  # 用于储存生成题目的字符及计算数字
title = []  # 用于储存生成题目的二叉树


class N_S:  # 数字结构体
    def __init__(self):
        self.number_sign = 0  # 数的类型
        self.numerator = 0  # 分子
        self.denominator = 1  # 分母

    def generate_number_sign(self):  # 随机生成数的类型，类型值为1时分母默认为1
        self.number_sign = random.randint(1, 2)

    def generate_numerator(self, min, max):  # 随机生成分子的大小
        self.numerator = random.randint(min, max)

    def generate_denominator(self, min, max):  # 随机生成分母的大小
        self.denominator = random.randint(min, max)


class B_T:  # 二叉树结构体,以及相关
    def __init__(self, rootObj):
        self.key = rootObj  # 将运算符作为根节点
        self.leftChild = None
        self.rightChild = None

    def insert_left(self, newRoot):  # 插入左子树
        if (self.leftChild == None):
            self.leftChild = B_T(newRoot)
        else:
            t = B_T(newRoot)
            t.leftChild = self.leftChild
            self.leftChild = t

    def insert_right(self, newRoot):  # 插入右子树
        if (self.rightChild == None):
            self.rightChild = B_T(newRoot)
        else:
            t = B_T(newRoot)
            t.rightChild = self.rightChild
            self.rightChild = t

    def get_leftChild(self):  # 返回左孩子
        return self.leftChild

    def get_rightChild(self):  # 返回右孩子
        return self.rightChild

    def set_root(self, Obj):  # 修改当前结点的内容
        self.key = Obj

    def get_Root(self):  # 返回当前结点的内容
        return self.key

    def inorder(self):  # 中序遍历
        if self.leftChild:
            self.leftChild.inorder()
        if self.key:
            num.append(self.key)
        if self.rightChild:
            self.rightChild.inorder()


# 判断树是否同构，防止出现重复的题目
def isOmorphic(t1, t2):
    if t1 == None and t2 == None: return True
    if (t1 != None and t2 == None) | (t1 == None and t2 != None):
        return False
    if t1.key != t2.key:
        return False
    if t1.leftChild == None and t2.leftChild == None:
        return isOmorphic(t1.rightChild, t2.rightChild)
    if t1.leftChild != None and t2.leftChild != None and t1.leftChild.key == t2.leftChild.key:
        return isOmorphic(t1.leftChild, t2.leftChild) and isOmorphic(t1.rightChild, t2.rightChild)
    else:
        return isOmorphic(t1.leftChild, t2.rightChild) and isOmorphic(t1.rightChild, t2.leftChild)


# 随机生成运算符号‘+’，‘-’，‘*’，‘/’
def generate_operator():
    operators = ['+', '-', '*', '/']
    return random.choice(operators)


# 随机生成题目长度
def num_size():
    size = [1, 2, 3]
    return random.choice(size)


# 随机生成题目
def generate_num(min, max):
    size = num_size()
    # 如果题目长度为2（1+2的情况）
    if size == 2:
        operator = generate_operator()  # 随机生成运算符号
        t = B_T(operator)  # 将随机生成的运算符插入二叉树作为根节点
        a = N_S()  # 参与运算的数a结构体
        b = N_S()  # 参与运算的数b结构体
        a.generate_number_sign()  # 参与运算的数a
        if a.number_sign == 1:  # 随机生成数的类型，类型值为1时分母默认为1
            a.generate_numerator(min, max)  # 随机生成分子的大小
        else:
            a.generate_numerator(min, max)  # 随机生成分子的大小
            a.generate_denominator(min, max)  # 随机生成分母的大小
        b.generate_number_sign()  # 参与运算的数2
        if b.number_sign == 1:
            b.generate_numerator(min, max)  # 随机生成分子的大小
        else:
            b.generate_numerator(min, max)  # 随机生成分子的大小
            b.generate_denominator(min, max)  # 随机生成分母的大小
        t.insert_left(Fraction(a.numerator, a.denominator))  # 将数a插入左子树
        t.insert_right(Fraction(b.numerator, b.denominator))  # 将数b插入右子树

    # 如果题目长度为1或3
    else:
        operator = generate_operator()  # 随机生成运算符号1
        t = B_T(operator)  # 将随机生成的运算符1插入二叉树作为根节点
        # 如果题目长度为1（1+2+3的情况）
        if size == 1:
            operator = generate_operator()  # 随机生成运算符号2
            t.insert_left(operator)  # 将该运算符2插入左子树
            a = N_S()  # 参与运算的数a结构体
            b = N_S()  # 参与运算的数b结构体
            c = N_S()  # 参与运算的数c结构体

            c.generate_number_sign()  # 随机生成数c的类型
            # 如果生成数c的类型为1
            if c.number_sign == 1:
                c.generate_numerator(min, max)  # 随机生成分子的大小（分母在该情况下为1）
            else:
                c.generate_numerator(min, max)  # 随机生成分子的大小
                c.generate_denominator(min, max)  # 随机生成分母的大小
            t.insert_right(Fraction(c.numerator, c.denominator))  # 将生成的数c插入右子树

            t1 = t.leftChild  # t1指向左子树
            a.generate_number_sign()  # 随机生成数a的类型
            if a.number_sign == 1:
                a.generate_numerator(min, max)
            else:
                a.generate_numerator(min, max)
                a.generate_denominator(min, max)
            t1.insert_left(Fraction(a.numerator, a.denominator))  # 将生成的数a插入左子树的左子树

            # 随机生成数b的类型
            b.generate_number_sign()
            if b.number_sign == 1:
                b.generate_numerator(min, max)
            else:
                b.generate_numerator(min, max)
                b.generate_denominator(min, max)
            t1.insert_right(Fraction(b.numerator, b.denominator))  # 将生成的数a插入左子树的右子树

        # 如果题目长度为3（3+2+1的情况）
        else:
            operator = generate_operator()  # 随机生成运算符2
            t.insert_right(operator)  # 将运算符2插入右子树
            a = N_S()
            b = N_S()
            c = N_S()

            a.generate_number_sign()  # 随机生成数a的类型
            if a.number_sign == 1:  # 如果数a的类型为1
                a.generate_numerator(min, max)
            else:
                a.generate_numerator(min, max)
                a.generate_denominator(min, max)
            t.insert_left(Fraction(a.numerator, a.denominator))  # 将数a插入左子树

            t2 = t.rightChild
            b.generate_number_sign()
            if b.number_sign == 1:
                b.generate_numerator(min, max)
            else:
                b.generate_numerator(min, max)
                b.generate_denominator(min, max)
            t2.insert_left(Fraction(b.numerator, b.denominator))  # 将数b加入右子树的左子树

            c.generate_number_sign()
            if c.number_sign == 1:
                c.generate_numerator(min, max)
            else:
                c.generate_numerator(min, max)
                c.generate_denominator(min, max)
            t2.insert_right(Fraction(c.numerator, c.denominator))  # 将数b加入右子树的右子树
    return t


# 将num列表转换为字符串
# num=[1,'/',2,'+',3]
def str_num(t):
    # 3数+2字符
    # num = []  用于储存生成题目的字符及计算数字
    if len(num) == 5:
        a = num.index(t.key)  # 取出根节点在列表中的位置
        # 如果第二个字符是乘除，第一个字符是加减，则在加减的部分加上括号
        if a == 3 and (num[3] == '*' or num[3] == '/') and (num[1] == '+' or num[1] == '-'):
            num.insert(0, '(')
            num.insert(4, ')')
        elif num[1] != num[3]:
            num.insert(2, '(')
            num.insert(6, ')')
    # result1代表输入到题目中显示的结果
    # result2表示电脑进行运算的结果,目的是为了将运算过程中的/改为÷
    if len(num) == 3:
        result1 = f"{num[0]} {str(num[1]).replace('/', '÷')} {num[2]}"
        result2 = '{} {} {}'.format(num[0], num[1], num[2])
    elif len(num) == 5:
        result1 = f"{num[0]} {str(num[1]).replace('/', '÷')} {num[2]} {str(num[3]).replace('/', '÷')} {num[4]}"
        result2 = '{} {} {} {} {}'.format(num[0], num[1], num[2], num[3], num[4])
    else:
        result1 = f"{num[0]} {str(num[1]).replace('/', '÷')} {num[2]} {str(num[3]).replace('/', '÷')} {num[4]} {str(num[5]).replace('/', '÷')} {num[6]}"
        result2 = '{} {} {} {} {} {} {}'.format(num[0], num[1], num[2], num[3], num[4], num[5], num[6])

    return result1, result2


# 重复生成题目
# n为生成题目的数量
def repeat(n, min, max):
    while n != 0:
        t = generate_num(min, max)
        if len(title) == 0:
            n -= 1
            title.append(t)
        else:
            for i in range(len(title)):
                if isOmorphic(t, title[i - 1]) == True:  # 通过是否同构表示是否重复
                    continue
            title.append(t)
            n -= 1


def main():
    function = int(input('生成题目输入1，自动查答案输入2\n'))
    # function = 2
    while function != 1 and function != 2:
        print('输入错误，请重新输入\n')
        function = int(input('生成题目输入1，自动查答案输入2\n'))
    if function == 1:
        # 删除之前已有的文件，避免出现文本重叠的情况
        for file in glob.glob('Answers.txt'):
            os.remove(file)
        for file in glob.glob('Exercises.txt'):
            os.remove(file)
        n = int(input('输入要生成题目的数量:'))
        while 1:
            min = int(input('输入数值的下限，必须是正数:'))
            max = int(input(f'输入数值的上限，需要大于{min}:'))
            if min <= 0:
                print("输入下限错误，请重新输入！")
                continue
            elif max < min:
                print("输入上限错误，请重新输入！")
            else:
                break
        f1 = open('./Exercises.txt', 'a', encoding='utf-8')
        f2 = open('./Answers.txt', 'a', encoding='utf-8')
        repeat(n, min, max)
        for i in range(len(title)):
            num.clear()
            title[i].inorder()
            question1, question2 = str_num(title[i])
            print(question1)
            f1.write(f'{i + 1}. ' + question1 + '\n')
            temp = question2.split(' ')

            if len(temp) == 5:
                problem = 'Fraction(temp[0])' + temp[1] + 'Fraction(temp[2])' + temp[3] + 'Fraction(temp[4])'
            elif len(temp) == 3:
                problem = 'Fraction(temp[0])' + temp[1] + 'Fraction(temp[2])'
            elif temp[0] == '(':
                problem = temp[0] + 'Fraction(temp[1])' + temp[2] + 'Fraction(temp[3])' + temp[4] + temp[
                    5] + 'Fraction(temp[6])'
            else:
                problem = 'Fraction(temp[0])' + temp[1] + temp[2] + 'Fraction(temp[3])' + temp[
                    4] + 'Fraction(temp[5])' + temp[6]
            f2.write(f'{i + 1}. ' + str(eval(problem)) + '\n')

    else:
        # 删除之前已有的文件，避免出现文本重叠的情况
        for file in glob.glob('Grade.txt'):
            os.remove(file)
        LIMIT = 10e-10
        f1 = open('./Exercises.txt', 'r', encoding='utf-8')
        f2 = open('./Answers.txt', 'r', encoding='utf-8')
        f3 = open('./Grade.txt', 'w', encoding='utf-8')
        line1 = f1.readline()
        line2 = f2.readline()
        Correct = []
        Wrong = []
        while line1 and line2:
            a = line1.split('.')
            b = line2.split('.')
            operators = ['+', '-', '*', '/', '(', ')']
            c = a[1].strip()
            c = c.split(' ')
            n = 0
            while n < len(c):
                try:
                    operators.index(c[n])
                    n += 1
                except:
                    c.insert(n, '(')
                    c.insert(n + 2, ')')
                    n += 2
            c = ' '.join(c)
            if (eval(c) - eval(b[1])) < LIMIT:
                Correct.append(a[0])
            else:
                Wrong.append(b[0])
            line1 = f1.readline()
            line2 = f2.readline()
        length1 = len(Correct)
        Correct = ','.join(Correct)
        Correct = '(' + Correct + ')'
        print(Correct)
        f3.write('Correct: ' + f'{length1}' + Correct + '\n')

        length2 = len(Wrong)

        Wrong = ','.join(Wrong)
        Wrong = '(' + Wrong + ')'
        print(Wrong)
        f3.write('Wrong: ' + f'{length2}' + Wrong + '\n')


if __name__ == '__main__':
    main()
