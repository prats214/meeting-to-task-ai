<h1>Add ReadMe</h1>

# Meeting-to-Task AI

Convert meeting conversations into **structured, actionable tasks** using AI.

---

## Overview

Meeting-to-Task AI is an end-to-end system that transforms **raw meeting audio** into:

* Clean transcripts
* Structured tasks with ownership
* Deadlines and priorities
* Actionable summaries

It bridges the gap between **unstructured discussions** and **execution-ready outputs**.

---

## System Pipeline

```text
Audio → Speech-to-Text → LLM Processing → Structured JSON → UI Display
```

---

## Core Components

### 1. Speech-to-Text (STT)

* Converts audio into text using **Whisper (faster-whisper)**
* Handles real-time or uploaded audio files
* Includes basic text cleaning (removing fillers, formatting)

---

### 2. LLM Task Extraction

* Processes transcript using an LLM
* Extracts structured information:

  * Task
  * Assigned To
  * Assigned By (if available)
  * Deadline
  * Priority
* Outputs clean, consistent JSON for downstream use

---

### 3. Frontend Interface (Streamlit)

* Simple UI for uploading audio files
* Displays:

  * Transcript
  * Extracted tasks
* Designed for fast, interactive demos

---

## Tech Stack

* Python
* faster-whisper (Speech-to-Text)
* OpenAI API / LLM
* Streamlit
* pydub + ffmpeg

---

## Running the Project

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the application

```bash
streamlit run main.py
```

### 3. Use the app

* Upload a meeting audio file (.mp3 / .wav)
* Click **Process**
* View transcript and extracted tasks

---

## Sample Output

```json
{
  "tasks": [
    {
      "task": "Complete frontend UI",
      "assigned_to": "Nidhi",
      "assigned_by": "Team Lead",
      "deadline": "Friday evening",
      "priority": "High"
    },
    {
      "task": "Develop backend APIs",
      "assigned_to": "Gaurav",
      "assigned_by": "Team Lead",
      "deadline": "Saturday night",
      "priority": "High"
    }
  ],
  "summary": "Discussion covered frontend, backend, integration, and deadlines."
}
```

---

## Use Cases

* Team meetings
* Project planning sessions
* Academic group discussions
* Event coordination
* Healthcare task management

---

##  Key Highlights

* Converts unstructured speech into structured insights
* Works across multiple domains (tech, healthcare, events)
* Fast and lightweight (optimized for hackathon use)
* Modular pipeline (STT → LLM → UI)

---

## Team

* **Nidhi** — Speech-to-Text Pipeline
* **Gaurav** — LLM & Task Extraction
* **Prarthana** — Frontend 

---



