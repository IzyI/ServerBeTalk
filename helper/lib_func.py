import os, sys
import time
import subprocess
import threading
import logging

ROOT_PATH = os.path.abspath(os.path.dirname(sys.argv[0]))


def timer_print(count, second=1, func=False):
    for i in range(1, count):
        print(i)
        if func:
            func()
        time.sleep(second)


def castom_create_trint():
    def trint(*args):
        f = open('logs/logs_' + str(threading.current_thread().name) + '-' + str(os.getpid()) + '.txt', 'a')
        for x in args:
            f.write(str(x) + '\n')
            print(x + "_" + str(threading.current_thread().name) + '-' + str(os.getpid()))
        f.close()

    return trint


def search_pid(tunell):
    cmd = "ps aux|grep '" + str(tunell) + "'|grep -v grep |awk '{print $2}'"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output, _ = p.communicate()
    if p.returncode == 1:  # no matches found tyrs = []
        return None
    elif p.returncode == 0:  # matches found tyrs = output.split('\n')
        return output.decode('utf-8').split('\n')
    else:  # error, do something with it
        return None


def kill_process(pppd):
    try:
        os.system(" kill -9 " + str(pppd))
    except:
        ...


def removeFiles(path):
    files = os.listdir(path)
    for file in files:
        try:
            os.remove(path + file)
        except:
            continue


def split_array(array, n):
    k, m = divmod(len(array), n)
    return (array[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))


def print_args(function):
    def wrapper(*args, **kwargs):
        print('Аргументы функции: ', args, kwargs)
        if function(*args, **kwargs):
            print('Yees')
            return True
        else:
            print("NOOO")
            return False

    return wrapper


def repeater_false_func(lim=3, rest=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(lim):
                result_func = func(*args, **kwargs)
                if result_func == False:
                    time.sleep(rest)
                    continue
                else:
                    return result_func
            return False

        return wrapper

    return decorator


def setup_logger(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)

if __name__ == "__main__":
    print(ROOT_PATH)
