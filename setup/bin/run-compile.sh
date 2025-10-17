@echo off
setlocal

UPDATE_VER=9.1
FULL_VER=4.1
PRJ_PATH=C:\Users\sstinchi\Documents\repos\Framework

echo Quale archivio vuoi creare? (UPDATE/FULL)
set /p risposta=

IF /I "%risposta%"=="UDATE" (
    zip -r Framework_update_sogei_V%{UPDATE_VER}.zip %{PRJ_PATH} -x  %{PRJ_PATH}/ant-contrib %{PRJ_PATH}/apache-ant  %{PRJ_PATH}/apache-ant %{PRJ_PATH}/dist %{PRJ_PATH}/download %{PRJ_PATH}/jdk1.8.0_152 %{PRJ_PATH}/Manual %{PRJ_PATH}/
) 
ELSE IF /I "%risposta%"=="FULL"(
    zip -r Framework_FULL_SOGEI_V%{FULL_VER}.zip %{PRJ_PATH}   
}
ELSE(    
    echo Operazione annullata.
)

endlocal
pause








