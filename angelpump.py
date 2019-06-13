# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 17:53:10 2019

@author: gonggong01
"""

import xlrd#处理excel文件的模块
import math#数学函数，ceil,round,floor
import matplotlib.pyplot as plt#画图
import numpy as np #方便处理数组，矩阵等，跟matlab的处理很般配
from scipy.optimize import curve_fit
import configparser#用于读取配置文件
#下面两行主要是为了画图中能显示中文字符
import matplotlib as mpl 
mpl.rcParams['font.sans-serif'] = ['SimHei']

#类似matlab中pow2的功能，就是函数y=ax**b+c
def func_pow2(x, a, b, c):
    return a*pow(x,b)+c

#读取配置文件信息，有关外部数据文件(Excel文件)的相关信息，包括文件名，sheet,起始行，时间的列，采集的输液量或注射量的列
def Get_Global_Param_From_Config():
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')
    xlsx_filename = config['Global']['Data_File_Name']
    sheet_index = config['Global']['Sheet_Index']#索引的方式，从0开始
    begin_line =  config['Global']['Begin_Line']
    time_column_index_in_sheet = config['Global']['Time_Column_Index_In_Sheet']#索引的方式，从0开始
    volume_column_index_in_sheet = config['Global']['Volume_Column_Index_In_Sheet']#索引的方式，从0开始
    return (xlsx_filename,sheet_index,begin_line,time_column_index_in_sheet,volume_column_index_in_sheet)

#读取配置文件信息，速度上升图的标题，还有保存文件名，文件名可以是pdf或者jpg后缀    
def Get_Rate_Param_From_Config():
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')
    rate =  config['Global']['Rate']
    rate_title = config['Rate Curve']['Title']
    rate_filename = config['Rate Curve']['Output_File_Name']
    return (rate,rate_title,rate_filename)

#读取配置文件，喇叭图的标题，还有保存文件名，文件名可以是pdf或者jpg后缀；还有拟合曲线所需要的初始参数
def Get_Trumpet_Param_From_Config():
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')
    rate =  config['Global']['Rate']
    trumpet_title = config['Trumpet Curve']['Title']
    trumpet_filename = config['Trumpet Curve']['Output_File_Name']
    max_fit_param1 = config['Trumpet Curve']['MAX_FIT_param1']
    max_fit_param2 = config['Trumpet Curve']['MAX_FIT_param2']
    max_fit_param3 = config['Trumpet Curve']['MAX_FIT_param3']
    min_fit_param1 = config['Trumpet Curve']['MIN_FIT_param1']
    min_fit_param2 = config['Trumpet Curve']['MIN_FIT_param2']
    min_fit_param3 = config['Trumpet Curve']['MIN_FIT_param3']
    return (rate,trumpet_title,trumpet_filename,max_fit_param1,max_fit_param2,max_fit_param3,min_fit_param1,min_fit_param2,min_fit_param3)

#从Excel文件中读取数据，即时间和液量，以两个数组返回
def Get_Data_From_EXCEL():
    #Read config file
    (xlsx_filename,sheet_index,begin_line,time_column_index_in_sheet,volume_column_index_in_sheet) = Get_Global_Param_From_Config()
    readbook = xlrd.open_workbook(xlsx_filename)
    sheet_index = int(sheet_index)
    sheet = readbook.sheet_by_index(sheet_index)#索引的方式，从0开始
    #截取begin_line个点以后的242个数据
    Weight = []
    UTime = []
    for i in range(0,242):
        time_column_index_in_sheet = int(time_column_index_in_sheet)
        volume_column_index_in_sheet = int(volume_column_index_in_sheet)
        tcellType = sheet.cell(int(begin_line)+i,time_column_index_in_sheet).ctype
        tcellVal = sheet.cell(int(begin_line)+i,time_column_index_in_sheet).value#索引的方式，从0开始
        vcellType = sheet.cell(int(begin_line)+i,volume_column_index_in_sheet).ctype
        vcellVal = sheet.cell(int(begin_line)+i,volume_column_index_in_sheet).value#索引的方式，从0开始
        if tcellType == 3:#时间值
            timeval = xlrd.xldate_as_datetime(tcellVal, 0)
            UTime.append(timeval)
        
        if vcellType == 1:#字符串
            vcellVal = "".join(vcellVal).strip()
            vcellVal = vcellVal.strip('g')
            vcellVal = vcellVal.strip()
            Weight.append(float(vcellVal))

        if vcellType == 2:#数值
            Weight.append(vcellVal)


    return UTime,Weight        

#画一幅'速度上升图'
def Draw_Rate_Curve_Map():
    (rate,rate_title,rate_filename) =Get_Rate_Param_From_Config()
    Dwater = 0.998
    RATE = float(rate)
    UTime,Weight = Get_Data_From_EXCEL()
    Qwater = []
    Qwater.append(0)
    for i in range(1,13):
        qtime = (UTime[20*i+1]- UTime[20*(i-1)+1])
        qtime = qtime.total_seconds()
        qval = 3600*(Weight[20*i+1]- Weight[20*(i-1)+1])/(qtime*Dwater)
        Qwater.append( qval )

    xx = []
    for i in range(0,13):
        xx.append(i*10)

    yy = []
    for i in range(0,13):
        yy.append(RATE)

    #开始画图
    plt.figure(figsize=(24,16))#防止出现相邻图片重叠
    z1 = np.polyfit(xx,Qwater,5)#拟合曲线
    p1 = np.poly1d(z1)#p1就是拟合曲线的参数
    x_new = np.linspace(xx[0], xx[12], 200)#为了让曲线圆滑，增加200个点的值
    y_new = p1(x_new)#依照这200个点的x值，得到y值，即得到了200个点的坐标
    plt.plot(xx,Qwater,'x')#画速度上升图的点
    plt.plot(x_new,y_new,'r') #依照这些点，拟合曲线，画速度上升图的曲线
    plt.plot([xx[0],xx[12]],[RATE,RATE],'b',linewidth=2)#画条参照的速度值的直线
    plt.xlabel('time(min)',fontSize = 16)
    plt.ylabel('flow(ml/h)',fontSize = 16)
    plt.title(rate_title,fontSize = 16)
    plt.xlim(0,120)
    plt.ylim(0,1.2*RATE)
    bbox = dict(boxstyle="round,pad=0.5", fc="lightgray")
    arrowprops = dict(
            arrowstyle = "->",
            connectionstyle = "angle,angleA=0,angleB=90,rad=10")
    # 设置偏移量
    offset = 72
    plt.annotate('设定流速',
                 (25, 1*RATE), xytext=(-2*offset, offset), textcoords='offset points',
                 bbox=bbox, arrowprops=arrowprops)
    plt.annotate('速度上升曲线',
                        (70, 1.05*RATE), xytext=(-2*offset, offset), textcoords='offset points',
                        bbox=bbox, arrowprops=arrowprops)
    plt.savefig(rate_filename,dpi=400,bbox_inches='tight')#,dpi=400,bbox_inches='tight'
    plt.close()
    return

#画喇叭图
def Draw_Trumpet_Curve_Map():
    #Read config file
    (rate,trumpet_title,trumpet_filename,max_fit_param1,max_fit_param2,max_fit_param3,min_fit_param1,min_fit_param2,min_fit_param3) =Get_Trumpet_Param_From_Config()
    PartTime = [1,2,5,11,19,31]
    ShortTime = 0.5
    AllTime = 60
    Dwater = 0.998
    RATE = float(rate)
    UTime,Weight = Get_Data_From_EXCEL()
    Qwater = []
    Ewater = []
    for i in range(0,241):
        qtime = UTime[i+1]-UTime[i]
        qtime = qtime.total_seconds()
        qval = 3600*(Weight[i+1]-Weight[i])/(qtime*Dwater)
        Qwater.append(qval)
        Ewater.append(100*(qval-RATE)/RATE)
  
    Emax = []
    Emin = []  
    for k in range(0,6):
        j_max = int((AllTime-PartTime[k]+ShortTime)/ShortTime)
        Epart = []
        for j in range(0,j_max):
            sum = 0
            i_max = (j+int(PartTime[k]/ShortTime))
            for i in range(j,i_max):
                sum=sum+Ewater[i]
            
            EpartVal = sum*ShortTime/PartTime[k]
            Epart.append(EpartVal)
        
        Emax.append(max(Epart))
        Emin.append(min(Epart))
    
    tt = []
    for i in range(0,6):
        val = (Emax[i]+Emin[i])/2
        tt.append(val)
    
    plt.figure(figsize=(24,16))#防止出现相邻图片重叠
    plt.plot(PartTime,tt,'*')#y
    plt.plot(PartTime,Emax,'x')#r
    plt.plot(PartTime,Emin,'o')#k
    popt, pcov = curve_fit(func_pow2, PartTime, Emax,p0=(float(max_fit_param1),float(max_fit_param2),float(max_fit_param3)))
    xx_new = np.linspace(0.0000001, PartTime[-1], 500)
    yy_new = func_pow2(xx_new, *popt)
    plt.plot(xx_new, yy_new, 'r')
    popt, pcov = curve_fit(func_pow2, PartTime, Emin,p0=(float(min_fit_param1),float(min_fit_param2),float(min_fit_param3)))
    xx_new = np.linspace(0.0000001, PartTime[-1], 500)
    yy_new = func_pow2(xx_new, *popt)
    plt.plot(xx_new, yy_new, 'g')
    plt.plot([0,PartTime[-1]],[tt[-1],tt[-1]],'b',linewidth=2)
    plt.plot([0,PartTime[-1]],[0,0],'m--',linewidth=2)
    plt.xlabel('observation window(min)',fontSize = 16)
    plt.ylabel('varlation in flowrate[%]',fontSize = 16)
    plt.title(trumpet_title,fontSize = 16)
    plt.xlim(0,31)
    up_limit = math.ceil(Emax[0])
    down_limit = math.floor(Emin[0])
    y_array = []
    up_array = []
    down_array = []
    for i in range(0,6):
        val = (i+1)*up_limit/6
        val = round(val,2)
        up_array.append(val)
        val = (6-i)*down_limit/6
        val = round(val,2)
        down_array.append(val)
        
    y_array = down_array + [0] + up_array    
    plt.ylim(down_limit,up_limit)
    plt.yticks(y_array,y_array)
    bbox = dict(boxstyle="round,pad=0.5", fc="lightgray")
    arrowprops = dict(
            arrowstyle = "->",
            connectionstyle = "angle,angleA=0,angleB=90,rad=10")
    # 设置偏移量
    offset = 72
    plt.annotate('Ep(max)',
            (10, Emax[3]), xytext=(-2*offset, offset), textcoords='offset points',
            bbox=bbox, arrowprops=arrowprops)
    plt.annotate('Ep(min)',
            (6, Emin[2]), xytext=(-2*offset, offset), textcoords='offset points',
            bbox=bbox, arrowprops=arrowprops)
    total_error = '总的百分比误差(A): %.2f%% '%(tt[-1])
    plt.annotate(total_error,
            (4, tt[-1]), xytext=(-2*offset, offset), textcoords='offset points',
            bbox=bbox, arrowprops=arrowprops)
    plt.savefig(trumpet_filename,dpi=400,bbox_inches='tight')#,dpi=400,bbox_inches='tight'
    plt.close()    
    return
    
#主函数，取数据，生成速度上升图和喇叭图    
def main():
    print('begin')
    Draw_Rate_Curve_Map()
    Draw_Trumpet_Curve_Map()
    print('end')
    
if __name__ == "__main__":
    main()   