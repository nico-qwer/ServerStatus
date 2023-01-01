import time

def write_to_logfile(line):
    file = open("botlogs.log", "a")
    file.write(line + "\n")
    file.close()

def info(message):
    timenow = time.ctime()
    write_to_logfile(f"{timenow} | {message}")

def warn(message):
    timenow = time.ctime()
    write_to_logfile(f"{timenow} | ! | {message}")

def error(message):
    timenow = time.ctime()
    write_to_logfile(f"{timenow} | ERROR | {message}")

def crit_error(message):
    timenow = time.ctime()
    write_to_logfile(f"<<< {timenow} | !!! CRITICAL ERROR !!! | {message} >>>")