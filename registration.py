#Инициализация программы, определение используемых в ней функций

# подключаем необходимые нам библиотеки для отправки почты и формирования случайных чисел
import smtplib, random, os

# имена файлов с регистрационными данными
emailfile ="email.txt"
loginfile ="login.txt"
passfile ="pass.txt"  

# откроем и закроем регистрационные файлы. Если их нет, они создадутся
f=open(emailfile,"a+")
f.close()
f=open(loginfile,"a+")
f.close()
f=open(passfile,"a+")
f.close

# функция отправки проверочного кода на указанный адрес
def code_to_mail (email_to):
    
    #формируем проверочный код случайным образом из указанного диапазона
    checkcode=random.randrange(10000,99999,1)
    
    #формируем необходимое для отправки почты тело письма 
    our_email="schoolcode61@gmail.com"
    subject="Регистрация/восстановление аккаунта"
    charset="Content-Type: text/plain; charset=utf-8"
    mime="MIME-Version: 1.0"
    text="Для регистрации/восстановления доступа к аккаунту введите код: "+str(checkcode)
    body="\r\n".join((f"From: {our_email}", f"To: {email_to}", f"Subject: {subject}", mime, charset, "", text))
    
    # пароль от нашего почтового ящика лежит в файле, чтобы не светить его в теле программы
    
    with open ("our_pass.txt") as f:
      our_pass=f.readline()

    # подключаемся к почтовому серверу
    smtp=smtplib.SMTP("smtp.gmail.com",587)
    smtp.starttls()
    smtp.ehlo()

    # логинимся на почтовом сервере
    smtp.login(our_email,our_pass)

    # пробуем отправить письмо
    smtp.sendmail(our_email,email_to, body.encode("utf-8"))

    # завершаем соединение
    smtp.quit()
    
    # передаем нашей функции строковое значение отправленного кода
    return str(checkcode)

# функция синтаксической проверки e-mail возвращает True, если данные синтаксис верен, иначе False
def email_ok (email):
    if email.find ("@") == -1 or email.find (".") == -1 or email.find (" ") != -1:
        return False
    else: return True

# процедура очистки экрана 
def clearscr ():
    os.system('cls' if os.name == 'nt' else 'clear')

# процедура записи регистрационных данных в файлы
def save(email,login,password):
    with open(emailfile,"a+") as f: 
                f.writelines (email+"\n")
    with open(loginfile,"a+") as f: 
                f.writelines (login+"\n")
    with open(passfile,"a+") as f: 
                    f.writelines (password+"\n")

# функция поиска пользователя по введенным логин и пароль в регистрационных файлах возвращает True, если найдены, иначе False
def exist_data (login, passw):
    with open(loginfile) as f:
        n = 0
        found_login = False
        for line in f:
            if login in line:
                found_login = True
                break
            n += 1
    if found_login:
        with open(passfile) as f:      
            password = f.readlines()[n]
        if passw+"\n"==password: return True
        else: return False
    else: return False

# функция поиска данных в регистрационных файлах возвращает True, если данные найдены, иначе False   
def exist_in_file (data, file):
    with open(file) as f:
        found = False
        for line in f:
            if data in line:
                found = True
                break
        return found 
# основное тело программы

while True:
    clearscr ()
    print("Введите:")
    print("1 - войти в систему")
    print("2 - зарегистрироваться в системе")
    print("3 - восстановить доступ к системе")
    print("0 - выход")
    choice=input()
    clearscr () 
    
    if str(choice) =="0": break # выбран выход
             
    if str(choice) =="1":  # выбран вход в систему 
        print ("Введите логин")
        login=input()
        print ("Введите пароль")
        password=input()
        clearscr()
        if exist_data (login, password):
            print ("Поздравляем, Вы удачно вошли в систему")
        else: print ("Пользователь с указанным логином и паролем не существует")

    if str(choice) =="2":  # выбрана регистрация в системе
        print ("Введите Ваш e-mail для регистрации")
        email=input()
        clearscr()
        if email_ok(email):
            if exist_in_file (email, emailfile):
                print ("Почта ", email, " уже используется в системе и не может быть использован повторно")
            else:
                codeout=code_to_mail(email)
                print ("Для проверки Вашего доступа к введенной почте ", email, " на неё был выслан код.")
                print ("Введите полученный код для продолжения регистрации.")
                codein=input()
                clearscr()
                # если удачно и код совпадает, продолжаем регистрацию
                if codein==codeout:
                    print ("Введите логин")
                    login=input()
                    clearscr()
                    if exist_in_file (login, loginfile):
                        print ("Данный логин уже используется в системе и не может быть использован повторно")
                    else:
                        while True:
                            print ("Введите пароль")
                            password=input()
                            clearscr()
                            print ("Повторите пароль")
                            password2=input()
                            clearscr()
                            if password==password2:
                                save(email,login,password)
                                print ("Поздравляем. Вы успешно зарегистрировались в системе")
                                break
                            else: print ("Пароли не совпадают")
                else:print("Неправильный код подтверждения e-mail")
        else: print("Ошибка в имени e-mail")

    if str(choice) =="3":  # выбрано восстановление доступа к системе
        print ("Введите Ваш e-mail, указанный при регистрации")
        email = input()
        clearscr()
        if email_ok(email):
            # поиск введенного e-mail в файле данных и сохранение номера строки под которым он записан
            with open(emailfile) as f:
                n = 0
                found = False
                for line in f:
                    if email in line:
                        accnumber = n
                        found = True
                        break
                    n += 1
            # если нашли e-mail в файле то отправляем проверочный код на e-mail и проверяем ввод этого кода
            if found:
                codeout=code_to_mail(email)
                print ("На почту ", email, "выслан код восстановления.")
                print ("Введите полученный код.")
                codein=input()
                # если удачно и код совпадает, достаем данные из файлов логинов и паролей и выводим их пользователю
                if codein==codeout:
                    with open(loginfile) as f:
                        login = f.readlines()[accnumber]     
                    with open(passfile) as f:      
                        password = f.readlines()[accnumber]
                    clearscr ()
                    print("Проверка произведена успешно")
                    print ()
                    print ("Ваш логин  в системе: ",login)
                    print ("Ваш пароль в системе: ",password)
                else: print ("Неправильный код")
            else:
                clearscr () 
                print ("Почта: ", email, " не зарегистрирована в системе")
        else: print("Ошибка в имени e-mail")
    print ("Для продолжения нажмите `Enter`")
    input()
clearscr ()
print ("Всего Вам доброго.")
print ("Для окончания работы нажмите `Enter`")
input()
