import paramiko
import time

PLC_IP = "192.168.7.2"
USERNAME = "root"
PASSWORD = "zeon"
vivod = []
firsttime = True

COMMAND = """
ip -o link show | awk '/ether/ {print $2, $17}';
ip -o -4 addr show | awk '/eth/ {print $2, $4}';
ip -o -6 addr show | awk '/eth/ {print $2, $4}'
"""


def get_plc_info(ip, username, password):
    global vivod
    global firsttime
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(ip, username=username, password=password)


        stdin, stdout, stderr = client.exec_command(COMMAND)

        output = stdout.read().decode('utf-8')
        errors = stderr.read().decode('utf-8')

        if errors:
            print(f"Errors: {errors}")
        else:
            output = output.split("\n")
            if firsttime:
                vivod.append(output[0])
                vivod.append(output[-3])
                vivod.append(output[-2])
                firsttime = False
                print(vivod)
            else:
                if output[0] == vivod[0] and output[-3] == vivod[-2] and output[-2] == vivod[-1]:
                    pass
                else:
                    vivod[0] = output[0]
                    vivod[-2] = output[-3]
                    vivod[-1] = output[-2]
                    print(output[0], output[-3], output[-2])
                    print("произошли изменения")
    finally:
        client.close()


if __name__ == "__main__":
    while True:
        get_plc_info(PLC_IP, USERNAME, PASSWORD)

        time.sleep(10)