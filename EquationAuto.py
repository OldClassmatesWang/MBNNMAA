# -*- coding: UTF-8 -*-
'''
@File    ：EquationAuto.py
@Author  ：Jeffrey Wang
@Date    ：2025/3/13 22:07
导出系数及求解方程
'''
import csv

import sympy as sp
import os

#The number of functions and their partial derivatives in the model sum
VARIABLES_NUM = 43
#Mathematica outputs the file address
FILEPATH = "E:\\Code\\Java_Code\\DS\\src\\File\\3-2-3-1\\1.csv"
#The common factor extracts the resulting address
SOLVEPATH = "E:\\Code\\Java_Code\\DS\\src\\File\\3-2-3-1\\2.txt"

#Original equation array
array=[]
#Common factor array
solveArray = []

def read_csv_to_array(file_path):
    '''
    Read a csv file into an array and convert each element to an Int
    :param file_path: csv file path
    :return: array
     '''
    data = []
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        # 创建 CSV 读取器对象
        reader = csv.reader(csvfile)
        for row in reader:
            int_row = [int(cell) for cell in row]
            # 将每一行添加到二维数组中
            data.append(int_row)
    return data


def orgnize_function_test(num):
    """
    Set up the first num equations, and print out the output, the test equation conversion is normal
    :return: Void
    """
    for h in range(num):
        elem = array[h]
        varible_f = elem[:VARIABLES_NUM]
        expr = 1
        empty_expr = sp.sympify(expr)
        for i in range(len(varible_f)):
            if varible_f[i] != 0:
                for j in range(varible_f[i]):
                    empty_expr  = empty_expr * sp.symbols("F_"+str(i+1))
        efficient_f = elem[VARIABLES_NUM:]
        for i in range(len(efficient_f)):
            if i == len(efficient_f) -1:
                empty_expr *= efficient_f[i]
                continue
            if efficient_f[i] != 0:
                for j in range(efficient_f[i]):
                    empty_expr *= sp.symbols("w_"+str(i+1))
        print("EQUATION  "+str(h+1) +":  "+ sp.latex(empty_expr))

def coefficient():
    """
    Partitioning factors and functions
    :return: dic[key:fucntion,value:coefficient]
    """
    dic={}
    for row in array:
        key = tuple(row[:VARIABLES_NUM])
        value = row[VARIABLES_NUM:]
        if key in dic:
            dic[key].append(value)
        else:
            dic[key] = [value]
    return dic
def transform_f(elem):
    """
    Transform the function composition to sympy expression
    :param elem:
    :return:
    """
    expr = 1
    empty_expr = sp.sympify(expr)
    for i in range(len(elem)):
        if elem[i] != 0:
            for j in range(elem[i]):
                empty_expr = empty_expr * sp.symbols("F_" + str(i + 1))
    return empty_expr

def transform_e(elem):
    """
    Transform the coefficient composition to sympy expression
    :param elem:
    :return:
    """
    expr = 1
    empty_expr = sp.sympify(expr)
    for i in range(len(elem)):
        if i == len(elem) - 1:
            empty_expr *= elem[i]
            continue
        if elem[i] != 0:
            for j in range(elem[i]):
                empty_expr *= sp.symbols("w_" + str(i + 1))
    return empty_expr

def extract_coefficient():
    """
    Extract the coefficient
    :return:
    """
    dic = coefficient()
    lists ={}
    for key,value in dic.items():
        expr = 0
        empty_expr = sp.sympify(expr)
        for elem in value:
            temp = transform_e(elem)
            empty_expr += temp
        factors = sp.factor(empty_expr)
        dic[key] = factors
    target= {}
    for key,value in dic.items():
        for sub_expr in value.args:
            if isinstance(sub_expr,(sp.Add)) and len(value.args) > 1:
                    target[sub_expr] = key
                    lists[sub_expr] = value
    temList = list(lists.values())
    try:
        with open(SOLVEPATH, 'w') as file:
            for expr in temList:
                # 将表达式转换为字符串
                expr_str = normalize2(sp.latex(expr))
                expr_str = normalize3(expr_str)
                file.write(expr_str + '\n'+'\n')
        print(f"表达式已成功写入 {SOLVEPATH}")
    except Exception as e:
        print(f"写入文件时出错: {e}")
    print_f(target)
    return temList

def print_f(target):
    """
    Print the list of functions corresponding to the deduplicated factor
    :param target:
    :return:
    """
    print()
    for key,value in target.items():
        str1 = sp.latex(key)
        str2 = sp.latex(transform_f(value))
        print("Key:"+str1 +"      Value:"+str2)

def normalize(expr):
    expr = expr.replace('\\left', '').replace('\\right', '').replace('\\omega ', 'omega')
    return expr

def normalize2(expr):
    expr = expr.replace('\\left', '').replace('\\right', '').replace("\\\\left","").replace("\\\\right","").replace("'","").replace("`","")
    return expr
def normalize3(expr):
    expr = expr.replace("w","\\omega")
    return expr

if __name__ == '__main__':
    array = read_csv_to_array(FILEPATH)
    orgnize_function_test(5)
    solveArray = extract_coefficient()
