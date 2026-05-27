
# Homework Club Hub 🚀

Welcome to the **Homework Club Hub**, an innovative digital ecosystem built during the **Indigenomics CreatorJam** contest. This project is a modern, community-driven platform designed to bridge the educational gap by seamlessly connecting volunteer tutors with students seeking academic support. 

Instead of relying on traditional, manual coding workflows, this platform was built using a cutting-edge, specification-first methodology outlined in the [CreatorJam SpecKit](https://github.com/indigenomicsxyz/CreatorJamSpecKit/tree/main). The entire development pipeline was driven by autonomous AI orchestration:

1. **The Blueprint:** We first designed a comprehensive, structured specification file (`vision-spec`)[specs/homework-club-hub/vision-spec.md] that served as the single source of truth—defining the product vision, core user personas (students, parents, and tutors), data structures, and UI layout requirements.
2. **The Synthesis:** We then used the **Hermes Agent** to ingest this specification. Hermes autonomously parsed the system architecture, mapped dependencies, and generated a functional, streamlined product directly from the spec file.

By combining structured conceptual planning with agentic product delivery, this project demonstrates how AI-driven workflows can rapidly transform a community need into a beautifully designed, functional web platform.

---

# 🛠️ I. Hermes Setup & Installation

Follow these steps to configure your environment, install the Hermes Agent, and connect to the CreatorJam AI endpoint.

### 1. Review the Specification Guidelines
Before creating your blueprint, review the **TEAM-PLAYBOOK** documentation included in this repository to understand the required structure and configurations for your spec file.

### 2. Install Hermes Agent
Open PowerShell on Windows and run the official installation script:

```powershell
iex (irm [https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1](https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1))
```

### 3. Configure the AI Endpoint
- API Base URL: https://regen.gaiaai.xyz/events/creator-jam/api/v1
- API Key: (Enter your assigned CreatorJam token)

### 4. Update and Launch

```bash
hermes update
hermes
```

---

# 🛠️ II. Design the Spec

* Check the [TEAM-PLAYBOOK](TEAM-PLAYBOOK.md) file to understand the required structure and foundational configurations for setting up a valid product specification.
* The active specification designed for this project is stored and maintained inside [specs/homework-club-hub/vision-spec.md](specs/homework-club-hub/vision-spec.md).

---

# 🛠️ III. Explore the Project

### Step 1: Clone & Switch Branches
Open your preferred terminal:
```bash
git clone https://github.com/wallrue/CreatorJam_Homework-Club-Hub.git
cd CreatorJam_Homework-Club-Hub
git switch team-2
```

**Below are the steps to design the new interface (if you just want to run the current website, skip Step 2)**

### Step 2: Launch the Hermes
Open your preferred terminal:
```bash
cd \path\to\CreatorJam_Homework-Club-Hub
Hermes
The spec is in specs\homework-club-hub\vision-spec, the database is homework_club_hub.db, backend is app.py, please design the front-end pages based on vision-spec
```
Troubleshooting:
- If you encounter a time-out problem, please close/restart your terminal and try executing Step 2 again.
- Open Hermes dashboard, remove all old sessions and change models Qwen/Gemma

### Step 3: Start the Backend Server Application
Open an Anaconda Prompt (or your primary terminal with Python environment):
```bash
cd \path\to\CreatorJam_Homework-Club-Hub
python app.py
```
Then access: http://localhost:5000/

---
