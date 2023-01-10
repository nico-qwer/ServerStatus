import time

def write_to_logfile(line):
    file = open("botlogs.log", "a")
    file.write(line + "\n")
    file.close()

def info(message, before = ""):
    timenow = time.ctime()
    write_to_logfile(f"{before}{timenow} | {message}")

def warn(message, before = ""):
    timenow = time.ctime()
    write_to_logfile(f"{before}{timenow} | ! | {message}")

def error(message, before = ""):
    timenow = time.ctime()
    write_to_logfile(f"{before}{timenow} | ERROR | {message}")

def crit_error(message, before = ""):
    timenow = time.ctime()
    write_to_logfile(f"{before}<<< {timenow} | !!! CRITICAL ERROR !!! | {message} >>>")