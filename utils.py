
def login(username, file_path):
    # Check for duplicates
    username = username + '\n'
    f = open(file_path, 'r+')
    for line in f:
        print(line)
        if (line == username):
            return False
    f.write(username)
    f.close()

def float_as_percentage(a):
        return int(a * 100)
