#!/usr/bin/env python3
#coding=utf8

from datetime import datetime
from os import getpid, path, remove, mkdir, getcwd
import psutil
import gzip
import shutil

def startup_log() :
    cwd = getcwd()
    logpath = path.join(cwd, "logs")
    latestpath = path.join(logpath, "latest.txt")
    if not path.isdir(logpath) :
        mkdir(logpath)
    if path.isfile(latestpath) :
        now = datetime.now()
        timestr = now.strftime("%d-%m-%Y")
        archive_name = path.join(logpath, f"log{timestr}.txt.gz")
        i = 1
        with open(latestpath, 'rb') as f_in:
            while path.isfile(path.join(logpath, archive_name)) :
                archive_name = f"log{timestr}-{i}.txt.gz"
                i = i + 1
            with gzip.open(path.join(logpath, archive_name), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        remove(latestpath)
        return
    else :
        return

def writelog(title: str ="LOG", message: str ="void", error: bool =False, perfreport=False) :
    current = psutil.Process(getpid())
    mem = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent(interval=None)
    now = datetime.now()
    timestr = now.strftime("%d/%m/%Y %H:%M:%S")
    cwd = getcwd()
    logpath = path.join(cwd, "logs")
    latestpath = path.join(logpath, "latest.txt")

    if path.isfile(latestpath) :
        with open(latestpath, 'a', encoding="utf-8") as f:
            if error:
                f.write(f"/!\\ ERROR - [{timestr}] - {title} - {message}\n")
            elif perfreport :
                f.write(f"[{timestr}] - PERFORMANCE (normal) - mem global : {mem}% - mem program : {round(((current.memory_info().rss) / 1000000), 2)} MB - cpu global : {cpu}%\n")
            else :
                f.write(f"[{timestr}] - {title} - {message}\n")
    else :
        with open(latestpath, 'w', encoding="utf-8") as f:
            if error:
                f.write(f"/!\\ ERROR - [{timestr}] - {title} - {message}\n")
            elif perfreport :
                f.write(f"[{timestr}] - PERFORMANCE (normal) - mem global : {mem}% - mem program : {round(((current.memory_info().rss) / 1000000), 2)} MB - cpu global : {cpu}%\n")
            else :
                f.write(f"[{timestr}] - {title} - {message}\n")