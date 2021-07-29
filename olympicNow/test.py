import cx_Oracle as oci

oci.init_oracle_client(lib_dir=r"C:/Program Files/SQLPlus")

conn = oci.connect('admin/Dkdldpdjdb12@iairdb_medium')

cursor = conn.cursor()
cursor.execute("""
    SELECT CURRENT_DATE FROM DUAL
""")
for CURRENT_DATE in cursor:
    print(CURRENT_DATE)