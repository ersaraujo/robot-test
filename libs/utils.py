# Author: Elisson Rodrigo
# Date: 21 de Dezembro de 2023

from socket import socket, AF_INET, SOCK_DGRAM
from colorama import Fore

import os
import random
import datetime
import numpy as np

from proto import commTypes_pb2 as pb
from utils import constants as const

def getLogsPath():
    return getFolderPath('data/logs')

def getPlotsPath():
    return getFolderPath('data/imgs')

def getInputPath():
    return getFolderPath('data/input')

def getDataPath():
    return getFolderPath('data')

def getFolderPath(subfolder):
    cur_path = os.getcwd()
    proj_path = os.path.abspath(os.path.join(cur_path, os.pardir))
    path = os.path.join(proj_path, subfolder)
    return path

def recvSSLMessage(udp_sock):
    msg = pb.protoMotorsDataSSL()
    hasMsg = False

    while True:
        try:
            data, _ = udp_sock.recvfrom(1024)
            msg.ParseFromString(data)
            hasMsg = True
        except:
            break
    
    currentSpeed = [msg.current_m1, msg.current_m2, msg.current_m3, msg.current_m4]
    pwms = [msg.pwm_m1, msg.pwm_m2, msg.pwm_m3, msg.pwm_m4]
    desiredSpeed = [msg.desired_m1, msg.desired_m2, msg.desired_m3, msg.desired_m4]
    timestamp = msg.msgTime

    return hasMsg, currentSpeed, pwms, desiredSpeed, timestamp

def sendSSLPWMMessage(udp_sock, pwm):
    msg = pb.protoMotorsPWMSSL()
    msg.m1 = pwm
    msg.m2 = pwm
    msg.m3 = pwm
    msg.m4 = pwm
    udp_sock.sendto(msg.SerializeToString(), (const.SERVER, const.PC_TO_ROBOT_PORT))

def serializeMsgToLog(currentSpeed, pwms, desiredSpeed, timestamp):
    return currentSpeed[0], currentSpeed[1], currentSpeed[2], currentSpeed[3], \
        pwms[0], pwms[1], pwms[2], pwms[3], \
        desiredSpeed[0], desiredSpeed[1], desiredSpeed[2], desiredSpeed[3], \
        timestamp

def generatePWMValues(start, end,count, seed):
    random.seed(seed)
    randomValues = [round(random.uniform(start, end), 1) for _ in range(count)]

    msg('DATA', f'Generated random PWM values:\n{randomValues}')
    # TODO:
    # 1. Save the random values to a file
    # 2. Add prints to debug

    return randomValues

def saveLogToFile(log, prefix=const.PWM_LOG_PREFIX, extension=const.PWM_LOG_EXTENSION):
    # Get the current date and time
    now = datetime.datetime.now()
    now_str = now.strftime("%Y-%m-%d_%H-%M-%S")

    # Create the file name
    file = getLogsPath + prefix + now_str + extension

    # Save the log to the file
    names = 'CURRENT_M1, CURRENT_M2, CURRENT_M3, CURRENT_M4, PWM_M1, PWM_M2, PWM_M3, PWM_M4, DESIRED_M1, DESIRED_M2, DESIRED_M3, DESIRED_M4, TIMESTAMP'
    np.savetxt(file, \
               log, 
               delimiter=',', 
               header=names)
    
def createSocket():
    # Initialize the UDP socket
    udp_sock = socket(AF_INET, SOCK_DGRAM)
    udp_sock.bind(('', const.ROBOT_TO_PC_PORT))
    udp_sock.settimeout(0)
    return udp_sock

def msg(prefix, msg):
    color_mapping = {
        'INFO': Fore.CYAN,
        'ERRO': Fore.RED,
        'DATA': Fore.YELLOW,
    }
    color = color_mapping.get(prefix, Fore.WHITE)
    print(f'{color}[{prefix}]{Fore.RESET} - {msg}')