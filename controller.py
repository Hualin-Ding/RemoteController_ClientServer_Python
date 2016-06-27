#!usr/bin/env python

# Client/controller program
import fcntl
import os
import signal
import socket
import sys
import termios
import time
from ast import literal_eval

HOST = socket.gethostname()  # get local machine host name
PORT = 12345  # give a random port number
remote_controller_battery = 100  # default remote controller battery
dict_btn = {'u': 'Up', 'd': 'Down', 'r': 'Repeat', '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
            '8': 8, '9': 9}  # button dictionary for the remote controller


# 8. Handle ctrl-c entered by user at runtime and print Interrupt, NOT kill the current process
def signal_handler(_signal, _frame):
    print("Interrupt")

signal.signal(signal.SIGINT, signal_handler)


def battery_charge(controller_battery):
    """
    5. Allow the user to recharge the battery
    :param controller_battery: int
    :return: controller_battery: int
    """
    if controller_battery < 100:
        controller_battery = 100
    return controller_battery


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a socket object
client_socket.connect((HOST, PORT))  # connect to host through the given port
connect_time = client_socket.recv(1024)  # Receive no more than 1024 bytes
# 1.Print time (EPOCH) of connection established
print("The connection established at %s" % connect_time + "\n")

# remote controller usage
print("### Remote Controller Usage ###\n" + "\tU <--> Up\n" + "\tD <--> Down\n" + "\tR <--> Repeat\n" +
      "\tM <--> To query for most pressed button and how many times it was pressed\n" +
      "\tL <--> To query for least pressed button and how many times it was pressed\n" +
      "\tA <--> To activate an alarm on the server\n" +
      "\tZ <--> To deactivate an alarm on the server\n" +
      "\tC <--> To Charge the remote controller battery\n" +
      "\tH <--> To print remote controller usage\n" +
      "\tQ <--> To disconnect to server and exit\n" +
      "\tCtrl+C <---> Will print Interrupt, NOT kill the current process\n"
      "\t0-9 <--> Digits\n")

# code for keyboard input in terminal
fd = sys.stdin.fileno()
oldterm = termios.tcgetattr(fd)
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)
oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

try:
    # 4. Not allow user to transmit keys to target when the battery level is 0
    while remote_controller_battery > 0:
        try:
            key_input = sys.stdin.read(1)

            # 9. Allow user to send single digits 0 through 9 to target at runtime instantly (i.e. once keyboard key 0 is released, send immediately)
            if key_input in dict_btn.keys():
                # 2. Decrement a battery variable (per time interval or each digit key pressed)
                remote_controller_battery -= 1
                print(dict_btn.get(key_input))
                # 3. Print battery level every time it is decremented
                print("Battery decreased to " + str(remote_controller_battery))
                client_socket.send(key_input)

            # target 5.query for most pressed button and how many times it was pressed
            elif key_input == "m":
                client_socket.send(key_input)
                remote_controller_battery -= 1
                most_pressed_btn_str = client_socket.recv(1024)  # received string tuple
                most_pressed_btn_tuple = literal_eval(most_pressed_btn_str)  # convert string tuple to tuple
                for i in range(len(most_pressed_btn_tuple[1])):
                    print("The most pressed button is " + most_pressed_btn_tuple[1][i] + ", totally got pressed " +
                          str(most_pressed_btn_tuple[0]) + " times")
                print("Battery decreased to " + str(remote_controller_battery))

            # target 6.query for least pressed button and how many times it was pressed
            elif key_input == "l":
                client_socket.send(key_input)
                remote_controller_battery -= 1
                least_pressed_btn_str = client_socket.recv(1024)  # received string tuple
                least_pressed_btn_tuple = literal_eval(least_pressed_btn_str)  # convert string tuple to tuple
                for i in range(len(least_pressed_btn_tuple[1])):
                    print("The least pressed button is " + least_pressed_btn_tuple[1][i] + ", totally got pressed " +
                          str(least_pressed_btn_tuple[0]) + " times")
                print("Battery decreased to " + str(remote_controller_battery))

            # 6. Allow the user to activate an alarm on the target (used to check key statistics per interval)
            elif key_input == "a":
                client_socket.send(key_input)
                print("Alarm got activated on server!")
                remote_controller_battery -= 1
                print("Battery decreased to " + str(remote_controller_battery))

            # 7. Allow the user to deactivate an alarm on the target
            elif key_input == "z":
                client_socket.send(key_input)
                print("Alarm got deactivated on server!")
                remote_controller_battery -= 1
                print("Battery decreased to " + str(remote_controller_battery))

            elif key_input == "c":
                print("Start charging battery...")
                remote_controller_battery = battery_charge(remote_controller_battery)
                time.sleep(2)  # for better user experience
                print("Remote controller battery value back to %s." % remote_controller_battery)
                client_socket.send(key_input)

            # 10. Allow the user to close connection to target gracefully
            elif key_input == "q":
                client_socket.send(key_input)
                print("Disconnecting...")
                # 11. Print time (EPOCH) of connection closed
                print("Disconnected to server successfully at %f." % time.time())
                client_socket.shutdown(socket.SHUT_RDWR)
                client_socket.close()
                exit(1)

            elif key_input == "h":
                remote_controller_battery -= 1
                print("### Remote Controller Usage ###\n" + "\tU <--> Up\n" + "\tD <--> Down\n" + "\tR <--> Repeat\n" +
                      "\tM <--> To query for most pressed button and how many times it was pressed\n" +
                      "\tL <--> To query for least pressed button and how many times it was pressed\n" +
                      "\tA <--> To activate an alarm on the server\n" +
                      "\tZ <--> To deactivate an alarm on the server\n" +
                      "\tC <--> To Charge the remote controller battery\n" +
                      "\tH <--> To print remote controller usage\n" +
                      "\tQ <--> To disconnect to server and exit\n" +
                      "\tCtrl+C <---> Will print Interrupt, NOT kill the current process\n"
                      "\t0-9 <--> Digits\n")
                print("Battery decreased to " + str(remote_controller_battery))

            else:
                print("Wrong button, please press again!")
        except IOError: pass

finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)