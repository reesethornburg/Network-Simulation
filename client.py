import argparse
import iperf3
import json

def run_client(ip, port, server_ip, test):
    client = iperf3.Client()
    client.server_hostname = server_ip
    client.port = port
    client.bind_address = ip
    client.duration = 60
    client.json_output = True

    if test == 'tcp':
        client.protocol = 'tcp'
    elif test == 'udp':
        client.protocol = 'udp'
#        client.bandwidth = 1000000  # 1 Mbps for UDPS
        
    print(f"Starting {test.upper()} test to server {server_ip}:{port}")

    result = client.run()

    if result.error:
        data = result.json['error']
        output_filename = f"output-{test}.json"
        with open(output_filename, 'w') as f:
            json.dump(data, f)
    else:

        data = result.json
        # ----- THIS PART MIGHT NEED WORK, I'VE BARELY EVER USED JSON -----
        output_filename = f"output-{test}.json"
        with open(output_filename, 'w') as f:
            json.dump(data, f)
        # -----------------------------------------------------------

        print(f"{test.upper()} test complete. Results saved in {output_filename}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="iPerf3 Client Setup")
    parser.add_argument('-ip', type=str, required=True, help='IP address to bind the client')
    parser.add_argument('-port', type=int, required=True, help='Port to run the client on')
    parser.add_argument('-server_ip', type=str, required=True, help='IP address of the iPerf3 server')
    parser.add_argument('-test', type=str, required=True, choices=['tcp', 'udp'], help='Type of test: tcp or udp')
    
    args = parser.parse_args()
    run_client(args.ip, args.port, args.server_ip, args.test)


