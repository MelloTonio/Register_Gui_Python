    conn2 = sqlite3.connect('databases/banco.db')
            cursor = conn2.cursor()
            conjunto = [nome,idade,email,idglobal]
            cursor.execute("UPDATE usuarios SET (nome,idade,email) = (?,?,?) where id=?",conjunto)
            conn2.commit()