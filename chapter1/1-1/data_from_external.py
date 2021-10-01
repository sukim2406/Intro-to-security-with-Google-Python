data_from_external = ["union all blah blah --", 1, 11]

def check_safe_number(data):
    if isinstance(data, int):
        if 0 < data <= 10:
            print("safe data")
        else:
            print("out of bound")
    else:
        print("not a number")

for data in data_from_external:
    check_safe_number(data)
