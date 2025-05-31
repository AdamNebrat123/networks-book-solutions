import socket
import protocol
import os
import glob
import shutil
import subprocess

import pyautogui


IP = '127.0.0.1'
# set YOUR path
PHOTO_PATH = 'D:\\Networks_by_Barak_Gonen\'s_book\\Targilim\\Targil 2.7\\screenshots and imgs\\ScreenShot1'  # The path + filename where the screenshot at the server should be saved


def check_client_request(cmd):
    """
    Break cmd to command and parameters
    Check if the command and params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        command: The requested cmd (ex. "DIR")
        params: List of the cmd params (ex. ["c:\\cyber"])
    """
    # Use protocol.check_cmd first
    if protocol.check_cmd(cmd):
        # Then make sure the params are valid
        params_list = cmd.split()
        command = params_list[0]
        params_list = params_list[1:]
        for param in params_list:
            if not os.path.exists(param):
                return False, params_list
    return True, command, params_list
    # (6)


def handle_client_request(command, params):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory
    Note: in case of SEND_PHOTO, only the length of the file will be sent

    Returns:
        response: the requested data

    """
    response = ''
    length_of_screenshot = 0
    if command == 'DIR':
        files_list = glob.glob(r'{0}'.format(params[0]))
        response = ''
        for item in files_list:
            response += item + '\n'
    elif command == 'DELETE':
        try:
            os.remove(r'{0}'.format(params[0]))
            response = 'The file was removed successfully'
        except Exception:
            response = 'could not delete it...'

    elif command == 'COPY':
        # copy from path: params[0] to path: params[1]
        try:
            shutil.copy(r'{0}'.format(params[0]), r'{0}'.format(params[1]))
            response = 'The file was copied successfully'
        except Exception:
            response = 'could not copy it...'

    elif command == 'EXECUTE':
        try:
            subprocess.call(r'{0}'.format(params[0]))
            response = 'runned successfully'
        except Exception:
            response = 'could not run it...'


    elif command == 'TAKE_SCREENSHOT':
        try:
            pass
            image = pyautogui.screenshot()
            image.save(PHOTO_PATH,format='PNG')
            with open(PHOTO_PATH, 'rb') as f:
                img_bytes = f.read()
                length_of_screenshot = len(img_bytes)
            response = str(length_of_screenshot)
        except Exception:
            response = 'screenshot was not saved'

    elif command == 'SEND_PHOTO':
        if length_of_screenshot != 0:
            response = length_of_screenshot
        else:
            response = 'the screenshot was not taken yet'

    elif command == 'EXIT':
        response = 'Exiting now'
    # (7)

    return response


def main():
    try:
        # open socket with client
        server_socket = socket.socket()
        server_socket.bind(("0.0.0.0", 8200))
        server_socket.listen()
        print("Server is up and running")
        (client_socket, client_address) = server_socket.accept()
        print("Client connected")
        # (1)

        # handle requests until user asks to exit
        while True:
            # Check if protocol is OK, e.g. length field OK
            valid_protocol, cmd = protocol.get_msg(client_socket)
            if valid_protocol:
                # Check if params are good, e.g. correct number of params, file name exists
                valid_cmd, command, params = check_client_request(cmd)
                if valid_cmd:

                    # (6)
                    # prepare a response using "handle_client_request"
                    response = handle_client_request(command, params)  # get the  response
                    # add length field using "create_msg"
                    response = protocol.create_msg(response)  # get the actual response with שדה אורך

                    # send to client
                    client_socket.send(response)

                    if command == 'SEND_FILE':
                        # Send the data itself to the client
                        try:
                            with open('image.png', 'rb') as f:
                                img_bytes = f.read()
                                client_socket.send(img_bytes)
                        except Exception:
                            pass
                        # (9)

                    elif command == 'EXIT':
                        break
                else:
                    # prepare proper error to client
                    response = 'Bad command or parameters'
                    # send to client
                    response = protocol.create_msg(response)
                    client_socket.send(response)

            else:
                # prepare proper error to client
                response = 'Packet not according to protocol'
                # send to client
                response = protocol.create_msg(response)
                client_socket.send(response)
                # Attempt to clean garbage from socket
                client_socket.recv(1024)
    except Exception:
        print('The connection was interupted')

    print("Closing connection")
    # close sockets
    client_socket.close()
    server_socket.close()


if __name__ == '__main__':
    main()
