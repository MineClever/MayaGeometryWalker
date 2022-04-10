:: coding:GBK
::Writed by MineClver
::coding in GB2312
CHCP 936
cls

:: --------------------
:: 主执行标签
:: --------------------
@echo off
cd /d "%~dp0"

:: 设置环境
call :setLocalEnv
:: $$$$启用指令扩展$$$$
SETLOCAL ENABLEEXTENSIONS
setlocal EnableDelayedExpansion

:RUN
call :delAllpycFile


:END
PAUSE
:: 结束
:: $$$$结束指令扩展$$$$
setlocal DisableDelayedExpansion
endlocal

exit
goto :EOF

::::::::::::::::::::::::::::::::::::::::::::::::::::
:: Function Here
::::::::::::::::::::::::::::::::::::::::::::::::::::

:delAllpycFile
del /a /f /q /s "%~dp0*.pyc" 2>nul

:setLocalEnv
:: 设置本地变量,避免无法读取到系统路径
set path=%SystemRoot%;%path%
set path=%SystemRoot%\system32;%path%
set sysRegEnvPath=HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment
set userRegEnvPath=HKEY_CURRENT_USER\Environment
goto :EOF

:EOF
