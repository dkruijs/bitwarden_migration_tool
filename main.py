import subprocess



def bw_login(): 
    # login 
    process = subprocess.Popen('bw login', stdout=subprocess.PIPE, universal_newlines=True)
    output = process.stdout.readline()
    print(output.strip())
    if 'You are already logged in' in output:
        return
    input_ = input("Input: ")
    process.communicate(input=input)

    output = process.stdout.readline()
    print(output.strip())

def bw_create_item():
    

if __name__ == '__main__':
    # if 'BW_SESSION' not in os.environ:
    #     bw_login()


