import MySQLdb
print('Conectando...')
conn = MySQLdb.connect(user='root', passwd='admin', db='jogoteca', host='127.0.0.1', port=3306)
cursor = conn.cursor()

# inserindo usuarios
cursor.executemany(
      'INSERT INTO usuario (id, nome, senha) VALUES (%s, %s, %s)',
      [
            ('admin', 'Nico', 'caelum'),
            ('luan', 'Luan Marques', 'flask'),
            ('danilo', 'Danilo', 'vegas')
      ])

cursor.execute('select * from usuario')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo jogos
cursor.executemany(
      'INSERT INTO jogo (nome, categoria, console) VALUES (%s, %s, %s)',
      [
            ('God of War', 'Ação', 'Xbox One'),
            ('NBA 2k18', 'Esporte', 'Xbox One'),
            ('Rayman Legends', 'Indie', 'PS4'),
            ('Super Mario RPG', 'RPG', 'SNES'),
      ])

cursor.execute('select * from jogo')
print(' -------------  Jogos:  -------------')
for jogo in cursor.fetchall():
    print(jogo[1])

# commitando senão nada tem efeito
conn.commit()
cursor.close()

