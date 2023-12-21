# Author: Elisson Rodrigo
# Date: 21 de Dezembro de 2023

import os
import sys
libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'libs'))
sys.path.append(libs_dir)

def list_options():
    print("\n1. Executar runPWMData.py")
    print("0. Sair\n")

def execute_option(option):
    if option == "1":
        from src import runPWMData
        runPWMData.main()
    elif option == "0":
        print("Saindo.")
        sys.exit()
    else:
        print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    while True:
        list_options()
        user_choice = input("Digite o número da opção desejada: ")
        execute_option(user_choice)
