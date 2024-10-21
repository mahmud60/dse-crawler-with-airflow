import psycopg2

conn = psycopg2.connect(host="localhost", dbname="dse", user="postgres", password="kratos", port=5432)

cur = conn.cursor()

conn.commit()

cur.close()
conn.close()

