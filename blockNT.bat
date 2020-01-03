@ECHO OFF
dig %1 +short > temp.txt
IF EXIST temp.txt (
    FOR /F %%A IN ('TYPE temp.txt') DO (
        NETSH ADVFIREWALL FIREWALL ADD RULE NAME="FLASKD" INTERFACE=ANY DIR=OUT ACTION=BLOCK REMOTEIP=%%A
    )
    DEL temp.txt /f /q
)