# 🏹 The Self-Correcting AI Agent (V-1.0)

 Welcome to the **Central Nervous System (CNS)** of a truly "Smart" agent. While most agents just search and guess, this one **re-thinks** when it fails.

## 🏛️ 1. The "Deep Why" 
Most AI scripts follow a **Linear Path**: Input ➔ Process ➔ Output.
The problem? Real world data is messy. If Wikipedia returns garbage, a linear agent delivers garbage.

This project implements a **Self-Correction Loop**. In the industry, this is known as **Re-Ranking** or **Verification-based Retrieval**. It ensures that the "Brain" (LLM) checks the "Hands" (Tools) before speaking to the "User".

## 🎨 2. Analogy: The Executive Assistant 
Imagine you have an assistant.
*   **Linear Assistant**: You ask for the CEO's number. He spends 5 seconds on Google, finds a fake number, and gives it to you. You fail.
*   **This Agent**: He finds a number, but before calling you, he thinks: *"Wait, this is an old office number, doesn't match the query."* He goes back, searches for the "Current CEO", finds the right one, and then delivers.

## 🧠 3. How it Works (The 5-Step Logic)
1.  **User Input**: Receives a query (e.g., "What is Capitalism?").
2.  **Hands (The Tool)**: Uses `WikipediaQueryRun` to pull the first 500 characters of a result.
3.  **Eyes (The Semantic Judge)**: A dedicated LLM call acts as a **Judge**. It strictly outputs `YES` or `NO` by comparing the query to the result.
4.  **The Refiner**: If the Judge says `NO`, the agent doesn't give up. It creates a **New Search Keyword** based on why the first one failed.
5.  **CNS (The Loop)**: It repeats this process up to **3 times** before concluding.

## 🛠️ 4. Tech Stack
*   **Framework**: [LangChain](https://www.langchain.com/) (The Orchestrator)
*   **Brain**: Google Gemini 2.0 Flash (via [OpenRouter](https://openrouter.ai/))
*   **Tools**: Wikipedia API Wrapper
*   **Environment**: Python + Dotenv

## 🚀 5. How to Run
1.  **Clone it**: `git clone https://github.com/AmanSoni1-apex/Agent-s.git`
2.  **Setup .env**: Add your `OPENROUTER_API_KEY`.
3.  **Install deps**: `pip install langchain-openai langchain-community python-dotenv`
4.  **Execute**: `python agent.py`
