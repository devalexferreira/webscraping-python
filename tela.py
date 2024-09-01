from main import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLineEdit, QLabel, QDialogButtonBox, QDialog, QApplication, QFileDialog
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from selenium.webdriver.common.by import By
import time
import re
from connection import Connection
from tables import Tables
from selenium import webdriver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
import sqlite3
from threading import Thread
import sys
from datetime import date
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders



class Tela(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(Tela, self).__init__(parent)
        Connection('sistema.db')
        Tables.createTableUltima()
        Tables.createTableSmtp()
        self.codvaga = 0
        self.load_ui()


    def load_ui(self):        
        self.setupUi(self) 
        self.setWindowTitle('Envios automáticos')             
        self.pushButton_2.clicked.connect(self.openFileNameDialog)
        self.pushButton_3.setEnabled(False)
        self.pushButton_3.clicked.connect(self.stop)
        self.pushButton.clicked.connect(self.send)
        self.pushButton_4.clicked.connect(self.saveSmtp)
        self.lineEdit_6.setEchoMode(QLineEdit.Password)
        validator = QRegExpValidator(QRegExp(r'[0-9]+'))
        self.lineEdit_2.setValidator(validator)
        self.curriculo = None  


    def saveSmtp(self):
        host = self.lineEdit_3.text()
        porta =self.lineEdit_5.text()
        email = self.lineEdit_4.text() 
        senha = self.lineEdit_6.text()
        if host != "" and porta != "" and email != "" and senha != "":
            conn = sqlite3.connect('sistema.db')
            cursor = conn.cursor()          


    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Selecionar arquivo", "","Pdf (*.pdf)", options=options)
        if fileName:
            path = Path(fileName)
            self.curriculo = path
            self.label_10.setText(str(path))


    def stop(self):
        self.stop_ = True
        self.pushButton.setEnabled(True)


    def send(self):
        self.pushButton_3.setEnabled(True)
        self.pushButton.setEnabled(False)
        self.label_6.setText(str(0))
        self.label_8.setText("0")
        descricao = self.lineEdit.text()
        # combinar = self.checkBox.isChecked()
        # print(combinar)
        result = self.getcod(descricao)
        print(descricao)
        print(result)
        sys.stdout.write("ss ")
        sys.stdout.flush()
        self.codvaga = 0
        for i in range(0, len(result)):
            self.codvaga = result[i][2]
        
        self.thread = Th(self.codvaga, descricao, self)
        self.thread.start()
        
                


    def getcod(self, descricao):
        conn = sqlite3.connect('sistema.db')
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * from busca where descricao = ?
        """,(descricao,))
        dados_ = cursor.fetchall()
        return dados_

    
    def informarSemVaga(self):
        dlg = CustomDialog()
        dlg.exec()


class Th(Thread):

    def __init__ (self, codigo, descricao, active=None):
        sys.stdout.write("Making thread number ")
        sys.stdout.flush()
        Thread.__init__(self)
        self.codigo = codigo
        self.active = active
        self.descricao = descricao
        self.urls= []
        self.conta = 0
        self.stop_ = False
        self.enviados = 0
        # options = Options()
        options = webdriver.FirefoxOptions()
        # options.add_argument("start-maximized")
        self.navegador = webdriver.Firefox(options=options)   
        

    def run(self):  
                                  
            self.navegador.get('https://empregacampinas.com.br')
            self.navegador.find_element(By.XPATH, '//*[@id="menu"]/form/div/div/input').send_keys(self.descricao)
            self.navegador.find_element(By.XPATH, '//*[@id="btn-search"]').click()
            self.stop_ = False
            num = 0
            hoje = date.today()
            while True:                
                time.sleep(7)
                results = self.navegador.find_elements(By.CLASS_NAME, "col-lg-12")
                self.conta = self.conta + len(results)
                self.active.label_6.setText(str(self.conta))                
                for element in results:
                    vaga = element.find_elements(By.CLASS_NAME, 'cod-vaga')
                    id_vaga = None
                    for v in vaga:
                        id_vaga = re.sub('[^0-9]', '', v.text)
                    if id_vaga == self.codigo:
                        self.stop_ = True
                        self.active.label_8.setText("Não há vagas para enviar")
                        # self.active.informarSemVaga()
                        break
                    elif num == 0:
                        conn = sqlite3.connect('sistema.db')
                        cursor = conn.cursor()
                        try:
                            if self.codigo != 0:
                                cursor.execute("""
                                UPDATE busca SET codigo = ? WHERE descricao = ? and codigo = ?
                                """, (id_vaga, self.descricao,self.codigo,))
                                conn.commit()
                            else:
                                cursor.execute("""
                                INSERT INTO busca (descricao, codigo)
                                VALUES (?,?)
                                """, (self.descricao,id_vaga,))
                                conn.commit()
                        except sqlite3.Error as er:
                            print(er)
                        conn.close()
                    link = element.find_elements(By.TAG_NAME, 'a')
                    txt_link = None
                    for l in link:
                        txt_link = l.get_attribute('href')
                        self.urls.append(txt_link)
                next = self.navegador.find_elements(By.CLASS_NAME, "nextpostslink")
                num += 1
                if self.stop_ == True:
                    break
                if num == 1:
                    break
                if len(next)> 0:
                    print(f"existe {len(next)}")
                    for c in next:
                        go = c.get_attribute('href')
                        self.navegador.get(go)
            for pg in self.urls:
                self.navegador.get(pg)
                result = self.navegador.find_elements(By.CLASS_NAME, "postie-post")
                for item in result:
                    p = item.find_elements(By.TAG_NAME, 'p')

                    #data, email, assunto vem de um p só
                    salario = None
                    data = None
                    try:
                        for pp in p:
                            if "Salário:" in pp.text:
                                salario = pp.text.split(":")[1].strip()   #3 
                                if "R$" in salario:
                                    salario = int(salario.split("R$ ")[1].split(",")[0].replace(".",""))
                            elif "Os interessados deverão" in pp.text:
                                data = pp.text[-11::].split(".")[0]
                                data = data.split("/")
                                data = date(int(data[2]),int(data[1]),int(data[0]))
                                assunto = pp.text.split("aos cuidados de")[1].split("para o e-mail")[0]
                                assunto_ =  pp.text.split("com a sigla")[1].split("no campo assunto")[0]
                                assunto = f"aos cuidados de {assunto} com a sigla {assunto_}"
                    
                        print(f"o salario eh isso {salario}")                   
                        print(f"a qtd de p é {len(p)}")                 
                        a  = item.find_elements(By.TAG_NAME, 'a')
                        email = None
                        for a_ in a:
                            email = a_.text 
                    except:
                        continue                   
                    
                    data = hoje
                    if hoje <= data:
                        if self.active.checkBox.isChecked() == True:
                            if salario == "a combinar":
                                #enviar o email
                                self.enviarEmail(email, assunto)
                                print("salario a combinar e o usuario aceitou")
                            elif self.active.lineEdit_2.text() != "":
                                if salario >= int(self.active.lineEdit_2.text()):
                                    #enviar o 
                                    self.enviarEmail(email, assunto)
                                    print("salario da vaga é maior ou igual ao salario que o usuario quer")
                                    pass
                            else:
                                self.enviarEmail(email, assunto)
                                print("salario é diferente de combinar e o usuario aceita a combinar e nao definiu valor minimo")
                                pass
                        else:
                            if self.active.lineEdit_2.text() != "":
                                if salario != "a combinar":
                                    if salario >= int(self.active.lineEdit_2.text()):
                                        #enviar o 
                                        self.enviarEmail(email, assunto)
                                        print("usuario nao aceita a combinar e o o salario é o que ele quer")
                            else:
                                if salario != "a combinar":
                                    #enviar o email
                                    self.enviarEmail(email, assunto)
                                    print("usuario nao aceita a combinar mais nao definiu valor minimo")
                        # [1].split("para o e-mail")[0]

                    print(email)
                    print(salario)
                    print(data)
                    print(assunto)
                    sys.stdout.flush()            
                break
            self.active.pushButton_3.setEnabled(False)
            self.active.pushButton.setEnabled(True)
            self.navegador.quit()


    


    def enviarEmail(self, email, assunto):        
        curriculo = self.active.label_10.text()
        print(curriculo)
        if curriculo != "":
            try:
                fromaddr = ""
                email = ''
                toaddr = email
                msg = MIMEMultipart()                 
                msg['From'] = fromaddr
                msg['To'] = toaddr
                msg['Subject'] = assunto
                body = """<html>
                    <head></head>
                    <body>
                        <p>Olá,<br>
                        Segue em anexo curriculo para vaga em questão.<br><br>
                        Desde já agradeço.
                        </p>
                    </body>
                    </html>
                    """
                msg.attach(MIMEText(body, 'html'))
                attachment = open(curriculo,'rb')
                part = MIMEBase('application', 'octet-stream')
                part.set_payload((attachment).read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', "attachment; filename= %s" % "curriculo.pdf")
                msg.attach(part)
                attachment.close()
                server = smtplib.SMTP('', 587)
                server.starttls()
                server.login(fromaddr, "")
                text = msg.as_string()
                server.sendmail(fromaddr, toaddr, text)
                server.quit()
                print('\nEmail enviado com sucesso!')
                self.enviados += 1
                self.active.label_8.setText(str(self.enviados))
            except smtplib.SMTPResponseException as e:
                error_code = e.smtp_code
                error_message = e.smtp_error
                print(error_message)
            

class CustomDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Atenção!")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Não há vagas para enviar o curriculo")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)



if __name__ == "__main__":
    app = QApplication([])
    w = Tela()
    w.show()
    p = w.palette()
    # p.setColor(w.backgroundRole(), Qt.white)
    w.setPalette(p)
    exit(app.exec_())