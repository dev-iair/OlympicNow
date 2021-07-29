import cx_Oracle as oci


oci.init_oracle_client(lib_dir=r"C:/Program Files/SQLPlus")
conn = oci.connect('admin/Dkdldpdjdb12@iairdb_medium')
cursor = conn.cursor()

cursor.execute("INSERT INTO OLPNOW_SPORTS VALUES (:RDATE, :SNAME, :SCOUNT)", [None, "양궁", 120])

conn.commit()