import pymysql

conn=pymysql.connect(host='your host name',user='your user name',password='your password',db='your db name',charset='utf8',autocommit=True)
curs=conn.cursor()

#sql=""
#curs.execute(sql)
#conn.commit()
#conn.close()
