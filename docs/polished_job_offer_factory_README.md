
# Job Offer Factory Autorun

Job Offer Factory Autorun is an end‑to‑end job search automation pipeline.  Built by Alex Minnick, it turns cumbersome applications into a repeatable, operator‑friendly workflow.

## 🎯 What It Does

* **Parses job descriptions** to extract keywords, skills and requirements.
* **Generates tailored materials** – resumes, cover letters and outreach messages customised to each role.
* **Scores your fit** and highlights where you meet or exceed requirements.
* **Logs every application** into a tracker (`applications.json`) and produces an action dashboard so you never lose track.
* **Drafts LinkedIn posts and About sections** to optimise your online presence.

## 🛠 Architecture

The pipeline is written in Python and orchestrated via modular functions:

1. **Input parser** – ingests job descriptions and tokenises them into required and preferred skills.
2. **Resume generator** – assembles your master resume into a customised version that emphasises relevant experience.
3. **Cover letter writer** – crafts concise, persuasive letters referencing the company’s mission and your projects.
4. **Outreach DM creator** – produces short, human‑sounding messages for recruiters or hiring managers.
5. **Tracker & dashboard** – logs each application with status and follow‑up dates and outputs a Markdown dashboard summarising your search.

## ✅ Why Use It

Applying manually wastes hours and leads to generic applications.  Job Offer Factory Autorun scales your effort: send high‑quality, customised applications to multiple roles in minutes while retaining the human touch.  Check the generated files, make any tweaks, then submit.  It’s like having a personal assistant for your job hunt.
