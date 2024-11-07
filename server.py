import argparse
import iperf3

def run_server(ip, port):
    server = iperf3.Server()
    server.bind_address = ip
    server.port = port

    print(f"Starting iPerf3 server on {ip}:{port}")
    while True:
        result = server.run()
        if result.error:
            print(f"Error: {result.error}")
        else:
            print("Server is running...")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="iPerf3 Server Setup")
    parser.add_argument('-ip', type=str, required=True, help='IP address to bind the server')
    parser.add_argument('-port', type=int, required=True, help='Port to run the server on')
    
    args = parser.parse_args()
    run_server(args.ip, args.port)
