import subprocess
import matplotlib.pyplot as mpl
import json

def main():
    #arrays for scatter plot
    tcp_xs = []
    tcp_ys = []
    udp_xs = []
    udp_ys = []

    #clear mininet then run tests
    subprocess.call(["sudo", "mn", "-c"])
    mbps_8 = subprocess.call(["python3", "network_bottleneck.py", "-bw_bottleneck", "8"])
    if mbps_8 == 0:
        print("8Mbps test ran successfully")
    else:
        print("8Mbps test failed")

    with open("output-tcp-8-100.json", 'r') as f:
        data = json.load(f)
        #calculate percent of bytes received. more useful than raw bytes in my opinion
        percent = float(data["total_bytes_received"])/float(data["total_bytes_sent"])
        tcp_xs.append(8)
        tcp_ys.append(percent)
    with open("output-udp-8-100.json", 'r') as f:
        data = json.load(f)
        percent = float(data["total_bytes_received"])/float(data["total_bytes_sent"]) 
        udp_xs.append(8)
        udp_ys.append(percent)
    

    subprocess.call(["sudo", "mn", "-c"])
    mbps_32 = subprocess.call(["python3", "network_bottleneck.py", "-bw_bottleneck", "32"])
    if mbps_32 == 0:
        print("32Mbps test ran succesffuly")
    else:
        print("32Mbps test failed")

    with open("output-tcp-32-100.json", 'r') as f:
        data = json.load(f)
        percent = float(data["total_bytes_received"])/float(data["total_bytes_sent"])
        tcp_xs.append(32)
        tcp_ys.append(percent)
    with open("output-udp-32-100.json", 'r') as f:
        data = json.load(f)
        percent = float(data["total_bytes_received"])/float(data["total_bytes_sent"]) 
        udp_xs.append(32)
        udp_ys.append(percent)
    
    subprocess.call(["sudo", "mn", "-c"])
    mbps_64 = subprocess.call(["python3", "network_bottleneck.py", "-bw_bottleneck", "64"])
    if mbps_64 == 0:
        print("64Mbps test ran succesffuly")
    else:
        print("64Mbps test failed")
    
    with open("output-tcp-64-100.json", 'r') as f:
        data = json.load(f)
        percent = float(data["total_bytes_received"])/float(data["total_bytes_sent"])
        tcp_xs.append(64)
        tcp_ys.append(percent)
    with open("output-udp-64-100.json", 'r') as f:
        data = json.load(f)
        percent =  float(data["total_bytes_received"])/float(data["total_bytes_sent"])
        udp_xs.append(64)
        udp_ys.append(percent)

    mpl.subplot(1,2,1)
    mpl.scatter(tcp_xs, tcp_ys, label = "tcp")
    mpl.title("TCP")
    mpl.ylabel("Bytes received / Bytes sent")
    
    mpl.subplot(1,2,2)
    mpl.scatter(udp_xs, udp_ys, label = "udp")
    mpl.title("UDP")

    mpl.xlabel("Mbps")
    

    mpl.savefig("analysis.png")


if __name__ == "__main__":
    main()
