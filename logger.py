#!/usr/bin/env python3
#coding=utf8

from datetime import datetime
from os import getpid, path, remove
import psutil
import gzip
import shutil

def startup_log() :
    if path.isfile('log.txt') :
        now = datetime.now()
        timestr = now.strftime("%d-%m-%Y")
        archive_name = f"log{timestr}.txt.gz"
        i = 1
        with open("log.txt", 'rb') as f_in:
            while path.isfile(archive_name) :
                archive_name = f"log{timestr}-{i}.txt.gz"
                i = i + 1
            with gzip.open(archive_name, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        remove("log.txt")
        return
    else :
        return

def writelog(title: str ="LOG", message: str ="void", error: bool =False, perfreport=False) :
    current = psutil.Process(getpid())
    mem = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent(interval=None)
    m = round(((current.memory_info().rss) / 1000000), 2)
    now = datetime.now()
    timestr = now.strftime("%d/%m/%Y %H:%M:%S")
    if path.isfile('log.txt') :
        with open('log.txt', 'a', encoding="utf-8") as f:
            if error:
                f.write(f"/!\\ ERROR - [{timestr}] - {title} - {message}\n")
            elif perfreport :
                f.write(f"[{timestr}] - PERFORMANCE (normal) - mem global : {mem}% - mem program : {m} MB - cpu global : {cpu}%\n")
            else :
                f.write(f"[{timestr}] - {title} - {message}\n")
    else :
        with open('log.txt', 'w', encoding="utf-8") as f:
            if error:
                f.write(f"/!\\ ERROR - [{timestr}] - {title} - {message}\n")
            elif perfreport :
                f.write(f"[{timestr}] - PERFORMANCE (normal) - mem global : {mem}% - mem program : {m} MB - cpu global : {cpu}%\n")
            else :
                f.write(f"[{timestr}] - {title} - {message}\n")