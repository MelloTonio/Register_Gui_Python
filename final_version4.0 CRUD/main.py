from PyQt5 import uic, QtWidgets, QtGui #pip install PyQt5 
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox
import sqlite3
import time
from converted_medias import resources
from converted_medias import resources2
from validate_email import validate_email
from time import sleep



#Inicializa o contador de deletados para evitar futuros erros
conn = sqlite3.connect('databases/banco.db')
cursor = conn.cursor()
cursor.execute('''SELECT * FROM contador_deletados''')
for row, form in enumerate(cursor):
    contador_deletados = (form[0])
name = ''
conn.close()

#Insere Usuários no DB e atualiza os ids quando necessário
def captura_dados():
    global contador_deletados
    rows = 0
    conn = sqlite3.connect('databases/banco.db')
    cursor = conn.cursor()
    usuario = newwindow.lineEdit.text()
    senha = newwindow.lineEdit_2.text()
    repetir_senha = newwindow.lineEdit_3.text()
    try:
        x = int(senha)
        if validate_email(repetir_senha,verify=True):
            if len(usuario) == 0 or len(senha) == 0 or len(repetir_senha) == 0:
                QMessageBox.warning(QMessageBox(),'Aviso!','Os campos não podem ser vazios')
            else:
                lista = [(usuario,senha,repetir_senha)]
                cursor.executemany("""
                INSERT INTO usuarios (nome, idade, email)
                VALUES (?,?,?)
                """,lista)
                conn.commit()
                lista = []
                QMessageBox.information(QMessageBox(),'Sucesso!','Usuário cadastrado com sucesso no banco de dados')
                newwindow.lineEdit_2.setText('')
                newwindow.lineEdit_3.setText('')
                cursor.execute('''SELECT * FROM usuarios''')
                for row, form in enumerate(cursor):
                    rows += 1
                tablewidget.setRowCount(rows)
                cursor.execute('''SELECT * FROM contador_deletados''')
                for row, form in enumerate(cursor):
                    contador_deletados = (form[0])
                cursor.execute('''SELECT * FROM usuarios''')
                if contador_deletados >= 1:
                    data = [(contador_deletados),(usuario)]
                    cursor.execute("Update or Ignore usuarios set id = id - ? where nome = ?",data)
                    conn.commit()
                newwindow.lineEdit.setText('')
                rows = 0
                for row, form in enumerate(cursor):
                    for column, item in enumerate(form):
                        tablewidget.setItem(row, column, QTableWidgetItem(str(item)))
                conn.close()
        else:
            QMessageBox.warning(QMessageBox(),'Informação Inválida','Email inválido')
    except:
        QMessageBox.warning(QMessageBox(),'Informação Inválida','Idade inválida')


#Da um refresh no DB e passa para a TableWidget com todas informações
def atualiza_dados():
    conn = sqlite3.connect('databases/banco.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM usuarios''')
    tablewidget.setRowCount(cursor.rowcount)
    for row, form in enumerate(cursor):
        for column, item in enumerate(form):
            tablewidget.setItem(row, column, QTableWidgetItem(str(item)))
    conn.close()

def mostra_detalhes():
    about.show()

#Cadastra usuarios na interface externa
def cadastra_usuario():
    conn = sqlite3.connect('databases/login.db')
    cursor = conn.cursor()
    usuario = web2.lineEdit_4.text()
    senha = web2.lineEdit_3.text()
    repetir_senha = web2.lineEdit_5.text()
    if senha != repetir_senha:
        QMessageBox.warning(QMessageBox(),'Erro','As senhas devem ser iguais!')
    if len(usuario) == 0 or len(senha) == 0 or len(repetir_senha) == 0:
        QMessageBox.warning(QMessageBox(),'Erro','Os campos não podem estar vazios!')
    else:
        lista = [(usuario,senha)]
        cursor.executemany("""
        INSERT INTO cadastro (Usuario, Senha)
        VALUES (?,?)
        """,lista)
        QMessageBox.information(QMessageBox(),'Sucesso','Seu cadastro foi realizado com sucesso!')
        web2.lineEdit_4.setText('')
        web2.lineEdit_3.setText('')
        web2.lineEdit_5.setText('')
        conn.commit()
        conn.close()

#Loga o usuário da interface externa para interna
def loga_usuario():
    usuario = web2.lineEdit_11.text()
    senha = web2.lineEdit_12.text()
    login = (usuario,senha)
    conn = sqlite3.connect('databases/login.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM cadastro''')
    ok = False
    for user in cursor:
        if user == login:
            ok = True
    if ok == True:
        name = usuario
        nova_aba(ok,name)
        conn.close()
        return
    else:
        QMessageBox.warning(QMessageBox(),'Erro','Registro não encontrados na base de dados!')
        conn.close()

#Maneja ações da interface interna
def nova_aba(ok,name):
    web2.close()
    web.lineEdit_4.setText(f'Bem vindo {name.capitalize()}...')
    conn = sqlite3.connect('databases/banco.db')
    cursor = conn.cursor()
    web.show()
    cursor.execute("""
    SELECT * FROM usuarios;
    """)
    cont = 0
    for linha in cursor.fetchall():
        cont += 1
    tablewidget.setRowCount(cont)
    web.pushButton_2.clicked.connect(atualiza_dados)
    newwindow.pushButton.clicked.connect(captura_dados)
    web.setStyleSheet(open('css_file/style.css').read())
    conn.close()

def adiciona_usuario():
    newwindow.show()

#Deleta todos Usuários do banco de dados
def deleteAll():
    global contador_deletados
    button = QMessageBox.question(QMessageBox(),'AVISO','Tem certeza que deseja apagar todos os dados?',QMessageBox.Yes | QMessageBox.No)
    if button == QMessageBox.Yes:    
        conn = sqlite3.connect('databases/banco.db')
        c = conn.cursor()
        c.execute('DELETE FROM usuarios;',)
        conn.commit()
        QMessageBox.information(QMessageBox(),'Sucesso','Dados apagados com sucesso!')
        c.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='usuarios';",)
        conn.commit()
        tablewidget.setRowCount(0)
        c.execute("UPDATE contador_deletados SET deletados = 0")
        conn.commit()
        contador_deletados = 0
        conn.close()
    if button == QMessageBox.No:
        pass

def mostra_delete():
    delesp.show()

#Deleta um Usuário específico pelo seu ID
def deleta_especifico():
    global contador_deletados
    rows = 0 
    usuario_deletado = delesp.spinBox.text()
    conn = sqlite3.connect('databases/banco.db')
    c = conn.cursor()
    exists = c.execute("SELECT * from usuarios WHERE id="+(usuario_deletado))
    yes = 0
    for element in exists.fetchall():
        yes += 1
    if (yes > 0):
        c.execute("DELETE from usuarios WHERE id="+(usuario_deletado))
        conn.commit()
        c.execute("Update or Ignore usuarios set id = id-1 where id > 1")
        conn.commit()
        deletado = True
        c.execute("UPDATE contador_deletados SET deletados = deletados + 1")
        for row, form in enumerate(c):
            contador_deletados = (form[0])
        conn.commit()
        c.execute('''SELECT * FROM usuarios''')
        for row, form in enumerate(c):
            rows += 1
        tablewidget.setRowCount(rows)
        atualiza_dados()
        conn.close()
        return
    else:
        QMessageBox.warning(QMessageBox(),'Erro','Id inexistente na base de dados!')

def mostra_busca_usuario():
    search.show()

idglobal = 0

#Busca um Usuário específico pelo seu ID
def busca_usuario():
    global idglobal
    try:
        busca = search.spinBox.text()
        conn = sqlite3.connect('databases/banco.db')
        c = conn.cursor()
        exists = c.execute("SELECT * from usuarios WHERE id="+(busca))
        idglobal = busca
        busca = exists.fetchone()
        details.show()
        details.lineEdit.setText(busca[0])
        details.lineEdit_2.setText(str(busca[1]))
        details.lineEdit_3.setText(busca[2])
        conn.close()
    except:
        details.lineEdit.setText('')
        details.lineEdit_2.setText('')
        details.lineEdit_3.setText('')
        QMessageBox.warning(QMessageBox(),'Erro','Usuário não encontrado!')
        conn.close()
        details.close()

#Altera informações de um Usuário específico pelo seu ID
def altera_especifico():
    global idglobal
    nome = details.lineEdit.text()
    idade = details.lineEdit_2.text()
    email = details.lineEdit_3.text()
    try:
        x = int(idade)
        if validate_email(email,verify=True):
            conn2 = sqlite3.connect('databases/banco.db')
            cursor = conn2.cursor()
            conjunto = [nome,idade,email,idglobal]
            cursor.execute("UPDATE usuarios SET (nome,idade,email) = (?,?,?) where id=?",conjunto)
            conn2.commit()
    except:
        QMessageBox.warning(QMessageBox(),'Erro','Idade inválida!')

#Inicialização do App
app = QtWidgets.QApplication([])

#Interface com informações sobre o Dev.
about = uic.loadUi('ui_files/about.ui')
about.setStyleSheet(open('css_file/style.css').read())
about.setFixedSize(262, 396)
#---------------------------------------------------#
#Interface para adicionar Usuários
newwindow = uic.loadUi('ui_files/newwindow.ui')
newwindow.setFixedSize(307, 299)
#---------------------------------------------------#


#---------------------------------------------------#
#Interface Externa(Login) - Apenas Login e Cadastro
web2 = uic.loadUi('ui_files/Interface_externa.ui')
web2.setFixedSize(290, 325)
web2.pushButton.clicked.connect(cadastra_usuario)
web2.pushButton_2.clicked.connect(loga_usuario)
web2.setStyleSheet(open('css_file/style.css').read())
#---------------------------------------------------#


#---------------------------------------------------#
#Interface Interna - Deleta Usuários/Busca Usuários/Adiciona Usuários
#                    Altera Usuários
web = uic.loadUi('ui_files/Interface_interna.ui')
web.setFixedSize(521, 507)
web.menuBar.triggered.connect(mostra_detalhes)

web.pushButton_6.clicked.connect(mostra_busca_usuario)
web.pushButton_3.clicked.connect(deleteAll)
web.pushButton_4.clicked.connect(adiciona_usuario)
web.pushButton_5.clicked.connect(mostra_delete)

tablewidget = web.tableWidget
tablewidget.setFixedSize(481, 281)
#---------------------------------------------------#


#---------------------------------------------------#
#Função que deleta um Usuário em especifico pelo seu ID
delesp = uic.loadUi('ui_files/delete.ui')
delesp.pushButton.clicked.connect(deleta_especifico)
delesp.setFixedSize(189, 193)
#---------------------------------------------------#


#--------------------------------------------------#
#Interface ''Dados sobre o Usuário'' - Indica o Nome,idade e email do Usuário
details = uic.loadUi('ui_files/details.ui')
details.pushButton.clicked.connect(altera_especifico)
#---------------------------------------------------#


#---------------------------------------------------#
#Interface de ''Busca'' - Busca Usuários no banco de dados
search = uic.loadUi('ui_files/search.ui')
search.setFixedSize(225, 182)
search.pushButton.clicked.connect(busca_usuario)
#---------------------------------------------------#

web2.show()
app.exec()
