# Author: Elisson Rodrigo
# Date: 21 de Dezembro de 2023

import time
from libs import utils

def main():
    # Create the UDP socket
    utils.msg('INFO',f'Creating the socket...')
    conn = utils.createSocket()

    # Initialize the PWM values
    utils.msg('INFO', f'Generating the PWM values...')
    pwmValues = utils.generatePWMValues(utils.const.START_RANGE,
                                        utils.const.END_RANGE,
                                        utils.const.NUM_VALUES,
                                        utils.const.SEED_VALUE)
    
    # Initialize the log file
    log = []

    # Iterate over the PWM values
    utils.msg('INFO', f'Starting the PWM values iteration...\n')
    for pwm in pwmValues:
        # Start message time counter
        startTime = time.time()

        while True:
            time.sleep(utils.const.SLEEP_TIME)
            # Receive the message
            hasMsg, currentSpeed, pwms, desiredSpeed, timestamp = utils.recvSSLMessage(conn)
            if hasMsg:
                # Serialize the message
                log.append(utils.serializeMsgToLog(currentSpeed, pwms, desiredSpeed, timestamp))
                utils.msg('DATA', pwms)

            # Count time
            elapsedTime = time.time() - startTime

            # Check if the time has passed
            if elapsedTime > utils.const.TIME_BETWEEN_MSGS:
                # Send the PWM message
                for i in range(utils.const.MESSAGE_TIME):
                    utils.sendSSLPWMMessage(conn, pwm)
                utils.msg('DATA', f'Current PWM value: {pwm}')
                break

    # Save the log to a file
    if len(log) > 0:
        utils.saveLogToFile(log, utils.const.PWM_LOG_PREFIX, utils.const.PWM_LOG_EXTENSION)
    else:
        utils.msg('ERRO',f'No data to save to a file. Empty log!')