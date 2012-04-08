Powershell -command "Remove-Item stage -Recurse"

@REM BASE URL is http://svn.zhtoolkit.com/ChineseWordExtractor/trunk
"c:\Program Files\TortoiseSVN\bin\TortoiseProc.exe" /command:export /path:stage
cd stage


xcopy data    dist\data    /E /I
xcopy dict    dist\dict    /E /I
xcopy filter  dist\filter  /E /I
xcopy samples dist\samples /E /I

copy ..\Microsoft.VC90.CRT.manifest .\
copy ..\msvcm90.dll .\
copy ..\msvcp90.dll .\
copy ..\msvcr90.dll .\

copy ..\Microsoft.VC90.CRT.manifest dist\
copy ..\msvcm90.dll dist\
copy ..\msvcp90.dll dist\
copy ..\msvcr90.dll dist\
copy application-icon.ico dist\

python exe-setup.py py2exe

chdir dist
del "Chinese Word Extractor.exe"
ren main.exe "Chinese Word Extractor.exe"
