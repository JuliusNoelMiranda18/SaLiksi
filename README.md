<p align="center">
  <img src="saliksi/public/logo.png" alt="SaLiksi Logo" width="120" />
</p>

<h1 align="center">SaLiksi</h1>

<p align="center">
  <em>"Ang maliksing pananaliksik"</em> — The agile research tool for Filipino scholars.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Next.js-16-black?logo=next.js" alt="Next.js 16" />
  <img src="https://img.shields.io/badge/React-19-61DAFB?logo=react" alt="React 19" />
  <img src="https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript" alt="TypeScript" />
  <img src="https://img.shields.io/badge/TailwindCSS-4-06B6D4?logo=tailwindcss" alt="Tailwind CSS 4" />
  <img src="https://img.shields.io/badge/Groq_AI-LLaMA_3.3--70B-orange" alt="Groq AI" />
</p>

---

## 🧐 What is SaLiksi?

**SaLiksi** is an AI-powered academic research platform designed specifically for **Filipino students and researchers**. It provides an end-to-end research workflow — from discovering credible sources and generating research topics, to writing papers, generating citations, and practicing thesis defense — all with a strong focus on **Philippine-context data** and local academic databases.

### At a Glance

| Metric | Value |
|---|---|
| **Lines of Code** | ~13,800 LoC (TypeScript) |
| **Source Files** | 61 |
| **API Endpoints** | 22 server-side routes |
| **React Components** | 26 |
| **Dashboard Pages** | 8 |
| **External APIs** | 7 integrations |
| **AI-Powered Features** | 12+ |
| **Academic Papers Accessible** | 250M+ (via OpenAlex & Semantic Scholar) |

---

## ✨ Features

### 🔍 Academic Search Engine
Unified search across **OpenAlex**, **Semantic Scholar**, and **PHILJOL** with AI-powered autocomplete, credibility scoring (0–100), layman summaries, and a Philippine institution filter.

### 🧠 AI Research Tools
A suite of AI-driven analysis tools operating on your saved sources:
- **Literature Synthesis** — common findings, contradictions, and gaps
- **Gap Detection** — CRITICAL/SIGNIFICANT research gaps with suggested directions
- **Knowledge Graph** — interactive canvas visualization of papers, concepts, authors, and regions
- **Contradiction Catcher** — verify thesis claims against selected literature

### 📝 Writer with AI Copilot
Full WYSIWYG editor powered by **TipTap** (15+ extensions) with a vault-aware AI copilot that can cite, rephrase, expand, check, summarize, and find sources from your research library. Export to **PDF** and **DOCX**.

### 💡 Topic Generator
Discover research topics with **20 curated Philippine problems** (transport, climate, agriculture, health, etc.) and **9 research frontiers** (Project NOAH, Blue Carbon, Coral Restoration, etc.). Location-based topic generation using **OpenStreetMap**.

### 📑 Citation Generator
Generate properly formatted citations in **APA 7th**, **MLA 9th**, and **Chicago 17th** with metadata resolution from CrossRef, Semantic Scholar, and HTML meta-tag scraping. Input via URL/DOI, file upload, or directly from your library.

### 🛡️ Credibility Scorer
AI-driven source evaluation with an **A–F grading system** across peer review status, accreditation (CHED/PHILJOL/Scopus), and publisher reputation. Visual dashboard with animated gauges and expandable dimension breakdowns.

### 📚 Research Library
Folder-based organization with article storage, PDF upload with AI metadata extraction, notebooks, and a vault system for attaching context to your AI copilot.

### ⚔️ Thesis Defenders
A **gamified thesis defense simulator** styled as a Pokémon-like battle. Face 3 AI panelists (Dr. Cruz, Prof. Garcia, Dr. Santos) across 5 rounds with an HP-based battle system, retro pixel aesthetics, and real-time answer evaluation.

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| **Framework** | Next.js 16 (App Router) |
| **Frontend** | React 19, TypeScript |
| **Styling** | TailwindCSS 4, Framer Motion |
| **AI Backend** | Groq SDK — 4-model LLM failover cascade (LLaMA 3.3-70B → Mixtral 8x7B → LLaMA 3.1-8B → Gemma2-9B) |
| **Rich Text Editor** | TipTap (15+ extensions) |
| **Data Sources** | OpenAlex, Semantic Scholar, PHILJOL, CrossRef |
| **Maps** | Leaflet + OpenStreetMap |
| **Storage** | localStorage + IndexedDB (client-side, privacy-first) |
| **PDF Processing** | pdfjs-dist (read), html2pdf.js (export) |
| **DOCX Export** | html-to-docx, docx |
| **Icons** | Lucide React, React Icons |
| **Typography** | Neue Montreal (custom OTF) |

---

## 📁 Project Structure

```
saliksi/
├── app/
│   ├── (dashboard)/          # Dashboard pages
│   │   ├── researcher/       # Academic search engine
│   │   ├── topic-generator/  # AI topic discovery
│   │   ├── library/          # Research library
│   │   ├── writer/           # TipTap editor + AI copilot
│   │   ├── credibility/      # Source credibility scorer
│   │   ├── aitools/          # AI analysis suite
│   │   ├── citation/         # Citation generator
│   │   └── defenders/        # Thesis defense game
│   └── api/                  # 22 API routes
│       ├── research/         # Paper search (OpenAlex, S2, PHILJOL)
│       ├── credibility/      # Credibility analysis
│       ├── synthesis/        # Literature synthesis
│       ├── gaps/             # Gap detection
│       ├── graph/            # Knowledge graph
│       ├── citation/         # Citation generation
│       ├── defenders/        # Defense game endpoints
│       └── ...               # 13 more routes
├── components/               # Reusable React components
├── lib/                      # Shared utilities & contexts
└── public/                   # Static assets & fonts
```

---

## 🚀 Getting Started

### Prerequisites

- **Node.js** 18+
- **npm** or **yarn**
- A **Groq API key** ([get one here](https://console.groq.com))

### Installation

```bash
# Clone the repository
git clone https://github.com/JuliusNoelMiranda18/SaLiksi.git
cd SaLiksi/saliksi

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
```

Add your Groq API key to the `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### Running Locally

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Building for Production

```bash
npm run build
npm start
```

---

## 🔑 Environment Variables

| Variable | Description | Required |
|---|---|---|
| `GROQ_API_KEY` | API key for Groq AI (powers all AI features) | ✅ |

---

## 🎨 Design System

| Element | Value |
|---|---|
| **Primary (Maroon)** | `#521118` |
| **Dark** | `#2b090d` |
| **Background** | `#FAF8F5` / `#e8e4df` |
| **Font** | Neue Montreal (custom OTF) |
| **Effects** | Glassmorphism, grain/noise textures, decorative blurs |
| **Animations** | Framer Motion — page transitions, hover effects, progress indicators |

---

## 🌏 Philippine Context

SaLiksi is purpose-built for Filipino researchers:

- 🇵🇭 **PHILJOL** integration for Philippine journal articles
- 🏫 **CHED accreditation** checks in credibility scoring
- 📍 **Location-based** topic generation via OpenStreetMap
- 🧠 **20 curated PH research problems** covering transport, climate, maritime, health, agriculture, and more
- 🔬 **9 research frontiers** featuring Philippine initiatives (Project NOAH, Abaca for Space Tech, Blue Carbon from Mangroves)
- 💚 **Sensitive content detection** with Philippine mental health hotline information

---

## 🤖 AI Architecture

SaLiksi uses a **4-model LLM failover cascade** via Groq for maximum reliability:

```
LLaMA 3.3-70B → Mixtral 8x7B → LLaMA 3.1-8B → Gemma2-9B
```

All AI calls use **structured JSON-mode** responses with automatic rate-limit detection and model fallback. Temperature ranges from `0.1` (factual tasks) to `0.3` (creative generation).

### AI-Powered Features (12+)

| Feature | Endpoint |
|---|---|
| Search Autocomplete | `/api/suggestions` |
| Layman Summaries | `/api/layman` |
| Credibility Analysis | `/api/credibility` |
| Literature Synthesis | `/api/synthesis` |
| Gap Detection | `/api/gaps` |
| Knowledge Graph | `/api/graph` |
| Contradiction Catcher | `/api/synthesis` |
| Topic Generation | `/api/generate-topics` |
| Writer Autocomplete | `/api/writer/autocomplete` |
| Vault Copilot | `/api/writer` |
| Defense Questions | `/api/defenders/question` |
| Defense Evaluation | `/api/defenders/evaluate` |

---

## 🔒 Privacy

SaLiksi follows a **privacy-first, zero-database architecture**:

- **All user data** (library, notebooks, settings) is stored **client-side** via `localStorage` and `IndexedDB`
- **No backend database** — no server-side storage of user data
- **No user accounts** — no sign-up or login required
- API calls to Groq are stateless and carry no persistent user identifiers

---

## 📄 License

This project is proprietary. All rights reserved.

---

<p align="center">
  Built with 🇵🇭 for Filipino researchers
</p>