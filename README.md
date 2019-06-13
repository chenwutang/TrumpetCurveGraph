# TrumpetCurveGraph
make a Rate Curve Graph and Trumpet Curve Graph according to Excel raw data

How to use the config.ini?


配置文件config.ini，里面必须改动的
有数据文件名Data_File_Name
还有本次测试的速度Rate
其他项目，你作相应更改
Sheet_Index是你的excel文件中第几个sheet，默认值为0，是sheet1，
Begin_Line是用于计算的242个数据，从第几行开始
Time_Column是采集时间在第几列，默认值为1，是第2列
Volume_Column是采集的液体质量，在第几列，默认值为2，是第3列
Rate Curve是指画速度图的，第一个Title是图标上的标题，第二个就是输出的文件名，可以是pdf文件名，也可以是jpg的文件名
Trumpet Curve是指喇叭图的，上面的一样，下面的fit_param是拟合曲线的参数，如果画不出图的时候，改动这些参数，以可以输出图形
