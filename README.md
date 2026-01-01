# Smart Agri Platform (Hack Era '25) 🌾

![Event](https://img.shields.io/badge/Hackathon-Hack_Era_2025-orange?style=for-the-badge)
![Role](https://img.shields.io/badge/Role-Team_Lead-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Result-Finalist_Submission-success?style=for-the-badge)

> **Competition Entry:** Built for **Hack Era 2025** at GITAM University, Hyderabad.
> **Role:** Team Lead (Squad of 4)

## 🖼️ Project Overview
A full-stack agricultural ecosystem designed to bridge the digital divide for rural farmers using voice accessibility and real-time market data.
![Main Dashboard](./preview-main.jpg)

---

## 🧠 Leadership & Methodology
As the **Team Lead**, I was responsible for architectural decisions, time management, and code integration during the tight hackathon deadline.

### ⏱️ Time Management Strategy
* **Triage & Prioritization:** We adopted an "MVP-First" approach, ensuring the core **Text-to-Speech (TTS)** and **Market API** features were functional within the first 12 hours before refining the UI.
* **Parallel Development:** I split the team into two streams—Frontend (Dashboard/UI) and Backend (API/Data Logic)—and managed merge conflicts to keep the main branch stable.

### 💡 The Problem & Solution
* **The Challenge:** Most Agri-Tech apps are text-heavy and require literacy, alienating the actual farmers who need them.
* **Our Solution:** An "Accessibility-First" interface that *speaks* to the farmer in their local language and uses visual indicators (Red/Green trends) instead of complex charts.

---

## 🌟 Key Features Showcase

### 1. Accessibility Engine (TTS)
We integrated the Web Speech API to read out navigation, prices, and alerts. This ensures farmers with low literacy can still navigate the app confidently.
* **Multi-Language Support:** Dynamic switching for regional accessibility.

**Feature Preview:**
![Accessibility Features](./preview-features.jpg)
*(Snapshot showing Voice Controls and Language Options)*

### 2. Live Market Intelligence
Real-time connection to agricultural endpoints to fetch current mandi (market) prices.
* **Logic:** Updates asynchronously to prevent page reloads.

---

## 🏗️ Technical Architecture
The system relies on a robust backend to handle data processing and serve the responsive frontend.

**Live-Prices Structure:**
![Live-Prices](./preview-backend.jpg)

### 🛠️ Tech Stack
* **Frontend:** HTML5, CSS3 (Responsive Grid), JavaScript (Vanilla).
* **Backend:** Python / Node.js (Scalable Architecture).
* **APIs:** Web Speech API, Open Government Data Platform (Agriculture).

## 🚀 How to Run Locally
```bash
# 1. Clone the repository
git clone [https://github.com/sumanthkatta-dev/smart-agri-platform-fullstack.git](https://github.com/sumanthkatta-dev/smart-agri-platform-fullstack.git)

# 2. Navigate into directory
cd smart-agri-platform-fullstack

# 3. Start the application
# (Refer to backend specific instructions in the repo)
