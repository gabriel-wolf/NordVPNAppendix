import subprocess
import platform
from datetime import datetime
import csv
import time
import requests
from requests import get
import re
import geocoder



def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output, error

def read_servers_from_file(file_path):
    with open(file_path, 'r') as file:
        servers = [line.strip().split(', ') for line in file.readlines()]
    return servers

def read_cities_from_file(file_path):
    with open(file_path, 'r') as file:
        cities = [line.strip() for line in file.readlines()]
    return cities

def curl_website(url):
    start_time = time.time()
    try:
        response = requests.get(url, timeout=180)  # Setting a timeout of 3 minutes (180 seconds)
        elapsed_time = time.time() - start_time

        if response.status_code == 200:
            print(f"Successfully curled {url} in {elapsed_time:.2f} seconds")
            return elapsed_time
        else:
            print(f"Failed to curl {url}. Status code: {response.status_code}")
            return None
    except requests.Timeout:
        print(f"Failed to curl {url}. Took too long (more than 3 minutes)")
        return None
    except Exception as e:
        print(f"Error while curling {url}: {str(e)}")
        return None

    
def run_advanced_speed_test():
    print("Speedtest has begun.")
    command = ['speedtest-cli', '--secure', '--csv', '--csv-delimiter', '~']
    result = subprocess.run(command, stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8').strip()


    # Split the CSV data
    data = output.split('~')

    print(data)

    if len(data) >= 8:
        # Extract the required information in the correct order
        server_id = int(data[0])
        sponsor = data[1]
        server_name = data[2]
        timestamp = data[3]
        distance = float(data[4])
        ping = float(data[5])
        download = float(data[6])  / 1_000_000
        upload = float(data[7])  / 1_000_000
        ip_address = data[9]

        return download, upload, ping, server_id, sponsor, server_name, distance, ip_address

    return None, None, None, None, None, None, None, None


def run_speed_test():
    print("Speedtest has begun.")
    command = ['speedtest-cli', '--secure', '--simple']
    result = subprocess.run(command, stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8').strip()

    if not output:
        print("Error: Speedtest result is empty.")
        return None, None, None

    # Identify lines containing speed values
    speed_lines = [line for line in output.split('\n') if 'Download:' in line or 'Upload:' in line or 'Ping:' in line]

    # Extract numerical values from speed lines
    speed_values = [float(value.split()[0]) for line in speed_lines for value in line.split(':') if value.split()[0].replace('.', '', 1).isdigit()]

    download_speed, upload_speed, ping_result = None, None, None

    for line in speed_lines:
        if 'Download:' in line:
            download_speed = float(line.split()[1])
        elif 'Upload:' in line:
            upload_speed = float(line.split()[1])
        elif 'Ping:' in line:
            ping_result = float(line.split()[1])

    return download_speed, upload_speed, ping_result


def run_ping_test(destination):
    # Adjust the ping test command based on your platform (Windows or Unix-like systems)
    if platform.system().lower() == 'windows':
        command = ['ping', '-n', '5', destination]
    else:
        command = ['ping', '-c', '5', destination]

    result = subprocess.run(command, stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')


def calculate_average(lst):
    if not lst:
        return None  # Return None for an empty list
    return sum(lst) / len(lst)


def main():
    servers_file = "nameservers.txt"
    servers = read_servers_from_file(servers_file)

    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    csv_filename = f'ip_{current_datetime}.csv'


    with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)

        headers = ['Timestamp', 'User IP', 'Server IP', 'Ping Speeds', 'Average Ping', 'VPN Address', 'VPN Server']
        csv_writer.writerow(headers)

        runcount = 0


        while True:
            runcount = runcount + 1

            # try:
            for server_info in servers:

                
                print ("\nRUNCOUNT: #" + str(runcount) + "\n")
                server = str(server_info[0])
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                try:
                    

                        #### CONNECT TO SERVER (server)
                    print("\nConnecting to " + server + "..." )
                    command = '"C:\\Program Files\\NordVPN\\nordvpn" -c -g "' + server + '"'
                    print(command)
                    run_command(command)
                    time.sleep(10)


                    try:
                        g = geocoder.ip('me')
                        print("\nVPN ADDRESS: " + str(g.address))
                    except:
                        print("\nCOULDN'T SET UP GEOCODER AND GET ADDRESS")
                        g = None


                    # get ip
                    try:
                        server_ip = get('https://api.ipify.org').content.decode('utf8')
                        print("\nSERVER IP IS: " + str(server_ip))
                    except:
                        print("\nFAILED TO GET SERVER IP")
                        server_ip = None

                    ###### DISCONNECT
                    print("\nDisconnecting...")
                    run_command('"C:\\Program Files\\NordVPN\\nordvpn" -d')
                    time.sleep(10)

                    try:
                        user_ip = get('https://api.ipify.org').content.decode('utf8')
                        print("\nUSER IP IS: " + str(user_ip))
                    except:
                        print("\nFAILED TO GET USER IP")
                        user_ip = None

                    # ping ip 

                    try:
                        ping_results = run_ping_test(server_ip)
                    except:
                        print("\nFAILED TO GET PING RESULTS")
                        ping_results = None

                    print(ping_results)

                    try:
                        if platform.system().lower() == 'windows':
                            time_values = re.findall(r'time=(\d+)ms', ping_results)
                        else:
                            time_values = re.findall(r'time=(\d+\.\d+)', ping_results)

                        # Convert the time values to integers or floats
                        if platform.system().lower() == 'windows':
                            time_values = [int(time) for time in time_values]  # Convert to integers
                        else:
                            time_values = [float(time) for time in time_values]  # Convert to floats
                    except:
                        print("\nFAILED TO GET TIME VALUES")
                        time_values = None

                    print("\nPING VALUES: " + str(time_values))

                    try:
                        avg_ping_speed = calculate_average(time_values)
                    except:
                        print("\nFAILED TO GET AVERAGE SPEED")
                        avg_ping_speed = None

                    print("\nAVERAGE PING VALUE: " + str(avg_ping_speed))

                    try:
                        row_data = [timestamp, user_ip, server_ip, time_values, avg_ping_speed, g.address, server]
                        # row_data = [c_timestamp, c_ip_address, c_server_id, c_sponsor, c_server_name, c_distance, c_download_speed, c_upload_speed, c_ping_result, c_netflix_time, c_hulu_time, c_hbomax_time, c_tiktok_time, c_instagram_time, c_bbc_time, c_nyt_time, c_cnn_time, c_fox_time, timestamp, ip_address, server_id, sponsor, server_name, distance, download_speed, upload_speed, ping_result, netflix_time, hulu_time, hbomax_time, tiktok_time, instagram_time, bbc_time, nyt_time, cnn_time, fox_time, server]
                        print(row_data)
                        csv_writer.writerow(row_data)
                    except UnicodeEncodeError as e:
                        print(f"Error encoding row: {e}")
                        # Handle the error as needed, you might want to log it or skip the problematic row.
                        pass
                except:
                    print("\nFAILED SOMEWHERE")
                    row_data = [timestamp, None, None, None, None, None, server]
                    print(row_data)
                    csv_writer.writerow(row_data)
            # except:
                # print("something went wrong big time but we caught it")

if __name__ == "__main__":
    main()
