import os, time

file = "test.txt"

created = os.path.getctime(file)
created_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(created))
print("Time created: " + created_time)

modified = os.path.getmtime(file)
modified_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modified))
print("Time modified: " + modified_time)

accessed = os.path.getatime(file)
accessed_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(accessed))
print("Time accessed: " + accessed_time)