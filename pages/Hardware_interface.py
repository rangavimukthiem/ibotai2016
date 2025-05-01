


import serial
from MyWidgets import CustomExceptionLogBox

def send_signal_to_hardware(self, class_id):
    try:
        arduino = serial.Serial('COM3', 9600, timeout=1)
        arduino.write(str(class_id).encode())
        arduino.close()
        CustomExceptionLogBox.log(f"Signal sent to hardware: {class_id}")
        print(f"Signal sent to hardware: {class_id}")
    except Exception as e:
        CustomExceptionLogBox.log(f"Error communicating with hardware: {e}")

