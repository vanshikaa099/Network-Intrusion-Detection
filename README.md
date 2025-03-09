# **Network Intrusion Detection in SDN**

## 📌 Project Overview  
This project focuses on detecting and mitigating **DDoS attacks** in a **Software-Defined Networking (SDN)** environment using **Mininet** and the **Ryu controller**. It involves:  
- Generating a **custom dataset**  
- Training a **machine learning model**  
- Implementing **real-time traffic monitoring**  
- Applying **firewall-based mitigation strategies**  

## ⚙️ Technologies Used  
- **Mininet** – Creates a virtual network topology  
- **Ryu Controller** – Manages and controls network traffic  
- **Python** – Used for dataset processing, model training, and live traffic monitoring  
- **Machine Learning** – Classifies network traffic as benign or malicious  
- **Firewall Mechanisms** – Implements blacklist and whitelist-based mitigation  

---

## 📊 Dataset Generation  

### **Why a Custom Dataset?**  
Publicly available datasets often contain anomalies, leading to models that achieve **100% accuracy** but fail in real-world scenarios. To address this, we generate our **own dataset** with realistic attack patterns.  

### **How It Works:**  
1. **Topology Creation** – A network topology is set up in Mininet.  
2. **Traffic Control** – The Ryu controller manages traffic flows between nodes.  
3. **DDoS Attack Simulation** – Malicious traffic is introduced to simulate attacks.  
4. **Benign Traffic Generation** – Normal traffic is recorded for training.  
5. **Dataset Preparation** – The collected traffic data is **preprocessed** and **labeled**.  

---

## 🧠 Machine Learning Model  

- The dataset is split into **DDoS attack traffic** and **benign traffic**.  
- A machine learning model is trained on this dataset, achieving **99% accuracy**.  
- The trained model is integrated into the **live network monitoring system** for real-time intrusion detection.  

---

## 🔥 Attack Detection & Mitigation  

### **Live Traffic Monitoring**  
- The model continuously **analyzes network packets**.  
- If **DDoS traffic** is detected, **mitigation strategies** are applied.  

### **Firewall-Based Mitigation**  
- **Blacklist Firewall** – Blocks detected malicious IPs.  
- **Whitelist Firewall** – Ensures trusted IPs remain unaffected.  
- **IP List Management** – Maintains an updated **blacklist** and **whitelist** for faster processing.  

---

## 🚀 How to Run the Project  

### **1️⃣ Start the Ryu Controller (Ubuntu VM)**  
1. **Check your IP address**  
   ```bash
   ifconfig

### **2️⃣ Set up the mininet **  
1. **Navigate to mininet diretory**  
    ```run the following
    nano topology.py
    sudo python topology.py

### **3️⃣ Simulate a DDOS**  
1. **Run the hping command**
   ```
   h1 hping3 -S --flood -p 80 h2
