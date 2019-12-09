#!/usr/bin/env python3

import sys
import socket
import selectors
import traceback

import libclient
import config
import my_logger



sel = selectors.DefaultSelector()


def create_request_old(action, value):
    if action == "search":
        return dict(
            type="text/json",
            encoding="utf-8",
            content=dict(action=action, value=value),
        )
    else:
        return dict(
            type="binary/custom-client-binary-type",
            encoding="binary",
            content=bytes(action + value, encoding="utf-8"),
        )


def create_request(action, value):
    return dict(
        type="text/json",
        encoding="utf-8",
        content=dict(action=action, value=value),
    )


def create_poll_request():
    return dict(
        type="text/json",
        encoding="utf-8",
        content=dict(action="poll")
    )


def create_add_request(new_recording):
    return dict(
        type="text/json",
        encoding="utf-8",
        content=dict(action="add", data=new_recording)

    )


def start_connection(host, port, request):
    addr = (host, port)
    my_logger.log("starting connection to {}".format(addr))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    message = libclient.Message(sel, sock, addr, request)
    sel.register(sock, events, data=message)

    try:
        while True:
            events = sel.select(timeout=1)
            for key, mask in events:
                message = key.data
                try:
                    message.process_events(mask)
                except Exception:
                    print(
                        "main: error: exception for",
                        f"{message.addr}:\n{traceback.format_exc()}",
                    )
                    message.close()
            # Check for a socket being monitored to continue.
            if not sel.get_map():
                break
    except KeyboardInterrupt:
        print("caught keyboard interrupt, exiting")
    finally:
        pass
        # sel.close()


def main_menu():
    print('1. poll')
    print('2. add')
    print('3. exit')
    while True:
        result = input('choice: ')
        try:
            result = int(result)
            if result == 1:
                start_connection(
                    config.HOST,
                    int(config.PORT),
                    create_poll_request()
                )
            elif result == 2:
                start_connection(
                    config.HOST,
                    int(config.PORT),
                    create_add_request('mitch')
                )
            elif result == 3:
                sys.exit(0)
            else:
                print("{} is not an option".format(result))
        except Exception as e:
            print(e)
            print('{}  is invalid choice'.format(result))
    sel.close()


if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     print("usage:", sys.argv[0], "<action> <value>")
    #     sys.exit(1)
    main_menu()
