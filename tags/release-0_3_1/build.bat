Powershell -command "Remove-Item stage -Recurse"

@REM BASE URL is http://svn.zhtoolkit.com/ChineseWordExtractor/trunk
"c:\Program Files\TortoiseSVN\bin\TortoiseProc.exe" /command:export /path:stage
cd stage


copy ..\Microsoft.VC90.CRT.manifest .\
copy ..\msvcm90.dll .\
copy ..\msvcp90.dll .\
copy ..\msvcr90.dll .\


python exe-setup.py py2exe

@REM copy ..\Microsoft.VC90.CRT.manifest dist
@REM copy ..\msvcm90.dll dist
@REM copy ..\msvcp90.dll dist
@REM copy ..\msvcr90.dll dist
@REM copy application-icon.ico dist

@REM Thanks for quietly ignoring these in a script, but work fine from the console
@REM xcopy data    dist\data    /E /I
@REM xcopy dict    dist\dict    /E /I
@REM xcopy filter  dist\filter  /E /I
@REM xcopy samples dist\samples /E /I

Powershell -command "Copy-Item -Recurse data dist\data"
Powershell -command "Copy-Item -Recurse dict dist\dict"
Powershell -command "Copy-Item -Recurse filter dist\filter"
Powershell -command "Copy-Item -Recurse samples dist\samples"

chdir dist
del "Chinese Word Extractor.exe"
ren main.exe "Chinese Word Extractor.exe"
