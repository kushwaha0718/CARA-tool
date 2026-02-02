<h1 align="center">📄 Contract Analysis & Risk Assessment Tool (CARA)</h1>

<p align="center">
  A GenAI-powered legal assistant that helps users understand contracts, identify risks, and make informed decisions — built for real-world use.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-App-brightgreen" />
  <img src="https://img.shields.io/badge/Python-3.10+-blue" />
  <img src="https://img.shields.io/badge/Status-Active-success" />
</p>

<hr/>

<h2>🚀 Live Demo</h2>

<p>
👉 <a href="https://caratoolbykushwaha.streamlit.app" target="_blank">
<strong>View Deployed App on Streamlit Cloud</strong>
</a>
</p>

<hr/>

<h2>🧠 Why this project?</h2>

<p>
Contracts are long, complex, and often confusing — especially for individuals and small businesses.
During a hackathon challenge, I built <strong>CARA</strong> to simplify contract analysis by breaking documents into readable insights:
</p>

<ul>
  <li>📌 What type of contract is this?</li>
  <li>⚠️ Where are the risks?</li>
  <li>❓ Which clauses are ambiguous?</li>
  <li>😊 Is the overall sentiment positive or risky?</li>
</ul>

<p>
Everything runs locally or on Streamlit Cloud — no paid APIs required.
</p>

<hr/>

<h2>✨ Key Features</h2>

<ul>
  <li>📤 Upload contracts (PDF / DOCX / TXT)</li>
  <li>📄 Automatic clause extraction</li>
  <li>🏷 Entity detection (Parties, Dates, Jurisdiction, Amounts)</li>
  <li>⚠️ Risk identification & scoring (Low / Medium / High)</li>
  <li>❓ Ambiguity detection</li>
  <li>😊 Sentiment analysis</li>
  <li>📊 Clean dashboard UI with visual indicators</li>
  <li>📥 Export analysis as PDF or JSON</li>
  <li>🕵️ Audit logging of user actions</li>
</ul>

<hr/>

<h2>🛠 Tech Stack</h2>

<table>
<tr>
  <td><strong>Frontend</strong></td>
  <td>Streamlit (custom CSS)</td>
</tr>
<tr>
  <td><strong>NLP</strong></td>
  <td>spaCy, NLTK, Transformers (Hugging Face)</td>
</tr>
<tr>
  <td><strong>Models</strong></td>
  <td>en_core_web_sm, distilGPT-2</td>
</tr>
<tr>
  <td><strong>Backend</strong></td>
  <td>Pure Python (modular architecture)</td>
</tr>
<tr>
  <td><strong>Deployment</strong></td>
  <td>Streamlit Community Cloud</td>
</tr>
</table>

<hr/>

<h2>📁 Project Structure</h2>

<pre>
CARA-tool/
│
├── app.py                 # Main Streamlit app
├── requirements.txt
│
├── core/
│   ├── extraction.py      # Text & clause extraction
│   ├── analysis.py        # Risk & sentiment analysis
│   ├── generation.py      # Clause explanations & suggestions
│   ├── audit.py           # Audit logging
│   └── nlp_setup.py       # NLP model initialization
│
├── ui/
│   └── styles.py          # Custom UI styles
</pre>

<hr/>

<h2>⚙️ Local Setup</h2>

<ol>
  <li><strong>Clone the repository</strong></li>
</ol>

```bash
git clone https://github.com/kushwaha0718/CARA-tool.git
cd CARA-tool
pip install -r requirements.txt
streamlit run app.py

<hr/> <h2>🧩 Challenges & Learnings</h2> <ul> <li>Handling NLP models on Streamlit Cloud</li> <li>Graceful fallbacks when spaCy / NLTK resources are unavailable</li> <li>Designing a modular, production-friendly project structure</li> <li>Balancing performance with explainability</li> </ul> <p> These challenges significantly improved my understanding of deploying NLP-heavy applications in constrained cloud environments. </p> <hr/> <h2>🔮 Future Improvements</h2> <ul> <li>Clause comparison across multiple contracts</li> <li>Custom risk thresholds per contract type</li> <li>User authentication & saved history</li> <li>Improved NER for legal-specific entities</li> </ul> <hr/> <h2>👤 Author</h2> <p> <strong>Ayush Kushwaha</strong><br/> Aspiring Data Scientist | NLP & AI Enthusiast </p> <p> 🔗 <a href="https://github.com/kushwaha0718" target="_blank">GitHub</a> </p> <hr/> <p align="center"> ⭐ If you find this project useful, consider starring the repository! </p> ```