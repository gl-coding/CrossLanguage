python2代码批量转为python3代码

由于python存在python2和python3两个主要的版本方向，经常会有将python2的代码转到python3的环境下运行的需求。尤其是跑一些神经网络的代码时有很多是在python2的环境下写的。在python3下运行会遇见很多不兼容，最常见的就是python3中print函数必须加()而python2中不是。一个一个修改这种错误又非常麻烦。

这里介绍一个python3自带的脚本2to3.py，可以将python2的程序自动转为python3的形式，节省了很多修改细节的时间。这个脚本在Python安装目录下Toolsscripts文件夹下，如果是利用anaconda3安装的python3，就在anaconda3/Tools/scripts中，如下图：

使用方法也很简单，如果我需要转换某个python文件，比如E盘根目录下的test.py，只需要在命令行里输入

python 2to3.py -w E:/test.py

一个快速将python2代码批量转为python3代码的好方法

如果需要转换某个文件夹下的所有文件，例如E盘test文件夹下的所有文件，只需要在命令行里输入

python 2to3.py -w E:/test/

一个快速将python2代码批量转为python3代码的好方法

就是这么简单就可以完成python2代码像python3代码的变换，当然目前对于一些比较复杂的依赖这种方法还不能完全转换，还需要根据运行错误调整，不过已经可以节省很多的时间啦。