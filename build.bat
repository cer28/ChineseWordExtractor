python exe-setup.py py2exe
xcopy data    dist\data    /E /I
xcopy dict    dist\dict    /E /I
xcopy filter  dist\filter  /E /I
xcopy samples dist\samples /E /I

copy Microsoft.VC90.CRT.manifest dist\
copy msvcm90.dll dist\
copy msvcp90.dll dist\
copy msvcr90.dll dist\
copy application-icon.ico dist\

chdir dist
ren main.exe "Chinese Word Extractor.exe"
