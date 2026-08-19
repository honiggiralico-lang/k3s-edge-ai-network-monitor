# K3s Edge AI Network Anomaly Detector

Questo progetto integra competenze DevOps, Networking (Telecomunicazioni) e Intelligenza Artificiale.
L'obiettivo è creare un sistema di rilevamento anomalie di rete (es. attacchi DDoS) in tempo reale, 
utilizzando un cluster K3s su Proxmox bare-metal.

## Architettura
- **Infrastruttura:** Proxmox VE (1 Master Fedora, 2 Workers Debian)
- **Orchestrazione:** K3s
- **Applicazione:** API in Flask (Python) che gira in container Docker
- **AI:** Modello di Machine Learning (scikit-learn) per l'anomaly detection, addestrato offline.

## Fasi del Progetto
1. Addestramento del modello AI su dati di rete sintetici.
2. Sviluppo dell'API Flask per l'inferenza in tempo reale.
3. Deploy su K3s e raccolta del traffico reale dai nodi Linux.
