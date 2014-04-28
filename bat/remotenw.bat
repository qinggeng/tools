@echo off
@echo %1
for /f "delims=" %%a in ('chdir') do @set currPath=%%a 
"D:\Program Files\OpenSSH\bin\ssh.exe" hunter@127.0.0.1 -p 2224 "echo '%currPath%'|sed 's_^.*:_/media/workspace_g'|sed 's/\\\\/\//g'|while read DIR; do pushd $DIR; pwd; notangle -Raction %1|tee action.sh; chmod 0755 action.sh; ./action.sh; rm action.sh; done"
action.bat
@del action.bat
