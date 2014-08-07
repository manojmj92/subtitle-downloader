@echo off
cls
set PATH=%PATH%;C:\Python27\
:my_loop
IF %1=="" GOTO completed
  python C:\subtitle-downloader-folder.py %1
  SHIFT
  GOTO my_loop
:completed
