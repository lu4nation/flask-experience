import MySQLdb
# db=MySQLdb.connect(passwd='admin',db="jogoteca", host="172.18.0.2")
print('Conectando...')
db=MySQLdb.connect(user="root", passwd='admin',db="jogoteca", host="127.0.0.1", port=3306)


cursor = db.cursor()
cursor.executemany(
      """INSERT INTO usuario (id, nome, senha)
      VALUES (%s, %s, %s)""",
      [
      ("admin", "John Snow", "lobo"),
      ("luan", "Luan Marques", "luan"),
      ("danilo", "Danilo", "teste")
      ])

cursor.execute('''select * from usuario''')
for user in cursor.fetchall():
    print(user[1] + ' AE!')
# print(cursor.fetchall())
# print(db)
