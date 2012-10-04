set PATH=C:\Program Files\Python27;c:\Program Files\TortoiseSVN\bin;%PATH%

@REM DEL /F /S /Q stage
RMDIR /S /Q stage


@REM BASE URL is http://svn.zhtoolkit.com/ChineseWordExtractor/tags/release-0_3_0

REM **Make sure to choose the proper tags/release-* directory as the source
TortoiseProc.exe /command:export /path:stage

@REM TortoiseProc.exe /command:dropexport /path:http://svn.zhtoolkit.com/ChineseWordExtractor/tags/release-0_3_0 /droptarget:stage

pause

cd stage


copy ..\Microsoft.VC90.CRT.manifest .\
copy ..\msvcm90.dll .\
copy ..\msvcp90.dll .\
copy ..\msvcr90.dll .\


python exe-setup.py py2exe


chdir dist
del "Chinese Word Extractor.exe"
ren main.exe "Chinese Word Extractor.exe"

cd ..
ren dist "Chinese Word Extractor"

REM Now zip the folder "Chinese Word Extractor", and rename the zip file
