#!usr/bin/env python

# Server/target program
import socket
import signal
import time

HOST = socket.gethostname()  # get local machine host name
PORT = 12345  # give a random port number
alarm_timing = 0

# count pressed button value
up_btn_cnt = 0
down_btn_cnt = 0
repeat_btn_cnt = 0
zero_btn_cnt = 0
one_btn_cnt = 0
two_btn_cnt = 0
three_btn_cnt = 0
four_btn_cnt = 0
five_btn_cnt = 0
six_btn_cnt = 0
seven_btn_cnt = 0
eight_btn_cnt = 0
nine_btn_cnt = 0

# button dictionary
dict_btn_count = {'u': up_btn_cnt, 'd': down_btn_cnt, 'r': repeat_btn_cnt}
# digits dictionary
dict_dgit_count = {'0': zero_btn_cnt, '1': one_btn_cnt, '2': two_btn_cnt, '3': three_btn_cnt, '4': four_btn_cnt,
                   '5': five_btn_cnt, '6': six_btn_cnt, '7': seven_btn_cnt, '8': eight_btn_cnt, '9': nine_btn_cnt}

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a socket object
server_socket.bind((HOST, PORT))  # bind host to the port
server_socket.listen(5)  # queue up to 5 requests


def handler(_signal, _frame):
    raise IOError("Couldn't get key statistics!")


def setup_alarm(alarm_time):
    # Set the signal handler and a x-second alarm
    if alarm_time == 0:
        return signal.alarm(0)
    else:
        signal.signal(signal.SIGALRM, handler)
        return signal.alarm(alarm_time)


while True:
    client_socket, addr = server_socket.accept()  # establish a connection
    print("Got a connection from %s" % str(addr))

    current_time = time.time()  # get current time
    if not current_time: break
    # 1.Print time (EPOCH) of connection established
    print("The connection established at %s" % current_time)
    client_socket.send(str(current_time))

    while client_socket:
        data = client_socket.recv(1024)  # Receive no more than 1024 bytes
        if data == "u":  # up_button = u
            # 2. Must keep track of each button pressed and how many times it was pressed
            up_btn_cnt += 1
            dict_btn_count['u'] = up_btn_cnt
            print("Up button got pressed, totally got pressed " + str(up_btn_cnt) + " times")

        elif data == "d":  # down_button = d
            down_btn_cnt += 1
            dict_btn_count['d'] = down_btn_cnt
            print("Down button got pressed, totally got pressed " + str(down_btn_cnt) + " times")

        elif data == "r":  # repeat_button = r
            repeat_btn_cnt += 1
            dict_btn_count['r'] = repeat_btn_cnt
            print("Repeat button got pressed, totally got pressed " + str(repeat_btn_cnt) + " times")

        elif data == "0":
            zero_btn_cnt += 1
            dict_dgit_count['0'] = zero_btn_cnt
            print("Number 0 received.")

        elif data == "1":
            one_btn_cnt += 1
            dict_dgit_count['1'] = one_btn_cnt
            print("Number 1 received.")

        elif data == "2":
            two_btn_cnt += 1
            dict_dgit_count['2'] = two_btn_cnt
            print("Number 2 received.")

        elif data == "3":
            three_btn_cnt += 1
            dict_dgit_count['3'] = three_btn_cnt
            print("Number 3 received.")

        elif data == "4":
            four_btn_cnt += 1
            dict_dgit_count['4'] = four_btn_cnt
            print("Number 4 received.")

        elif data == "5":
            five_btn_cnt += 1
            dict_dgit_count['5'] =  five_btn_cnt
            print("Number 5 received.")

        elif data == "6":
            six_btn_cnt += 1
            dict_dgit_count['6'] = six_btn_cnt
            print("Number 6 received.")

        elif data == "7":
            seven_btn_cnt += 1
            dict_dgit_count['7'] = seven_btn_cnt
            print("Number 7 received.")

        elif data == "8":
            eight_btn_cnt += 1
            dict_dgit_count['8'] = eight_btn_cnt
            print("Number 8 received.")

        elif data == "9":
            nine_btn_cnt += 1
            dict_dgit_count['9'] = nine_btn_cnt
            print("Number 9 received.")

        # 3. Allow controller to activate alarm on the target
        elif data == "a":
            print("Alarm got activated!")

            most_pressed_btn_num = max(dict_btn_count.values())  # most pressed button value
            most_pressed_btn_list = [k for k, v in dict_btn_count.items() if
                                     v == most_pressed_btn_num]  # list of most pressed button
            # 7. Print most pressed button and how many times it was pressed per controller initiated alarm interval
            for i in range(len(most_pressed_btn_list)):
                print("The most pressed button is " + most_pressed_btn_list[i] + ", totally got pressed " +
                      str(most_pressed_btn_num) + " times")

            least_pressed_btn_num = min(dict_btn_count.values())  # least pressed button value
            least_pressed_btn_list = [k for k, v in dict_btn_count.items() if
                                      v == least_pressed_btn_num]  # list of least pressed button
            # 8. Print least pressed button and how many times it was pressed per controller initiated alarm interval
            for i in range(len(least_pressed_btn_list)):
                print("The least pressed button is " + least_pressed_btn_list[i] + ", totally got pressed " +
                      str(least_pressed_btn_num) + " times")

            alarm_timing = 3

        # 4. Allow controller to deactivate alarm on the target
        elif data == "z":
            print("Alarm got deactivated!")
            alarm_timing = 0

        elif data == "m":
            print("The most pressed button queried.")
            setup_alarm(alarm_timing)  # setup an alarm before checking key statistic

            # for alarm testing purpose, when the alarm is on, the program will break, because system will
            # sleep 8 seconds which is greater than alarm timing 5
            # if alarm_timing != 0:
            #     time.sleep(5)

            most_pressed_btn_num = max(dict_btn_count.values())  # most pressed button value
            most_pressed_btn_list = [k for k,v in dict_btn_count.items() if v == most_pressed_btn_num]  # list of most pressed button
            client_socket.send(str((most_pressed_btn_num, most_pressed_btn_list)))  # send string tuple data to client

        elif data == 'l':
            print("The least pressed button queried.")
            setup_alarm(alarm_timing)  # setup an alarm before checking key statistic

            least_pressed_btn_num = min(dict_btn_count.values())  # least pressed button value
            least_pressed_btn_list = [k for k, v in dict_btn_count.items() if v == least_pressed_btn_num]  # list of least pressed button
            client_socket.send(str((least_pressed_btn_num, least_pressed_btn_list)))  # send string tuple data to client

        # 9. Print time (EPOCH) when battery replaced message was received from controller
        elif data == "c":
            print("Remote controller got fully charged at %f." % time.time())

        # 10. Print time (EPOCH) of connection closed
        elif data == "q":
            print("Disconnected to client successfully at %f." % time.time())
            server_socket.close()  # disconnect to client
            exit(1)

        else:
            print("Wrong button, please press again!")