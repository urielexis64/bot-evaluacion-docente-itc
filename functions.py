import os, sys
from colorama import Fore

TITLE = f"""{Fore.LIGHTCYAN_EX}   Created by urielexis64{Fore.LIGHTBLUE_EX}\n
   ███████╗██╗░░░██╗░█████╗░██████╗░░█████╗░░█████╗░██████╗░░█████╗░████████╗
   ██╔════╝██║░░░██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝
   █████╗░░╚██╗░██╔╝███████║██║░░██║██║░░██║██║░░╚═╝██████╦╝██║░░██║░░░██║░░░
   ██╔══╝░░░╚████╔╝░██╔══██║██║░░██║██║░░██║██║░░██╗██╔══██╗██║░░██║░░░██║░░░
   ███████╗░░╚██╔╝░░██║░░██║██████╔╝╚█████╔╝╚█████╔╝██████╦╝╚█████╔╝░░░██║░░░
   ╚══════╝░░░╚═╝░░░╚═╝░░╚═╝╚═════╝░░╚════╝░░╚════╝░╚═════╝░░╚════╝░░░░╚═╝░░░\n
{Fore.LIGHTYELLOW_EX}DEBUGGING: En este modo se accede normalmente a la cuenta, pero no se
           envían las evaluaciones como tal, solo se simula que se hace.\n
{Fore.LIGHTYELLOW_EX}AUTOMÁTICO: Si está activado, se realizarán todas las evaluaciones de los
            maestros variando la opción elegida (Compl. de acuerdo,
            De acuerdo, Indeciso, etc.) con un valor default de 2 (Compl. 
            de acuerdo, De acuerdo, Indeciso).\n"""


#* Get absolute path to resource (PyInstaller)
def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

