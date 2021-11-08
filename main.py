# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Time import (to wait n seconds)
from time import sleep

# Generate random numbers to decide each option pseudorandomly
import random

from functions import resource_path, TITLE
import os
from colorama import init, Fore
import requests

# Init driver var to use it as global
driver = None

# Student variables
control_number = 0
student_info = []
career = ''
teachers = []
comment = ''
currentTeacherIndex = 0
maxRightMovements = -1
minRightMovements = -1

# Variable modes
isDebugging = False
isAutomatic = False


def run():
    global control_number
    # Enter your credentials by console
    control_number = input("\nPor favor, ingresa tu número de control:\n>>> ")
    password = input("Contraseña: (Enter = holahola)\n>>> ")

    print("\nPerfecto! Ahora iniciaré sesión y empezaré a evaluar...")

    # Initialize webdriver and execute signInEvaDoc function
    try:
        global driver
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(resource_path('chromedriver.exe'), options=options)
        signInEvaDoc(control_number, password)
    except Exception as e:
        print(e)


def signInEvaDoc(controlNumber, password):
    try:
        # Open a new tab with the specified web (maximized)
        driver.get('https://evadoc.culiacan.tecnm.mx/index.php')

        # Locate the text fields to enter the credentials
        controlTxt = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "usuario3")))
        passwordTxt = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "pass3")))
        loginBtn = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "entra3")))

        # Write the credentials you enter in each text field and click login button
        controlTxt.send_keys(controlNumber)
        passwordTxt.send_keys(password or 'holahola')
        loginBtn.click()

        # get info about current student
        getInfo()

        print(f"\nWow! Veo que serás un(a) gran ingeniero(a){career}\n")

        # An infinite loop to evaluate all the teachers (it ends when all teachers are evaluated)
        while 1:
            evaluate()
    except Exception:
        print('Parece que ingresaste un número de control inválido.\nIntenta de nuevo.')
        driver.quit()
        run()
    except SystemExit:
        raise SystemExit


def evaluate():
    global maxRightMovements, comment, minRightMovements
    try:
        comment = ''

        # Locate "Evaluar" button and click on it
        evaluateBtn = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "accion")))

        # Assign a default number (automatic) or the one you enter for each teacher
        # This number is used to decide among all the options (with index 0-5)
        teacherRate = getTeacherRate() if not isAutomatic else ''
        maxRightMovements = 2 if isAutomatic else teacherRate

        if maxRightMovements in [1, 2]:
            minRightMovements = 0
        else:
            maxRightMovements += 1
            minRightMovements = 2

        if teacherRate == 1:
            comment = 'Excelente docente.'
        elif teacherRate == 3:
            comment = 'Pésimo docente.'

        evaluateBtn.click()

        # This int var is used to locate correctly each question by its index
        questionIndex = 0

        # A for cycle from 0 to 28 (because there are 28 questions)
        for questionNumber in range(28):

            currentQuestionMovements = getRandom(minRightMovements, maxRightMovements)

            # Locate the first option of each question and click on it
            option = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "r" + str(questionIndex))))
            option.click()

            # If the random number is > 0, then press RIGHT key 'number' times
            for _ in range(currentQuestionMovements):
                option.send_keys(Keys.RIGHT)

            # We need to refresh the option selected to continue
            option = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "r" + str(questionIndex + currentQuestionMovements))))
            option.send_keys(Keys.SPACE)
            option.send_keys(Keys.TAB)

            # The first question option is always divisible by 5, so we add 5 at each end of question
            questionIndex += 5

        commentArea = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="sComentarios"]')))
        commentArea.click()
        commentArea.send_keys(comment)

        if isDebugging:
            # If debugging, click on  Cancelar" button
            driver.find_element_by_xpath('//*[@id="evalua"]/p/input[2]').click()
        else:
            # Or locate "Envio" button to submit our teacher evaluation
            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "envio"))).click()

    except Exception as e:
        # Sign off of your account
        print(e)
        signoff(maxRightMovements == -1)


def getInfo():
    global student_info, career, teachers

    student_info = driver.find_element_by_xpath("/html/body/table/tbody/tr[3]/td").text
    student_info = student_info.split('\n')

    if len(student_info) == 1:
        student_info.append('CARRERA NO ENCONTRADA')

    career = driver.find_element_by_xpath("/html/body/table/tbody/tr[3]/td/span").text
    career = (career[10:].lower() if len(career) != 0 else ' mecatrónico(a)') \
        if career[10:].lower()[-1:] not in ['a', 'o'] else career[10:].lower()[:-1] + 'o(a)'

    teachers = driver.find_elements_by_class_name('estilo2')
    for t in range(len(teachers)):
        teachers[t] = teachers[t].text


def getTeacherRate():
    global currentTeacherIndex
    while 1:
        rate = int(input(f"{Fore.WHITE}¿Qué opinas de \"{teachers[currentTeacherIndex]}\"? (1: Bueno, 2: Regular, 3: Malo)\n>>> "))
        if rate not in [1, 2, 3]:
            print(f'{Fore.RED}Solo valores del 1 al 3')
        else:
            break
    currentTeacherIndex += 1
    return rate


def getRandom(min, max):
    # Generate a random number to choose different options in each question
    number = random.randint(min, max)
    return number


def getStudentName():
    return student_info[0].split(" - ")[1]


def getStudentCareer():
    return student_info[1]

def signoff(alreadyEvaluated: bool):
    if not alreadyEvaluated:
        print("Cerrando sesión...")
        # Locate 'Cerrar sesión' button ad click on it
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/table/tbody/tr[2]/td[2]/strong/a"))).click()
        driver.quit()
        print(f"\nMuy bien, {getStudentName().title()}, ya quedó tu evaluación docente ;)\n")
    else:
        print("Hmm... parece que ya habías realizado tu evaluación docente. Qué responsable.\n")
        driver.quit()

    if input("¿Quieres realizar otra evaluación? (S = Sí | N = No)\n>>> ").lower() == 's':
        reset()
    else:
        print("Hasta luego, gracias por utilizarme :)")
        sleep(2)
        raise SystemExit

def reset():
    global currentTeacherIndex, maxRightMovements
    currentTeacherIndex = 0
    maxRightMovements = -1
    run()

def downloadChromedriver():
    print(f"{Fore.GREEN}Verificando última versión de chromedriver.")
    print("Por favor, espere...\n")
    print(f"{Fore.YELLOW}Presiona Ctrl + C para saltarte esta verificación.")

    download_url = 'https://github.com/urielexis64/bot-evaluacion-docente-itc/raw/main/chromedriver.exe'
    r = requests.get(download_url, allow_redirects=True)

    with open('chromedriver.exe', 'wb') as chromedriver:
        chromedriver.write(r.content)

if __name__ == "__main__":
    init(convert=True)
    try:
        downloadChromedriver()
    except KeyboardInterrupt:
        raise SystemExit
    finally:
        # for windows OS
        if os.name == "nt":
            os.system("cls")
        # for linux / Mac OS
        else:
            os.system("clear")

        os.system('mode 85, 40')
        print(TITLE)
        print(f"{Fore.LIGHTWHITE_EX}DEBBUGING? (Y/N)\n>>>  ", end='')
        if input().lower() == 'y':
            isDebugging = True
        if input("Automático? (Y/N)\n>>> ").lower() == 'y':
            isAutomatic = True
        run()
