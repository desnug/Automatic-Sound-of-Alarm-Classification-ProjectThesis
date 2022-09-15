from rpi_lcd import LCD
from signal import signal, SIGTERM, SIGHUP, pause
import os
import sys
import getopt
import signal
import time
from edge_impulse_linux.audio import AudioImpulseRunner

import smbus
import sys

runner = None

DEVICE_BUS = 1
DEVICE_ADDR = 0x10
RELAY1 = 0x01
RELAY2 = 0x02
RELAY3 = 0x03
RELAY4 = 0x04
bus = smbus.SMBus(DEVICE_BUS)


def signal_handler(sig, frame):
    print('Interrupted')
    if (runner):
        runner.stop()
    sys.exit(0)


# lib LCD 16x2
lcd = LCD()


def safe_exit(signum, frame):
    exit(1)


signal.signal(signal.SIGINT, signal_handler)


def help():
    print('python classify.py <path_to_model.eim> <audio_device_ID, optional>')


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h", ["--help"])
    except getopt.GetoptError:
        help()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            help()
            sys.exit()

    if len(args) == 0:
        help()
        sys.exit(2)

    model = args[0]

    dir_path = os.path.dirname(os.path.realpath(__file__))
    # dir_path = ("mfe_model.eim")
    modelfile = os.path.join(dir_path, model)

    with AudioImpulseRunner(modelfile) as runner:
        try:
            model_info = runner.init()
            labels = model_info['model_parameters']['labels']
            print('Loaded runner for "' +
                  model_info['project']['owner'] + ' / ' + model_info['project']['name'] + '"')

            # Let the library choose an audio interface suitable for this model, or pass device ID parameter to manually select a specific audio interface
            selected_device_id = None
            if len(args) >= 2:
                selected_device_id = int(args[1])
                print("Device ID " + str(selected_device_id) +
                      " has been provided as an argument.")

            for res, audio in runner.classifier(device_id=selected_device_id):
                print('(%d ms.) Listening: ' % (
                    res['timing']['dsp'] + res['timing']['classification']), end='')
                for label in labels:
                    score = res['result']['classification'][label]
                    #print('%s: %.2f\t' % (label, score), end=' ')

                    if label == "danger_alarm" and score >= 0.7:
                        print('%s detected!! --> prob: %.2f\t' %
                              (label, score))
                        bus.write_byte_data(DEVICE_ADDR, RELAY1, 0xFF)
                        bus.write_byte_data(DEVICE_ADDR, RELAY2, 0x00)
                        bus.write_byte_data(DEVICE_ADDR, RELAY3, 0x00)
                        bus.write_byte_data(DEVICE_ADDR, RELAY4, 0x00)

                        lcd.text("Danger Alarm!!", 1)
                        lcd.text("Prob.: %.2f" % (score), 2)

                    elif label == "fire_alarm" and score >= 0.7:
                        print('%s detected!! --> prob: %.2f\t' %
                              (label, score))
                        bus.write_byte_data(DEVICE_ADDR, RELAY1, 0x00)
                        bus.write_byte_data(DEVICE_ADDR, RELAY2, 0xFF)
                        bus.write_byte_data(DEVICE_ADDR, RELAY3, 0x00)
                        bus.write_byte_data(DEVICE_ADDR, RELAY4, 0x00)

                        lcd.text("Fire Alarm!!", 1)
                        lcd.text("Prob.: %.2f" % (score), 2)

                    elif label == "gas_alarm" and score >= 0.7:
                        print('%s detected!! --> prob: %.2f\t' %
                              (label, score))
                        bus.write_byte_data(DEVICE_ADDR, RELAY1, 0x00)
                        bus.write_byte_data(DEVICE_ADDR, RELAY2, 0x00)
                        bus.write_byte_data(DEVICE_ADDR, RELAY3, 0xFF)
                        bus.write_byte_data(DEVICE_ADDR, RELAY4, 0x00)

                        lcd.text("Gas Alarm!!", 1)
                        lcd.text("Prob.: %.2f" % (score), 2)

                    elif label == "tsunami_alarm" and score >= 0.7:
                        print('%s detected!! --> prob: %.2f\t' %
                              (label, score))
                        bus.write_byte_data(DEVICE_ADDR, RELAY1, 0x00)
                        bus.write_byte_data(DEVICE_ADDR, RELAY2, 0x00)
                        bus.write_byte_data(DEVICE_ADDR, RELAY3, 0x00)
                        bus.write_byte_data(DEVICE_ADDR, RELAY4, 0xFF)

                        lcd.text("Tsunami Alarm!!", 1)
                        lcd.text("Prob.: %.2f" % (score), 2)

                    elif label == "non_alarm" and score >= 0.6:
                        #print('%s --> prob: %.2f\t' % (label, score))
                        print("Standby...")
                        bus.write_byte_data(DEVICE_ADDR, RELAY1, 0x00)
                        bus.write_byte_data(DEVICE_ADDR, RELAY2, 0x00)
                        bus.write_byte_data(DEVICE_ADDR, RELAY3, 0x00)
                        bus.write_byte_data(DEVICE_ADDR, RELAY4, 0x00)

                        lcd.text("Status:", 1)
                        lcd.text("Standby...", 2)
                print('', flush=True)

        finally:
            if (runner):
                runner.stop()
                # lcd.clear()
                lcd.text("Stop machine", 2)


if __name__ == '__main__':
    main(sys.argv[1:])
