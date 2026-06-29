# 🛡️ SafeStream Workspace
### Google Trust & Safety Internal Operations Suite — Live Content Moderation Engine

![Status](https://img.shields.io/badge/Status-Operational-success?style=for-the-badge&logo=google-cloud&logoColor=white)
![Framework](https://img.shields.io/badge/Framework-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![AI Engine](https://img.shields.io/badge/Model-ToxicBERT-blue?style=for-the-badge&logo=huggingface&logoColor=white)

**SafeStream Workspace** is an internal Trust & Safety prototype designed to optimize automated content moderation queues. Built to reflect real-world enterprise infrastructure at scale, the application ingests live video streams, search indexes, metadata, and user interactions via the **YouTube Data API v3**, passing them through a hybrid validation pipeline to evaluate, categorize, and act on platform risk factors in real time.

---

## 🚀 Architectural Design & Flow



The system processes text-based metadata signals through an integrated, multi-tier compliance framework:

1. **Ingestion & Resolution Layer**: Resolves query data by dynamically looking up asset indexes via video metadata catalogs or parsing direct URL nodes (Standard videos, Shorts, and Live Streams).
2. **Hybrid Enforcement Engine**: 
   * **Transformer Layer**: Runs parallel text inference using a multi-label deep learning model (`unitary/toxic-bert`) fine-tuned to classify data against 6 core policy violation verticals.
   * **Heuristic Lexicon Layer**: A localized regex dictionary engine working synchronously alongside the transformer to catch high-risk localized keywords, slang, or context variations that cross-lingual models frequently miss.
3. **Escalation & Queue Routing Logic**: Calculates operational threat vectors and automates workflow routing. If a severe violation threshold is crossed, the asset triggers a crisis workflow bypass directly to senior human review parameters.

---

## 🛠️ Key Technical Implementations

* **Multi-Label AI Classification**: Utilizes deep learning to evaluate compliance data across 6 granular policy verticals simultaneously: *Toxic, Severe Toxic, Obscene, Threat, Insult, and Identity Hate*.
* **Custom Lexicon Overlays**: Proves capability in handling localized regional slang (e.g., Hinglish/Romanized Hindi phrases like "Gatiya log") that standard transformer layers naturally bypass.
* **Operational Dashboard (Material Inspired)**: Tailored using custom CSS injections to match standard Google Admin Console and internal operations tools.
* **State Preservation**: Built using Streamlit `session_state` and resource-cached model loading to maximize server processing efficiency.

---

## 📂 Repository Structure

```text
safestream-tns/
│
├── app.py                  # Core production script & Material UI layout
├── requirements.txt        # Production dependencies (PyTorch, Transformers, etc.)
├── .gitignore              # Access token and environment protection controls
└── README.md               # Operations & engineering documentation