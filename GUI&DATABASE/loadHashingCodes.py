import numpy as np
import pymysql
import sys
def fun(host,user,password):
	data32=np.load(r"..\yuhang\hashing_code_32.npz")
	train_data32=data32['output.npy']
	test_data32=data32['test_output.npy']
	data16=np.load(r"..\yuhang\hashing_code_16.npz")
	train_data16=data16['output.npy']
	test_data16=data16['test_output.npy']

	db=pymysql.connect(host,user,password,)
	cursor = db.cursor()
	cursor.execute("CREATE DATABASE IF NOT EXISTS yalefaces_database ")
	cursor.execute("USE yalefaces_database")
	#train_dataset32
	cursor.execute("DROP TABLE IF EXISTS TRAIN_DATASET32")
	create_sql="""CREATE TABLE TRAIN_DATASET32(
			HASH_CODE CHAR(32) NOT NULL,
			FILE_NAME CHAR(20) NOT NULL)"""
	cursor.execute(create_sql)
	list=[]
	train_data32[train_data32==-1]=0
	for i in range(train_data32.shape[0]):
		a=train_data32[i,:].astype(int).astype(str)
		s=''.join(a)
		list.append((s,"s"+str(i+1)+".bmp"))
	insert_sql="INSERT INTO TRAIN_DATASET32(HASH_CODE,FILE_NAME) VALUES (%s,%s)"
	try:
		cursor.executemany(insert_sql,list)
		db.commit()
	except:
		db.rollback()

	#test_dataset32
	cursor.execute("DROP TABLE IF EXISTS TEST_DATASET32")
	create_sql="CREATE TABLE TEST_DATASET32(" \
	           "HASH_CODE CHAR(32) NOT NULL," \
				"FILE_NAME CHAR(20) NOT NULL)"
	cursor.execute(create_sql)
	list=[]
	test_data32[test_data32==-1]=0
	for i in range(test_data32.shape[0]):
		a=test_data32[i,:].astype(int).astype(str)
		s=''.join(a)
		list.append((s,"t"+str(i+1)+".bmp"))
	insert_sql="INSERT INTO TEST_DATASET32(HASH_CODE,FILE_NAME) VALUES (%s,%s)"
	try:
		cursor.executemany(insert_sql,list)
		db.commit()
	except:
		db.rollback()

	#train_dataset16
	cursor.execute("DROP TABLE IF EXISTS TRAIN_DATASET16")
	create_sql="""CREATE TABLE TRAIN_DATASET16(
			HASH_CODE CHAR(16) NOT NULL,
			FILE_NAME CHAR(20) NOT NULL)"""
	cursor.execute(create_sql)
	list=[]
	train_data16[train_data16==-1]=0
	for i in range(train_data16.shape[0]):
		a=train_data16[i,:].astype(int).astype(str)
		s=''.join(a)
		list.append((s,"s"+str(i+1)+".bmp"))
	insert_sql="INSERT INTO TRAIN_DATASET16(HASH_CODE,FILE_NAME) VALUES (%s,%s)"
	try:
		cursor.executemany(insert_sql,list)
		db.commit()
	except:
		db.rollback()

	#test_dataset16
	cursor.execute("DROP TABLE IF EXISTS TEST_DATASET16")
	create_sql="CREATE TABLE TEST_DATASET16(" \
	           "HASH_CODE CHAR(16) NOT NULL," \
				"FILE_NAME CHAR(20) NOT NULL)"
	cursor.execute(create_sql)
	list=[]
	test_data16[test_data16==-1]=0
	for i in range(test_data16.shape[0]):
		a=test_data16[i,:].astype(int).astype(str)
		s=''.join(a)
		list.append((s,"t"+str(i+1)+".bmp"))
	insert_sql="INSERT INTO TEST_DATASET16(HASH_CODE,FILE_NAME) VALUES (%s,%s)"
	try:
		cursor.executemany(insert_sql,list)
		db.commit()
	except:
		db.rollback()


	cursor.close()
	db.close()

if __name__=='__main__':
	host=sys.argv[1]
	user=sys.argv[2]
	password=sys.argv[3]
	fun(host,user,password)