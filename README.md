# Team: The Butterfly Effect  
## CS683 – Final Project Repository

## Project Overview

This project extends the **Berti Prefetcher (MICRO’22)** to improve performance on **server workloads**, which typically exhibit irregular memory access patterns, frequent phase changes, and large working sets. While baseline Berti performs well on SPEC/GAP-style workloads, it suffers from **cold-start issues**, **phase pollution**, and the inability to share useful patterns across different instruction pointers (IPs). :contentReference[oaicite:1]{index=1}

To address these limitations, our team (**The Butterfly Effect**) introduces two major enhancements:

### **1️⃣ Cross-IP Delta Correlation**
- Builds a **Global Delta Graph** to track stride/delta patterns across *all* IPs.  
- Helps new or transient IPs avoid cold-start by borrowing high-confidence deltas.  
- Improves coverage, warm-up time, and overall IPC.  
- Particularly effective for CloudSuite workloads where many IPs are short-lived. :contentReference[oaicite:2]{index=2}

### **2️⃣ Phase-Aware Learning**
- Detects execution phases using miss-rate signatures.  
- Maintains **separate delta histories per phase**, preventing pattern pollution.  
- Ensures each phase learns its own access behavior, improving prediction accuracy.  
- Allows fast re-learning when phases repeat. :contentReference[oaicite:3]{index=3}

---

Our work includes:

- Full Berti-Artifact framework  
- Prefetcher implementations  
- Scripts for building and running simulations  
- Python analysis tools  
- Updated results and plots  
- Explanatory video (link below)

---

## Explanatory Video

Watch our detailed explanation video here:  
**https://drive.google.com/drive/folders/1ZFJ7OCdpGrFQO7NT4e8i89Q7wMzZzURR?usp=drive_link**

---

## 📌 Simulation Configuration

For all our experiments, we used the following configuration:

- **Warmup Instructions:** 5 Million  
- **Simulation Instructions:** 20 Million  

These settings were consistently applied across all workloads and prefetcher evaluations.

---

## 📂 Result Directories

All results generated during the project are stored in the following folders:

- **Original baseline results:**  
  `Berti-Artifact/Originalberti_results/`

- **Our updated final results:**  
  `Berti-Artifact/UpdatedBerti/`


Contains:

- IPC/MPKI CSVs  
- Prefetcher comparison  
- Final graphs used in the report and presentation  

---
## 👥 Team Members

| Name             | Roll Number |
|------------------|-------------|
| Saptarshi Biswas | 22B1258     |
| Madhava Sriram   | 22B1233     |
| Dhruv Meena      | 22B1279     |


