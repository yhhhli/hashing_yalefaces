import sys
import numpy as np
import pymysql

def fun(absoluteFilePath,host,user,password):
	db = pymysql.connect(host, user, password, "yalefaces_database")
	cursor = db.cursor()
	if(len(absoluteFilePath)>=6 and(absoluteFilePath[-6]=='s' or absoluteFilePath[-6]=='t')):
		segment=-6
	elif(len(absoluteFilePath)>=7 and (absoluteFilePath[-7]=='s'or absoluteFilePath[-7]=='t')):
		segment=-7
	s=absoluteFilePath[segment:]
	if(s[0]=='s'):
		select_sql="SELECT HASH_CODE FROM TRAIN_DATASET16 WHERE FILE_NAME = '%s'" %s
	elif(s[0]=='t'):
		select_sql="SELECT HASH_CODE FROM TEST_DATASET16 WHERE FILE_NAME = '%s'" % s
	else:
		print("未找到该文件")
		return
	try:
		cursor.execute(select_sql)
		target_hash_code_str=cursor.fetchone()[0]
		target_hash_code = np.ones(len(target_hash_code_str))
		for i in range(len(target_hash_code_str)):
			if (target_hash_code_str[i] == '0'):
				target_hash_code[i] = -1
	except:
		print("未找到该文件")
		return

	select_sql="SELECT * FROM TRAIN_DATASET16"
	cursor.execute(select_sql)
	train_hash_codes=cursor.fetchall()
	dis=np.zeros(len(train_hash_codes))
	for i in range(len(train_hash_codes)):
		cur_code_str=train_hash_codes[i][0]
		cur_code=np.ones(len(cur_code_str))
		for j in range(len(cur_code_str)):
			if(cur_code_str[j]=='0'):
				cur_code[j]=-1
		a=np.dot(cur_code,target_hash_code)
		dis[i]=a
	index=np.argsort(dis)
	list=[]
	for i in range(9):
		list.append(absoluteFilePath[0:segment]+"s"+str(index[index.shape[0]-1-i]+1)+".bmp")
	return list

if __name__=='__main__':
	s=sys.argv[1]
	host=sys.argv[2]
	user=sys.argv[3]
	password=sys.argv[4]
	list=fun(s,host,user,password)
	for i in range(9):
		print(list[i])