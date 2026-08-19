import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
import joblib
import os

def generate_synthetic_network_data():
    """
    Genera dati di rete finti ma realistici per addestrare il modello.
    Simuliamo due scenari: Traffico Normale (navigazione, API) e Traffico Anomalo (DDoS).
    """
    np.random.seed(42)
    n_normal = 5000
    n_anomalies = 100
    
    # Traffico Normale (BENIGN)
    # Pacchetti/sec: 10-100, Byte: 500-5000, Durata: 1-10 sec
    normal_data = {
        'packets_per_sec': np.random.uniform(10, 100, n_normal),
        'bytes_per_sec': np.random.uniform(500, 5000, n_normal),
        'flow_duration_sec': np.random.uniform(1, 10, n_normal),
        'dst_port_entropy': np.random.uniform(0.1, 0.5, n_normal) # Bassa entropia = porte standard (80, 443)
    }
    normal_df = pd.DataFrame(normal_data)
    
    # Traffico Anomalo (DDoS)
    # Pacchetti/sec: 5000-20000, Byte: 50-200 (pacchetti piccoli e tantissimi), Durata: 0.1-1 sec
    anomaly_data = {
        'packets_per_sec': np.random.uniform(5000, 20000, n_anomalies),
        'bytes_per_sec': np.random.uniform(50, 200, n_anomalies),
        'flow_duration_sec': np.random.uniform(0.1, 1, n_anomalies),
        'dst_port_entropy': np.random.uniform(0.8, 1.0, n_anomalies) # Alta entropia = porte casuali
    }
    anomaly_df = pd.DataFrame(anomaly_data)
    
    # Uniamo i dati
    df = pd.concat([normal_df, anomaly_df], ignore_index=True)
    # Creiamo le etichette: 1 per normale, -1 per anomalia (richiesto da Isolation Forest)
    labels = np.concatenate([np.ones(n_normal), -np.ones(n_anomalies)])
    
    return df, labels

def main():
    print("1. Generazione dei dati sintetici di rete...")
    X, y = generate_synthetic_network_data()
    
    # Mescoliamo i dati
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("2. Addestramento del modello Isolation Forest...")
    # Isolation Forest è perfetto per l'Edge: leggero e veloce
    # contamination = percentuale di anomalie attese (100 / 5100 ~ 0.02)
    model = IsolationForest(n_estimators=100, contamination=0.02, random_state=42)
    model.fit(X_train)
    
    # Valutazione veloce
    from sklearn.metrics import classification_report
    y_pred = model.predict(X_test)
    print("\n--- Report di Addestramento ---")
    print(classification_report(y_test, y_pred, target_names=["Anomalia", "Normale"]))
    
    # Salvataggio del modello
    model_path = os.path.join(os.path.dirname(__file__), 'network_anomaly_model.joblib')
    joblib.dump(model, model_path)
    print(f"\n3. Modello salvato con successo in: {model_path}")
    print("   Puoi copiare questo file nella cartella dell'app Flask!")

if __name__ == "__main__":
    main()
