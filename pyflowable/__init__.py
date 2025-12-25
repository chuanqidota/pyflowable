import pymysql

pymysql.install_as_MySQLdb()

#  关键：设置版本信息，欺骗 Django 版本检查
pymysql.version_info = (2, 2, 1, "final", 0)
