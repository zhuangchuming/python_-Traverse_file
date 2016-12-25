#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb
import os
import time  
import config#配置文件
#root = './0000'
sep = os.sep
#databaseName = raw_input("please input the database name which whill be connected:")
tableName = raw_input('please input the table name which will be created:')
root = raw_input('请输入需要遍历的路径：')
print 'input : %s' % input

#连接表
try:  
	conn = MySQLdb.connect(config.serverAddr,config.user,config.password)  
	cur = conn.cursor()
	conn.select_db(config.databaseName)
except MySQLdb.Error,msg:  
	print "MySQL connet error %d: %s" %(msg.args[0],msg.args[1])


#创建表
def createTable():
	#cur.execute('create table if not exists mike
	sql = '(id int(4) primary key not null auto_increment, '+'qid text, '+'time text, '+'user text, '+'answer0 text, '+'answer1 text, '+'spend text)'
	cur.execute('create table if not exists '+tableName +sql) 
	conn.commit()
		

#读取文件里面的内容插入数据库
def InsertDataFromFile(absolutePath,file_name):
	file_name = file_name.split('.')[0]
	file_list_name = absolutePath.split(sep)
	if(len(file_list_name)>2):#设置父目录名字
		parent_name = file_list_name[len(file_list_name)-2]
	else:
		parent_name = "default_root"#缺省的根目录名字
	file_object = open(absolutePath)
	try:
		all_the_text = file_object.read()
	finally:
		file_object.close()
	all_the_text = all_the_text.strip(',')
	#all_the_text = all_the_text.replace('[','(');
	#splitList = all_the_text.replace(']',')');
	all_the_text = all_the_text.lstrip('[')
	all_the_text = all_the_text.rstrip(']') 
	splitList = all_the_text.split('],[')
	totalList = []
	for item in  splitList:
		arr = item.split(',')#将一组数据变成数据
		if config.GaomuTrue == 1:
			arr.insert(0,'0')#插入id
			arr.insert(3,parent_name+'_'+file_name.split(config.keyWord)[0])#插入文件名字
			arr.append(arr[4])
			arr.remove(arr[4])
			#text = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(arr[2]))
			#print text
			#arr[2] = text
			#arr.remove(arr[2])
			#arr.insert(2,text);
			#print time.localtime(int(arr[2]))
			#print time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(arr[2])))
			#print int(arr[2])
		else:
			arr.insert(0,'0')#插入id
			arr.insert(1,file_name)#插入文件名字
		#totalList.insert(len(totalList),arr);
		totalList.append(arr)
	try:  
		#sql_string = 'insert into '+tableName+ ' values (0,'+ file_name +',%s,%s,%s,%s,%s) '
		sql_string = 'insert into '+tableName+ ' values (%s,%s,%s,%s,%s,%s,%s) '
		# 执行sql语句
		cur.executemany(sql_string,totalList)
	    # 提交到数据库执行
		conn.commit()
	except MySQLdb.Error,msg:  
		print file_name+" insert data error"
	    # 发生错误时回滚
		conn.rollback()
		return 0
	#cur.close()
	#conn.close()
	return len(totalList)#返回文件插入的条数

amountOfInsert = 0#统计本次插入的总数
#获取路径下的所有文件				
def getfilelist(filepath, tabnum=0):#tabnum是终端输出的退格符个数
    #simplepath = os.path.split(filepath)[1]  
    #returnstr = simplepath+"目录<>"+"\n"  
    #returndirstr = ""  
    #returnfilestr = ""  
    global amountOfInsert
    filelist = os.listdir(filepath)
    root_name = filepath.split(sep)
    root_name = root_name[len(root_name)-1]
    one_file_insert = 0#一个文件夹里的数据插入的条数
    one_file_count = 0
    for num in range(len(filelist)):  
        filename=filelist[num]
        absolutePath = filepath+'/'+filename
        if os.path.isdir(absolutePath):  
            #returndirstr += "\t"*tabnum+getfilelist(filepath+"/"+filename, tabnum+1)  
            getfilelist(absolutePath, tabnum+1)
        else:
        	if config.keyWord in filename:#包含log的文件才插入数据库
        		one_file_insert += InsertDataFromFile(absolutePath,filename)
        		one_file_count += 1
        		#returnfilestr += "\t"*tabnum+filename+"\n"  
    print '\t'*tabnum+root_name+'文件夹总共插入数据:'+str(one_file_insert)+'\t,共读取了:'+str(one_file_count)+'个'+config.keyWord+'文件;'+'\n'
    amountOfInsert += one_file_insert
    #print amountOfInsert
    #returnstr += returnfilestr+returndirstr  
    #return returnstr+"\t"*tabnum+"</>\n"
createTable()
getfilelist(root)
print '本次一共插入数据：'+str(amountOfInsert)
cur.close()
conn.close()