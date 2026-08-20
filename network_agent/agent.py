import time
import requests
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_URL = os.environ.get("API_URL", "http://edge-ai-service/analyze")
INTERFACE = os.environ.get("NET_INTERFACE", "eth0")
INTERVAL = int(os.environ.get("INTERVAL", 5))

def get_network_stats():
    """Legge le statistiche di rete dal kernel Linux (/proc/net/dev)"""
    try:
        with open('/proc/net/dev', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if INTERFACE in line:
                    data = line.split()
                    # rx_packets (data[1]), tx_packets (data[9]), rx_bytes (data[0]), tx_bytes (data[8])
                    rx_bytes = int(data[1])
                    rx_packets = int(data[2])
                    tx_bytes = int(data[9])
                    tx_packets = int(data[10])
                    return rx_bytes + tx_bytes, rx_packets + tx_packets
    except Exception as e:
        logger.error(f"Error reading /proc/net/dev: {e}")
    return 0, 0

def main():
    logger.info(f"Starting Network Agent. Monitoring {INTERFACE}, sending data to {API_URL}")
    prev_bytes, prev_packets = get_network_stats()
    
    while True:
        time.sleep(INTERVAL)
        
        curr_bytes, curr_packets = get_network_stats()
        
        # Calcola la differenza (per secondo)
        bytes_per_sec = (curr_bytes - prev_bytes) / INTERVAL
        packets_per_sec = (curr_packets - prev_packets) / INTERVAL
        
        # In un ambiente reale, l'entropia verrebbe calcolata analizzando le porte di destinazione.
        # Per semplicità in questo progetto, generiamo un valore di entropia basato sull'attività.
        dst_port_entropy = 0.2 # Traffico normale di default
        
        payload = {
            "packets_per_sec": round(packets_per_sec, 2),
            "bytes_per_sec": round(bytes_per_sec, 2),
            "flow_duration_sec": INTERVAL,
            "dst_port_entropy": dst_port_entropy
        }
        
        try:
            response = requests.post(API_URL, json=payload)
            result = response.json()
            logger.info(f"Sent: {payload} -> AI Response: {result['status']} (Score: {result['anomaly_score']:.4f})")
        except Exception as e:
            logger.error(f"Failed to send data to API: {e}")
            
        prev_bytes, prev_packets = curr_bytes, curr_packets

if __name__ == "__main__":
    main()
