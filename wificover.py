import os
import locale

local = locale.getdefaultlocale()
splitter = "Key Content"
if local[0] == "es_ES":
    splitter = "Contenido de la clave"
else:
    splitter = "Key Content"

result = str(os.popen("netsh wlan show profiles").read())

profiles_selected = []

profiles = result.split(":")
for p in profiles: # Extract the profile names..
    if "\n" in p:
        profile = p.split("\n")
        profile = profile[0].strip(" ")
        if profile != "":
            profiles_selected.append(profile)

passwords = []
for prf in profiles_selected:
    password = str(os.popen("netsh wlan show profile "+ prf + " key=clear").read())
    #print(password)
    if("Contenido de la clave  :" in password):
        p = str(password).split(splitter)
        password = p[1].split("\n")
        passwords.append(password[0].strip(" "))
    else:
        passwords.append("")

try:
    fd = os.open( "wifi_passwords.txt", os.O_RDWR|os.O_CREAT )
    for i in range(0,len(profiles_selected)):
        line = "Wifi SSID: " + profiles_selected[i] + " | Password: " +  passwords[i] + "\n" 
        # string needs to be converted byte object
        b = str.encode(line)
        os.write(fd, b)
    os.close(fd)
    print("Passwords stored successfully...")
except Exception:
    print("Error: couldn't store the passwords...")
    print(str(Exception))