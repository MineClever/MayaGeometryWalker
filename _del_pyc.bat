:: coding:GBK
::Writed by MineClver
::coding in GB2312
CHCP 936
cls

:: --------------------
:: ��ִ�б�ǩ
:: --------------------
@echo off
cd /d "%~dp0"

:: ���û���
call :setLocalEnv
:: $$$$����ָ����չ$$$$
SETLOCAL ENABLEEXTENSIONS
setlocal EnableDelayedExpansion

:RUN
call :delAllpycFile


:END
PAUSE
:: ����
:: $$$$����ָ����չ$$$$
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
:: ���ñ��ر���,�����޷���ȡ��ϵͳ·��
set path=%SystemRoot%;%path%
set path=%SystemRoot%\system32;%path%
set sysRegEnvPath=HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment
set userRegEnvPath=HKEY_CURRENT_USER\Environment
goto :EOF

:EOF
