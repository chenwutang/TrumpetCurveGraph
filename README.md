# TrumpetCurveGraph
make a Rate Curve Graph and Trumpet Curve Graph according to Excel raw data

How to use the config.ini?

    
[Global]
Data_File_Name = AJ5808 25mlh 30s 24h.xlsx    #有数据文件名

Rate = 25                                     #本次测试的速度

Sheet_Index = 0                               #你的excel文件中第几个sheet，默认值为0，是sheet1

Begin_Line = 201                              #用于计算的242个数据，从第几行开始

Time_Column_Index_In_Sheet = 1                #采集时间在第几列，默认值为1，是第2列

Volume_Column_Index_In_Sheet = 2              #采集的液体质量，在第几列，默认值为2，是第3列

[Rate Curve]
Title = AJ5808 Infusion Pump at 25ml/hr       #速度图  图标上的标题

Output_File_Name = 25ml Rate.pdf              #速度图  输出的文件名(可以是pdf文件名，也可以是jpg的文件名)


[Trumpet Curve]
Title = AJ5808 Infusion Pump at 25ml/hr       #喇叭图  图标上的标题

Output_File_Name = 25ml Trumpet.pdf           #喇叭图  输出的文件名(可以是pdf文件名，也可以是jpg的文件名)

MAX_FIT_param1 = 99                           #拟合曲线的参数，如果画不出图的时候，改动这些参数，或许可以输出图形

MAX_FIT_param2 = -1

MAX_FIT_param3 = 3

MIN_FIT_param1 = -90

MIN_FIT_param2 = -0.4

MIN_FIT_param3 = 23


