#   Ex. 2.7 template - protocol


LENGTH_FIELD_SIZE = 4
PORT = 8820


def check_cmd(data):
    """
    Check if the command is defined in the protocol, including all parameters
    For example, DELETE c:\work\file.txt is good, but DELETE alone is not
    """
    splited_data = data.split()
    command = splited_data[0]
    splited_data = splited_data[1:]
    if command == 'DIR' and len(splited_data) == 1:
        return True
    elif command == 'DELETE' and len(splited_data) == 1:
        return True
    elif command == 'COPY' and len(splited_data) == 2:
        return True
    elif command == 'EXECUTE' and len(splited_data) == 1:
        return True
    elif command == 'TAKE_SCREENSHOT' and not splited_data:
        return True
    elif command == 'SEND_PHOTO' and not splited_data:
        return True
    elif command == 'EXIT' and not splited_data:
        return True
    # (3)
    return False


def create_msg(data):
    """
    Create a valid protocol message, with length field
    """
    data = str(data)
    zfill_length = str(len(data)).zfill(4)
    data = zfill_length + data
    # (4)
    return data.encode()


def get_msg(my_socket):
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"
    """
    length = my_socket.recv(4).decode()
    if not length.isdigit():
        my_socket.recv(1024)
        return False, "Error"
    data = my_socket.recv(int(length)).decode()
    # (5)
    return True, data


