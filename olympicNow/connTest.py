
import cx_Oracle as oci


oci.init_oracle_client(lib_dir=r"C:/Program Files/SQLPlus")
conn = oci.connect('admin/Dkdldpdjdb12@iairdb_medium')
cursor = conn.cursor()

cursor.execute("SELECT * FROM OLPNOW_PLAYERS")
for row in cursor:
    print(row)
print('======================================================================')
cursor.execute("SELECT * FROM OLPNOW_SPORTS")
for row in cursor:
    print(row)

conn.close()