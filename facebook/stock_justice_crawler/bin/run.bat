@echo off

set STARTTIME=%DATE%%TIME%

echo FB crawler
echo Start : %STARTTIME%

rem ************** MAIN CODE SECTION

python -u ../crawler/run.py

rem ************** MAIN CODE SECTION

set ENDTIME=%DATE%%TIME%
echo Finish : %ENDTIME%

rem pause
EXIT;
