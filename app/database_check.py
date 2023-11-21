import pymysql

conn = pymysql.connect(host='34.31.96.18', user='root', passwd='divyaansh', db='app')
cursor = conn.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print("Database version : %s " % data)
conn.close()
