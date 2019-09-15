set CurrentDir=%cd%

set ScriptDir=%~dp0
cd /d %ScriptDir%

if not defined IsVsDevCmdLoaded (
  set IsVsDevCmdLoaded="True"
  call "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\Common7\Tools\VsDevCmd.bat"
)

cl out.cpp

cd /d %CurrentDir%

pause