import threading
import time
import sys


def calculate(stop):
    global emotion
    # initially we are happy
    emotion = "happy"
    while True:
        if stop():
            print(f'Now I am {emotion} and will shut up.')
            break
        time.sleep(1)
        print(f'I am {emotion}! Say "badboy" to make me stop being {emotion}..')


def main():
    global emotion
    # output_thread runs in parallel to user input
    # to stop it we provide a (lambda-)function as second argument 
    stop_thread = False
    output_thread = threading.Thread(target=calculate, args=(lambda: stop_thread,))
    output_thread.daemon = True
    output_thread.start()
    while True:
        sent = input('> ').encode('utf-8')  # Input
        if sent == 'badboy':
            # emotion is a global variable and, thus, accessible by main thread and output_thread
            emotion = "sad"
            stop_thread = True
            sys.exit()
        else:
            print(f'I am still {emotion}..')
            print(sent)


main()
