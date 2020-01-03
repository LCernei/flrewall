# FLREWALL

## Requirements
```
python >= 3.7
```
### Windows:  
Go to https://www.isc.org/download/.
Download BIND 9, Current-Stable version (BIND9.14.9.x64.zip).  
Extract to `C:\Program Files\BIND9.14.9.x64`.  
Add `C:\Program Files\BIND9.14.9.x64` to system path:  
(`Control Panel\System and Security\System`; click `Advanced system settings`; click `Environment variables`; find `Path` somewhere in the bottom text box and click `Edit`; click `New`; write `C:\Program Files\BIND9.14.9.x64`; `OK`; `OK`; `OK`)

### Linux:
`sudo apt install dnsutils`

## Run

### Windows:  
Open administrator cmd
```
git clone ...
cd flrewall
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
flask run --host=0.0.0.0
```
### Linux:
Open terminal
```
git clone ...
cd flrewall
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```
Edit the `.flaskenv` file: replace `mypassword` with your sudo password.

```
flask run --host=0.0.0.0
```
