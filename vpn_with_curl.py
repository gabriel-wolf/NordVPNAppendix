import subprocess
import platform
from datetime import datetime
import csv
import time
import requests

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

def main():
    servers_file = "nameservers.txt"
    servers = read_servers_from_file(servers_file)

    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    csv_filename = f'results_{current_datetime}.csv'

    websites_to_curl = ["http://www.netflix.com", "https://www.hulu.com", "https://www.max.com", "https://www.tiktok.com", "https://www.instagram.com", "https://www.bbc.com", "https://www.nytimes.com", "https://www.cnn.com", "https://www.foxnews.com"]

    with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)

        headers = ['Control Timestamp', 'Control IP', 'Control Server ID', 'Control Sponsor', 'Control Server Name', 'Control Distance (km)', 'Control Download (mbps)', 'Control Upload (mbs)', 'Control Ping (ms)', 'Control Netflix (s)', 'Control Hulu (s)', 'Control HBO MAX (s)', 'Control TikTok (s)', 'Control Instagram (s)', 'Control BBC (s)', 'Control NYT (s)', 'Control CNN (s)', 'Control FOX (s)', 'Timestamp', 'IP', 'Server ID', 'Sponsor', 'Server Name', 'Distance', 'Download (mbps)', 'Upload (mbps)', 'Ping (ms)', "Netflix (s)", 'Hulu (s)', 'HBO MAX (s)', 'TikTok (s)', 'Instagram (s)', 'BBC (s)', 'NYT (s)', 'CNN (s)', 'FOX (s)', 'VPN Server']
        csv_writer.writerow(headers)

        runcount = 0


        while True:
            runcount = runcount + 1
            print ("\nRUNCOUNT: #" + str(runcount) + "\n")

            try:
                for server_info in servers:

                    print ("\nRUNCOUNT: #" + str(runcount) + "\n")


                    server = str(server_info[0])

                    c_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    ###### DISCONNECT
                    print("\nDisconnecting...")
                    run_command('"C:\\Program Files\\NordVPN\\nordvpn" -d')
                    time.sleep(10)

                    # Run all three tests
                    c_download_speed, c_upload_speed, c_ping_result, c_server_id, c_sponsor, c_server_name, c_distance, c_ip_address = run_advanced_speed_test()
                    # c_download_speed, c_upload_speed, c_ping_result = run_speed_test()

                    c_netflix_time = curl_website(websites_to_curl[0])
                    c_hulu_time = curl_website(websites_to_curl[1])
                    c_hbomax_time = curl_website(websites_to_curl[2])
                    c_tiktok_time = curl_website(websites_to_curl[3])
                    c_instagram_time = curl_website(websites_to_curl[4])
                    c_bbc_time = curl_website(websites_to_curl[5])
                    c_nyt_time = curl_website(websites_to_curl[6])
                    c_cnn_time = curl_website(websites_to_curl[7])
                    c_fox_time = curl_website(websites_to_curl[8])

                    try:
                        print(f"Control Download Speed: {c_download_speed:.2f} Mbps")
                        print(f"Control Upload Speed: {c_upload_speed:.2f} Mbps")
                        print(f"Control Ping Test Result: {c_ping_result} ms")
                        print(f"Control Server ID: {c_server_id}")
                        print(f"Control Sponsor: {c_sponsor}")
                        print(f"Control Server Name: {c_server_name}")
                        print(f"Control Distance: {c_distance} km")
                        print(f"Control IP Address: {c_ip_address}")
                    except:
                        print("error printing control")

                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    #### CONNECT TO SERVER (server)
                    print("\nConnecting to " + server + "..." )
                    command = '"C:\\Program Files\\NordVPN\\nordvpn" -c -g "' + server + '"'
                    print(command)
                    run_command(command)
                    time.sleep(10)
                    netflix_time = curl_website(websites_to_curl[0])
                    hulu_time = curl_website(websites_to_curl[1])
                    hbomax_time = curl_website(websites_to_curl[2])
                    tiktok_time = curl_website(websites_to_curl[3])
                    instagram_time = curl_website(websites_to_curl[4])
                    bbc_time = curl_website(websites_to_curl[5])
                    nyt_time = curl_website(websites_to_curl[6])
                    cnn_time = curl_website(websites_to_curl[7])
                    fox_time = curl_website(websites_to_curl[8])

                    # Run all three tests
                    # download_speed, upload_speed, ping_result = run_speed_test()
                    download_speed, upload_speed, ping_result, server_id, sponsor, server_name, distance, ip_address = run_advanced_speed_test()

                    try:
                        print(f"Download Speed: {download_speed:.2f} Mbps")
                        print(f"Upload Speed: {upload_speed:.2f} Mbps")
                        print(f"Ping Test Result: {ping_result} ms")
                        print(f"Server ID: {server_id}")
                        print(f"Sponsor: {sponsor}")
                        print(f"Server Name: {server_name}")
                        print(f"Distance: {distance} km")
                        print(f"IP Address: {ip_address}")
                    except:
                        print("error printing vpn ")


                    try:
                        row_data = [c_timestamp, c_ip_address, c_server_id, c_sponsor, c_server_name, c_distance, c_download_speed, c_upload_speed, c_ping_result, c_netflix_time, c_hulu_time, c_hbomax_time, c_tiktok_time, c_instagram_time, c_bbc_time, c_nyt_time, c_cnn_time, c_fox_time, timestamp, ip_address, server_id, sponsor, server_name, distance, download_speed, upload_speed, ping_result, netflix_time, hulu_time, hbomax_time, tiktok_time, instagram_time, bbc_time, nyt_time, cnn_time, fox_time, server]
                        print(row_data)
                        csv_writer.writerow(row_data)
                    except UnicodeEncodeError as e:
                        print(f"Error encoding row: {e}")
                        # Handle the error as needed, you might want to log it or skip the problematic row.
                        pass
            except:
                print("something went wrong big time but we caught it")

if __name__ == "__main__":
    main()
