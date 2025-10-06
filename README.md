# 🧠 Multi-Agent Research Assistant using Context Engineering

> Build a **multi-agent research assistant** powered by **context engineering** — integrating documents, web search, memory, and research papers to deliver accurate, contextual responses.

---

## 📘 Overview

This project demonstrates how to apply **Context Engineering (CE)** principles to build a **multi-agent system** that gathers and filters information from multiple sources before generating an intelligent response.

Traditional prompt engineering focuses on “magic words.”  
**Context Engineering**, on the other hand, ensures that LLMs receive:
- ✅ The **right information**  
- 🧰 The **right tools**  
- 🧩 In the **right format**

This allows the model to reason more effectively and generate more accurate, grounded outputs.

---

## ⚙️ Workflow

The assistant gathers, filters, and synthesizes information using the following **context engineering pipeline**:

1. **User submits a query**
2. **Fetch context** from:
   - 📄 Documents (via Tensorlake)
   - 🌐 Web (via Firecrawl)
   - 🧠 Memory (via Zep)
   - 📚 Research papers (via ArXiv API)
3. **Aggregate and filter** context using a *context evaluation agent*
4. **Generate response** using a *synthesizer agent*
5. **Save the final response** back to memory (Zep)

<img src="https://github.com/user-attachments/assets/058b1fdd-e358-4590-a373-61ad810b1bc9" alt="workflow" width="600" height="480" />

---

## 🧠 Implementation Note

This project is **adapted from the “Daily Dose of DS” article on Context Engineering**.  
Original concept and architecture credit go to **Daily Dose of DS**.  

🔗 Source: [Daily Dose of DS – Context Engineering Demo](https://github.com/patchy631/ai-engineering-hub/tree/main/context-engineering-workflow) *(original thread reference)*

In this implementation,  
> 🧩 I have **replaced the original LLM integration with the Gemini API** for response generation, while maintaining the same multi-agent workflow structure.

---
