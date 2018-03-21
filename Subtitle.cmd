@echo off
cls
IF EXIST C:\Python34\ SET PATH=%PATH%;C:\Python34\
IF EXIST C:\Python27\ SET PATH=%PATH%;C:\Python27\
:my_loop
IF %1=="" GOTO completed
  python C:\subtitle-downloader.py %1
  SHIFT
  GOTO my_loop
:completed
