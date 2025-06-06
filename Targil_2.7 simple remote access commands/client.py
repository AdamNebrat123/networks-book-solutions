#   Ex. 2.7 template - client side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020


import socket


import protocol


IP = '127.0.0.1'
SAVED_PHOTO_LOCATION = 'D:\\Networks_by_Barak_Gonen\'s_book\\Targilim\\Targil 2.7\\saved pohotos\\Copied Screenshot' # The path + filename where the copy of the screenshot at the client should be saved

def handle_server_response(my_socket, cmd):
    """
    Receive the response from the server and handle it, according to the request
    For example, DIR should result in printing the contents to the screen,
    Note - special attention should be given to SEND_PHOTO as it requires and extra receive
    """
    # (8) treat all responses except SEND_PHOTO
    valid_protocol, data = protocol.get_msg(my_socket)
    if valid_protocol:
        if not 'SEND_PHOTO' in cmd:
            print(data)
        # (10) treat SEND_PHOTO
        else:
            try:
                length_of_img = int(data)
                img_bytes = my_socket.recv(length_of_img)
                with open(SAVED_PHOTO_LOCATION, 'wb') as f:
                    f.write(img_bytes)
                    print("Successfully saved")
            except Exception:
                print("The img could not be saved")





def main():
    try:
        my_socket = socket.socket()
        my_socket.connect(("127.0.0.1", 8200))
        # (2)

        # print instructions
        print('Welcome to remote computer application. Available commands are:\n')
        print('TAKE_SCREENSHOT\nSEND_PHOTO\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')

        # loop until user requested to exit
        while True:
            cmd = input("Please enter command:\n")
            if protocol.check_cmd(cmd):
                packet = protocol.create_msg(cmd)
                my_socket.send(packet)
                handle_server_response(my_socket, cmd)
                if cmd == 'EXIT':
                    break
            else:
                print("Not a valid command, or missing parameters\n")
    except Exception:
        print('The connection was interupted')
    my_socket.close()

if __name__ == '__main__':
    main()