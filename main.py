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

# To print messages with color on console
from colorama import Fore

# Init driver var to use it as global
driver = None


def run():
    # Enter your credentials by console
    controlNumber = input("Número de control: ")
    password = input("Contraseña(default: 'holahola'):  ")

    # Initialize webdriver and execute signInEvaDoc function
    try:
        global driver
        driver = webdriver.Chrome()
        signInEvaDoc(controlNumber)
    except Exception as e:
        print(e)


def signInEvaDoc(controlNumber, password='holahola'):
    try:
        # Open a new tab with the specified web (maximized)
        driver.get('https://evadoc.culiacan.tecnm.mx/index.php')
        driver.fullscreen_window()

        # Locate the text fields to enter the credentials
        controlTxt = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "usuario3")))
        passwordTxt = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "pass3")))
        loginBtn = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "entra3")))

        # Write the credentials you enter in each text field and click login button
        controlTxt.send_keys(controlNumber)
        passwordTxt.send_keys(password)
        loginBtn.click()

        # An infinite loop to evaluate all the teachers (it ends when all teachers are evaluated)
        while 1:
            evaluate()
    except Exception as e:
        print(e)


def evaluate():
    try:
        # Locate "Evaluar" button and click on it
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "accion"))).click()

        # This int var is used to locate correctly each question by its index
        n = 0

        # A for cycle from 0 to 27 (because there are 27 questions)
        for questionNumber in range(0, 27):
            # Generate a random number to choose different options in each question ("Indeciso" option is the least likely)
            number = random.randint(0, 2 if questionNumber % 7 == 0 else 1)

            # Locate the first option of each question and click on it
            r = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "r" + str(n))))
            r.click()

            # If the random number is > 0, then press RIGHT key 'number' times
            for _ in range(0, number):
                r.send_keys(Keys.RIGHT)

            # We need to refresh the option selected to continue
            r = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "r" + str(n + number))))
            r.send_keys(Keys.SPACE)
            r.send_keys(Keys.TAB)

            # The first question option is always divisible by 5, so we add 5 at each end of question
            n += 5

        # Locate "Envio" button to submit our teacher evaluation
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "envio"))).click()
    except Exception:
        # Sign off of your account
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > table > tbody > tr:nth-child(8) > td > form > table > tbody > tr:nth-child(7) > td > table > tbody > tr > td > strong > font > a"))).click()
        driver.quit()
        print(f"\n{Fore.GREEN}It's done! Your teacher evaluation is complete! :)")
        exit(0)

if __name__ == "__main__":
    run()
