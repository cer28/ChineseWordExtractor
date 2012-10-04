set PATH=C:\Program Files\Python27;%PATH%

@REM Powershell -command "Remove-Item stage -Recurse"
DEL /F /S /Q stage

@REM BASE URL is http://svn.zhtoolkit.com/ChineseWordExtractor/trunk
"c:\Program Files\TortoiseSVN\bin\TortoiseProc.exe" /command:export /path:stage
cd stage


copy ..\Microsoft.VC90.CRT.manifest .\
copy ..\msvcm90.dll .\
copy ..\msvcp90.dll .\
copy ..\msvcr90.dll .\


python exe-setup.py py2exe


chdir dist
del "Chinese Word Extractor.exe"
ren main.exe "Chinese Word Extractor.exe"

REM Now rename the dist folder to "Chinese Word Extractor", zip it, and rename the zip file
