# FastAPI_Indian_Gov_Scheme

<!-- PROJECT TITLE -->
<h1 align="center">🇮🇳 Indian Government Schemes NLP</h1>
<p align="center">
  <b>AI-powered FastAPI application to search and analyze Indian Government schemes using NLP</b>
  <br>
  <sub>Built by <a href="https://github.com/PradeeshVasu">Pradeesh Vasu</a></sub>
</p>

---

<!-- BADGES -->
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.110+-green?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/NLP-TF--IDF-orange?logo=openai&logoColor=white" alt="NLP">
  <img src="https://img.shields.io/badge/Frontend-HTML%20%7C%20CSS-yellow" alt="Frontend">
  <img src="https://img.shields.io/badge/Status-Active-success" alt="Status">
</p>

---

## 🧠 Overview
The **Indian Government Schemes NLP** project enables users to **search, understand, and compare** Indian government schemes using **Natural Language Processing (NLP)**.  

It employs **TF-IDF vectorization** and **cosine similarity** to retrieve the most relevant schemes based on a user’s query — all accessible through a **FastAPI web interface**.

---

## 🚀 Features
- 🔍 **Search Schemes** using plain English queries  
- 🧠 **TF-IDF-based text vectorization** for semantic understanding  
- 📊 **Cosine similarity** to rank the most relevant policies  
- ⚡ **FastAPI backend** for high-speed API responses  
- 🖥️ **User-friendly web interface** built with HTML and Jinja2  
- 💾 **Model persistence** with Joblib for optimized performance  

---

## 🧩 Technologies Used
| Category | Tools / Libraries |
|-----------|------------------|
| **Language** | Python 3.10 |
| **Framework** | FastAPI |
| **NLP Model** | TF-IDF |
| **Similarity Metric** | Cosine Similarity |
| **Frontend** | HTML, Jinja2, CSS |
| **Libraries** | pandas, scikit-learn, joblib, textwrap, uvicorn |

---

## 🗂️ Project Structure
```

Indian_Government_Schemes_NLP/
│
├── app.py                        # Main FastAPI application
├── policy_vectorizer.pkl         # Trained TF-IDF vectorizer
├── policy_tfidf_matrix.pkl       # Stored TF-IDF matrix for policies
│
├── templates/
│   └── index.html                # User interface template
│   └── login.html
│   └── results.html
│   └── signup.html
├── static/                       # CSS, JS, or images
│
├── train/                        # Training data files
├── test/                         # Testing data files
├── updated_data/                 # Preprocessed policy dataset
│
├── requirements.txt              # Python dependencies
└── README.md                     # Documentation

````
### Create Login credentials

1. The Login credentials are created using using html codes
2. The login credentials allow users in after entering their "Name" and "Password"
3. The details of the users are stored in MySQL database 

<img width="1918" height="1086" alt="Screenshot 2025-11-19 172126" src="https://github.com/user-attachments/assets/603e7915-d9e1-4c51-a7ec-e24f9c7893db" />

<img width="1919" height="1082" alt="Screenshot 2025-11-19 172146" src="https://github.com/user-attachments/assets/d3b34266-7f08-423b-ab3f-7688643bc5f7" />

### Install and Open MYSQL

1. Enter user password in the MySQL server.                                         
2. Create a sql database.                                                                                                                   
3. Place the password, sql database name in your app.py code                                                                                        
4. After this run your FastAPI server using hte steps mentioned below

<img width="1919" height="1139" alt="Screenshot 2025-11-19 172614" src="https://github.com/user-attachments/assets/ed732666-6759-474b-8f04-8c5693ee4698" />

<img width="1149" height="474" alt="Screenshot 2025-11-19 172703" src="https://github.com/user-attachments/assets/7979fd2c-5865-455f-837a-dddf5bb3a8bc" />

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/PradeeshVasu/Indian_Government_Schemes_NLP.git
cd Indian_Government_Schemes_NLP
````

### 2️⃣ Create a Virtual Environment

```bash
python -m venv env
env\Scripts\activate      # On Windows
# or
source env/bin/activate   # On Linux / Mac
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the FastAPI Server

```bash
uvicorn app:app --reload
```

### 5️⃣ Access the Application

Visit 👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

<img width="1911" height="1088" alt="Screenshot 2025-11-19 172209" src="https://github.com/user-attachments/assets/023fa3dd-4b3d-4451-860b-ec9a579cd5c1" />

<img width="1898" height="1083" alt="Screenshot 2025-11-19 172228" src="https://github.com/user-attachments/assets/17b2272e-0608-4a06-adc6-f31821d09c89" />


## 🧠 How It Works

1. The user enters a text query (e.g., *“agriculture subsidy for farmers”*).
2. The query is vectorized using **TF-IDF**.
3. **Cosine similarity** compares it with all stored policy descriptions.
4. The system returns the **most relevant schemes**, ranked by similarity score.

---

## 💡 Example Query

**Input:**

> “Financial help for women entrepreneurs”

**Output:**

* **Scheme:** Stand-Up India Scheme
* **Relevance Score:** 0.924
* **Benefits:** Loans for women and SC/ST entrepreneurs
* **Eligibility:** Women aged 18–60 starting a new enterprise
* **Application:** Apply through the official portal

---

## 🧰 Requirements

```
fastapi
uvicorn
pandas
scikit-learn
joblib
jinja2
textwrap3
```

---

## 🔮 Future Enhancements

* 🤖 Integrate **Transformer models (BERT)** for deeper semantic search
* 🌐 Add **multilingual support** (Hindi, Tamil, Telugu, etc.)
* 🎙️ Enable **voice-based queries** for better accessibility
* ☁️ Deploy as a **public API** with authentication

---

## 👨‍💻 Author

**Pradeesh Vasu**                
🎓 B.Tech in Computer Science Engineering          
💼 Experienced in Machine Learning, NLP & FastAPI Projects            
💬 Passionate about AI-driven social impact solutions

---

## 📬 Contact

* 📧 **Email:** [pradeeshvasu22@gmail.com](mailto:pradeeshvasu22@gmail.com)
* 💼 **LinkedIn:** [linkedin.com/in/pradeesh-vasu-03486b319](https://www.linkedin.com/in/pradeesh-vasu-03486b319)
* 🧑‍💻 **GitHub:** [github.com/PradeeshVasu](https://github.com/PradeeshVasu)

---

<p align="center">
  <i>“Empowering citizens through AI-driven access to government welfare data.”</i>
</p>

---

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
  <img src="https://img.shields.io/badge/Status-Production%20Ready-success" alt="Status">

</p>

