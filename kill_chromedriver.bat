@echo off
@REM For some reason, chromedriver instances don't quit with the quit function on Windows so I made this batch file to kill ALL chrome processes when the user wishes to exit the program.  
@REM NOTE: this is not a good fix because executing this batch file kills ALL chrome processes: not just those created by running this program

taskkill /im chrome.exe /f
