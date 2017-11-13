import subprocess

def init(passwd, python="python3"):
   proc = subprocess.Popen('sudo -S {} -m bbb_hal'.format(python),
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE,
                           shell=True)
   proc.stdin.write(passwd.encode() + '\n'.encode())
