from pywinauto.application import Application
import subprocess
import time
import os

app = Application().start("notepad.exe")

app.UntitledNotepad.Edit.type_keys("print {(}'ui automation sample'{)}", with_spaces = True)

app.UntitledNotepad.menu_select("File(&F)->Save(&S)")
app.Save_As.Edit1.set_edit_text(r"C:\Users\sukim\codes\google-python-security\automation\samplecode.py")
app.Save_As.ComboBox2.select("All Files ")
app.Save_As.ComboBox3.select("UTF-8")

time.sleep(1.0)
app.Save_As.Button1.click()
app.UntitledNotepad.menu_select("File(&F)->Exit(X)")

cmd = subprocess.run(["python", "samplecode.py"], capture_output=True)
stdout = cmd.stdout.decode()
print(stdout)

os.remove("samplecode.py")