由于业务需要对用户操作数据进行分析，需要将批量的用户操作记录文件插入到mysql数据库。本人是python小白，以此文记录一下，同时也希望能帮到其他有这方面困扰的童鞋：

python的基本语法不阐述，网上有很多的教程，但是需要注意的是，如果你用的退格符不相同，是很容易引起各种错误的，所以看到报错的时候耐心检查一下自己的格式。

退格相关报错如下图:

![Image](https://raw.githubusercontent.com/zhuangchuming/python_-Traverse_file/blob/master/imgs/1.jpg)

全文退格使用的是tab，在这个位置我用空格符退一个的空格会报错。

步骤流程：
一、获取文件相关的信息，并解析

1、首先能够读取到路径下的文件列表

![image](https://raw.githubusercontent.com/zhuangchuming/python_-Traverse_file/blob/master/imgs/2.jpg)

2、遍历所有文件目录，判断是否是文件夹，是的话继续遍历文件夹

![Image](https://raw.githubusercontent.com/zhuangchuming/python_-Traverse_file/blob/master/imgs/3.jpg)

3、非文件夹的文件，对文件名字进行过滤，过滤在config.py的keyword，设置为自己的需要过滤的内容即可。

4、读取文件内容

![Image](https://raw.githubusercontent.com/zhuangchuming/python_-Traverse_file/blob/master/imgs/4.jpg)

5、将文件的内容解析成能够插入数据库的列表，每一组数据都保存到totalList，

all_the_text是文件的所有内容，config.GaomuTrue==1是我定制的解析数据格式，如果有其他要求，可以自己在else部分添加，并且把config.py的GaomuTrue的值给改为0。解析结果得到totalList,

![Image](https://raw.githubusercontent.com/zhuangchuming/python_-Traverse_file/blob/master/imgs/5.jpg)

二、连接上mysql数据库，并创建表插入数据

1、安装python-mysql

mac推荐链接：
http://blob.csdn.net/xiaodanpeng/article/details/46120359

windows跟linux的就要自己去找啦，嘿嘿。

2、连接mysql数据库，并选择使用的数据库名称，该名称的配置在config文件的databaseName.

![Image](https://raw.githubusercontent.com/zhuangchuming/python_-Traverse_file/blob/master/imgs/6.jpg)

3、插入数据

![Image](https://raw.githubusercontent.com/zhuangchuming/python_-Traverse_file/blob/master/imgs/7.jpg)

sql_string为mysql的语句，cur.executemany()这个方法是同时插入多个语句，这是mysql中最高效的插入方式。最后conn.commit()执行后，数据才会出现在数据库中。

Forexample：下图是本机的一个终端运行输出的例子。
遍历文件夹0000下面的所有文件

![Image](https://raw.githubusercontent.com/zhuangchuming/python_-Traverse_file/blob/master/imgs/8.jpg)

