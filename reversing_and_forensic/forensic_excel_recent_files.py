import winreg

try:
    hKey = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        "Software\\Microsoft\\Office\\16.0\\Excel\\File MRU"
    )

    for i in range(0, winreg.QueryInfoKey(hKey)[1]):
        name, value, type = winreg.EnumValue(hKey, i)

        if name.startswith("Item"):
            print(name+":"+value)

except FileNotFoundError:
    print("Excel not found")