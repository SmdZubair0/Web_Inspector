# 🌐 DOM Locator Generator  

A Python application that generates **robust locators** (XPath, CSS Selector, ID) for any given DOM element.  
Built with **LangGraph** and **lxml**, this tool helps in automating element identification for testing, scraping, and AI-driven web automation.  

---

## 🚀 Features  
- Accepts **full DOM** as input.  
- Element can be specified either:  
  - Directly as input  
  - Or by providing a **query**  
- Generates:  
  - **XPath**  
  - **CSS Selector**  
  - **ID (if available)**  
- Modular design for easy integration into automation/testing pipelines.  

---

## 📂 Project Structure  

```
project-root/
│
├── src/
│   ├── main/
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── config.py
│   │   │
│   │   ├── generator/
│   │   │   ├── base/
│   │   │   │   └── (base classes for selectors/strategies)
│   │   │   |   ├── BasicSelectorProvider.py
│   │   │   |   ├── LocatorStrategy.py
│   │   │   |   ├── ParentExplorer.py
│   │   │   |   ├── Runner.py
│   │   │   |   ├── SiblingExplorer.py
│   │   │   |   └── __init__.py
│   │   │   |
|   │   │   ├── helpers/
|   │   │   │   ├── CssSelectorHelper.py
|   │   │   │   ├── IdHelper.py
|   │   │   │   ├── XPathHelper.py
|   │   │   │   └── __init__.py
│   │   │   |
|   │   │   ├── locators/
|   │   │   │   ├── CssSelectorLocator.py
|   │   │   │   ├── IdLocator.py
|   │   │   │   ├── XPathLocator.py
|   │   │   │   └── __init__.py
│   │   │   ├── __init__.py
|   |   |   |
│   │   ├── models/
│   │   │   ├── base/
│   │   │   │   ├── EmbeddingModel.py
│   │   │   │   ├── GenerativeModel.py
│   │   │   │   └── VectorStoreInterface.py
│   │   │   ├── embeddings/
│   │   │   │   ├── HuggingFaceEmbeddings.py
│   │   │   │   └── __init__.py
│   │   │   ├── llms/
│   │   │   │   ├── ElementNamingModel.py
│   │   │   │   └── __init__.py
|   │   │   ├── vector_stores/
|   │   │   │   ├── FaissVectorStore.py
|   │   │   │   └── __init__.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── readers/
│   │   │   ├── DOMReader.py
│   │   │   ├── HTMLReader.py
│   │   │   ├── XMLReader.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── Locator.py
│   │   │   ├── LocatorState.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── searchers/
│   │   │   ├── SearchHelper.py
│   │   │   ├── SearchWithEmbeddings.py
│   │   │   ├── SearchWithLLM.py
│   │   │   ├── Searcher.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── utils/
│   │   │   ├── DomExplorer.py
│   │   │   ├── GetPageSource.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── validators/
│   │   │   ├── ValidateLocator.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── main.py
│   │   └── __init__.py
│   │
├── └── resources/
│   |   ├── dom.html
│   |   ├── dom.xml
│   |   ├── dom2.html
│   |   ├── dom2.xml
│   |   ├── element_selector.js
│   └── __init__.py
│
├── test/
│   ├── d.ipynb
│   ├── dev.ipynb
│   ├── notebook.ipynb
├── README.md
├── requirements.txt
└── note.txt

```

## 🛠️ Installation  

1. Clone the repo  
   ```bash
   git clone https://github.com/SmdZubair0/Web_Inspector.git
   cd dom-locator-generator
```
