import argparse
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

import server
import client
import subprocess
import json

# define classnetwork_bottleneck.py: error: unrecognized arguments: --bw_bandwidth 12
class BottleneckTopo(Topo):

    # build function to create mininet
    def build(self, bw_bottleneck, bw_other):
        # create switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # create hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')

        # create links
        self.addLink(h1, s1, bw=bw_other)
        self.addLink(h2, s1, bw=bw_other)
        self.addLink(h3, s2, bw=bw_other)
        self.addLink(h4, s2, bw=bw_other)
        self.addLink(s1, s2, bw=bw_bottleneck)

# Function to run basic topology tests
def run_topology_tests(bw_bottleneck, bw_other):
    topo = BottleneckTopo(bw_bottleneck, bw_other)
    net = Mininet(topo)
    net.start()
    
    with open('output-network-config.txt', 'w') as file_config:
        file_config.write('Network Configuration:\n')
        file_config.write(f'Bottleneck bandwidth: {bw_bottleneck} Mbps\n')
        file_config.write(f'Other links bandwidth: {bw_other} Mbps\n')
        file_config.write("Node connections:\n")
        for link in net.links:
            node1 = link.intf1.node
            node2 = link.intf2.node
            file_config.write(f"{node1} <--> {node2}\n")
    
    for n in range(1, 5):
        host = net.get(f'h{n}')
        result = host.cmd('ifconfig')
        with open(f'output-ifconfig-h{n}.txt', 'w') as file_ifconfig:
            file_ifconfig.write(result)
        with open(f'output-ping-h{n}.txt', 'w') as file_ping:
            for i in range(1, 5):
                if n != i:
                    to_ping = net.get(f'h{i}')
                    ping_result = host.cmd(f'ping -c 1 {to_ping.IP()}')
                    file_ping.write(f'Pinging from h{n} to h{i}:\n{ping_result}\n')

    net.stop()

# New function to run iPerf3 performance tests for TCP and UDP
def run_perf_tests(bw_bottleneck, bw_other):
    # Define IPs for your Mininet hosts
    h1_ip = '10.0.0.1'
    h3_ip = '10.0.0.3'
    h2_ip = '10.0.0.2'
    h4_ip = '10.0.0.4'

    # Setup Mininet topology
    topo = BottleneckTopo(bw_bottleneck, bw_other)
    net = Mininet(topo)
    net.start()

    # Get hosts
    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')
    h4 = net.get('h4')

    # Start iPerf3 server on h3 (TCP) and h4 (UDP)
    print("Starting iPerf3 servers on h3 (TCP) and h4 (UDP)")
    h3.cmd('python3 server.py -ip {} -port 5201 &'.format(h3_ip))  # TCP server
    h4.cmd('python3 server.py -ip {} -port 5201 &'.format(h4_ip))  # UDP server

    # Run iPerf3 TCP client on h1 (to h3) for 60 seconds
    print("Running TCP client from h1 to h3")
    h1.cmd('python3 client.py -ip {} -port 5201 -server_ip {} -test tcp'.format(h1_ip, h3_ip))
    
    # Run iPerf3 UDP client on h2 (to h4) for 60 seconds
    print("Running UDP client from h2 to h4")
    h2.cmd('python3 client.py -ip {} -port 5201 -server_ip {} -test udp'.format(h2_ip, h4_ip))
    

    #set filenames for output
    tcp_output_filename = f"output-tcp-{bw_bottleneck}-{bw_other}.json"
    udp_output_filename = f"output-udp-{bw_bottleneck}-{bw_other}.json"

    tcp_output = {}
    udp_output = {}

    with open("output-tcp.json", 'r') as file:
        tcp_output = json.load(file)
    with open("output-udp.json", 'r') as file:
        udp_output = json.load(file)

    #error checking
    tcp_data = tcp_output
    if (type(tcp_output) == "string"):
        print("TCP error: " + tcp_output)
    else:
        tcp_data = {"protocol":"tcp", "total_bytes_sent":tcp_output['end']['sum_sent']['bytes'], "total_bytes_received":tcp_output['end']['sum_received']['bytes']}

    udp_data = udp_output
    if (type(udp_output) == "string"):
        print("UDP error: " + udp_output)
    else:
        l_p = float(udp_output['end']['sum']['lost_percent'])
        total_received = int((1-(l_p/100)) * int(udp_output['end']['sum']['bytes']))

        udp_data = {"protocol":"udp", "total_bytes_sent":udp_output['end']['sum']['bytes'], "total_bytes_received":total_received}    

    with open(tcp_output_filename, 'w') as file:
        json.dump(tcp_data, file)
    with open(udp_output_filename, 'w') as file:
        json.dump(udp_data, file)

    
    # Stop the network
    net.stop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create a Mininet with specified bottlenecks.")
    parser.add_argument('-bw_bottleneck', type=int, default=10, help="Bandwidth of bottleneck in Mbps.")
    parser.add_argument('-bw_other', type=int, default=100, help="Bandwidth of other links in Mbps.")
    parser.add_argument('-time', type=int, default=10, help="Duration of the traffic simulation in seconds.")
    args = parser.parse_args()

    setLogLevel('info')
    
    # First, run topology tests
    run_topology_tests(args.bw_bottleneck, args.bw_other)
    
    # Then, run performance tests
    run_perf_tests(args.bw_bottleneck, args.bw_other)
