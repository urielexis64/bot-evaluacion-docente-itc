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

from functions import resource_path
from db import insert
import sys

# Init driver var to use it as global
driver = None
control_number = 0
student_info = []
career = ''
teachers = []

c = 0
file_path = 'NUMEROS DE CONTROL.txt'

isDebugging = False
isAutomatic = False
isMultirun = True


def run():
    global control_number
    # Enter your credentials by console
    control_number = input("Por favor, ingresa tu número de control: ")
    # password = input("Contraseña(default: 'holahola'): ")

    # print("Perfecto! Ahora iniciaré sesión y empezaré a evaluar...")

    # Initialize webdriver and execute signInEvaDoc function
    try:
        global driver
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(resource_path('chromedriver.exe'), options=options)
        signInEvaDoc(control_number)
    except Exception as e:
        print(e)

def multirun():
    global control_number
    controlnumbers = open(file_path, 'r+')
    lines = controlnumbers.readlines()
    try:
        global driver
        lineNumber = 0
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(resource_path('chromedriver.exe'), options=options)
        for line in lines:
            control_number = line.split(' ')[0]
            signInEvaDoc(control_number)
            lineNumber += 1
            print(lineNumber)
    except Exception as e:
        pass


def signInEvaDoc(controlNumber, password='holahola'):
    try:
        # Open a new tab with the specified web (maximized)
        driver.get('https://evadoc.culiacan.tecnm.mx/index.php')

        # Locate the text fields to enter the credentials
        controlTxt = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "usuario3")))
        passwordTxt = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "pass3")))
        loginBtn = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "entra3")))

        # Write the credentials you enter in each text field and click login button
        controlTxt.send_keys(controlNumber)
        passwordTxt.send_keys(password)
        loginBtn.click()

        getInfo()

        # print(f"\nWow! Veo que serás un(a) gran ingeniero(a){career}\n")
        # An infinite loop to evaluate all the teachers (it ends when all teachers are evaluated)
        while student_info:
            evaluate()
    except:
        signoff(True, True)
        # driver.quit()
        # run()


def getInfo():
    global student_info, career, teachers

    student_info = driver.find_element_by_xpath("/html/body/table/tbody/tr[3]/td").text
    student_info = student_info.split('\n')

    if len(student_info) == 1:
        student_info.append('CARRERA NO ENCONTRADA')

    career = driver.find_element_by_xpath("/html/body/table/tbody/tr[3]/td/span").text
    career = (career[10:].lower() if len(career) != 0 else ' mecatrónico(a)') \
        if career[10:].lower()[-1:] not in ['a', 'o'] else career[10:].lower()[:-1] + 'o(a)'

    tempList = []
    teachers = driver.find_elements_by_class_name('estilo2')
    teachers.reverse()
    for t in range(len(teachers)):
        tempList.append(teachers.pop().text)
    teachers = tempList


def getStudentName():
    global student_info
    return student_info[0].split(" - ")[1]

def getStudentCareer():
    global student_info
    return student_info[1]


number = -1

xd = True

def evaluate():
    global number
    try:
        # Locate "Evaluar" button and click on it
        evaluateBtn = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "accion")))

        global xd
        if xd:
            print(student_info, end='')
            xd = False

        number = 2 if isAutomatic else getTeacher()

        evaluateBtn.click()

        # This int var is used to locate correctly each question by its index
        n = 0

        # A for cycle from 0 to 27 (because there are 27 questions)
        for questionNumber in range(27):
            max = getRandom(number)

            # Locate the first option of each question and click on it
            r = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "r" + str(n))))
            r.click()

            # If the random number is > 0, then press RIGHT key 'number' times
            for _ in range(max):
                r.send_keys(Keys.RIGHT)

            # We need to refresh the option selected to continue
            r = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "r" + str(n + max))))
            r.send_keys(Keys.SPACE)
            r.send_keys(Keys.TAB)

            # The first question option is always divisible by 5, so we add 5 at each end of question
            n += 5

        # Locate "Envio" button to submit our teacher evaluation
        if isDebugging:
            driver.find_element_by_xpath('//*[@id="evalua"]/p/input[2]').click()
        else:
            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "envio"))).click()

    except Exception as e:
        # Sign off of your account
        signoff(True if number == -1 else False, True)


def getTeacher():
    global c
    max = int(input(f"Qué opinas de \"{teachers[c]}\"? (1: Bueno, 2: Regular, 3: Malo) "))
    c += 1
    return max


def getRandom(max):
    # Generate a random number to choose different options in each question
    number = random.randint(0, max)
    return number


def signoff(alreadyEvaluated: bool, multi: bool):
    if not alreadyEvaluated:
        tmpStudentName = getStudentName()
        tmpCareer = getStudentCareer()
        tmpCtrlNumber = control_number
        insert(tmpCtrlNumber, tmpStudentName, tmpCareer)
        global number
        number = -1
    if not multi:
        print("Cerrando sesión...")
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/table/tbody/tr[2]/td[2]/strong/a"))).click()
        driver.quit()
        print(f"\nMuy bien, {getStudentName().title()}, ya quedó tu evaluación docente ;)")
        input("Presiona Enter para salir...")
        print("Hasta luego, gracias por utilizarme :)")
        sleep(2)
        sys.exit()

    global student_info, xd
    xd = True
    student_info = []
    try:
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr[2]/td[2]/strong/a'))).click()
    except:
        try:
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="reg"]/table/tbody/tr[2]/td[2]/strong/a'))).click()
        except:
            pass


if __name__ == "__main__":
    if input("DEBBUGING? (Y/N) ").lower() == 'y':
        isDebugging = True
    if input("Automático? (Y/N) ").lower() == 'y':
        isAutomatic = True
    if isMultirun:
        multirun()
    else:
        print("===== Hola! Es un gusto verte por acá. Si me permites, yo haré la evaluación docente por ti :D =====")
        run()
