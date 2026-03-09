🧠 Subjective Answer Evaluation System

The **Subjective Answer Evaluation System** is an AI-powered web application built with **Machine Learning**, **NLP**, and **Django**.  
It automatically evaluates students' **subjective (theory-based)** answers by comparing them with model answers — providing fair, fast, and consistent grading.

---

## 🚀 Features

- 📄 Upload and process handwritten or typed student answers using **OCR**.
- 🧩 Compare student answers with model answers using **TF-IDF** and **SVM**.
- 🔍 Generate accurate similarity scores and assign marks automatically.
- 💻 Built with an easy-to-use **Django web interface**.
- 📊 View results and analytics instantly.

---

## 🛠️ Tech Stack

- **Backend:** Python (Django Framework)
- **Machine Learning:** Scikit-learn, TF-IDF, SVM
- **OCR:** Pytesseract, OpenCV
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite (default in Django)

---

## 📂 Project Structure

```
subjective_analysis/
│
├── manage.py
├── requirements.txt
├── dataset/                # Model answers and student answers
├── ml_model/               # SVM + TF-IDF model training files
├── evaluation/             # Django app for evaluation logic
├── templates/              # HTML templates for UI
├── static/                 # CSS, JS, and image files
└── ocr/                    # OCR scripts for text extraction

````

---

## ⚙️ Installation & Setup

Follow these simple steps to run the project on your local machine:

### 1️⃣ Clone the repository
```bash
git clone https://github.com/mayurit83/subjective-answer-evaluation-system.git
cd subjective-answer-evaluation-system
````

### 2️⃣ Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate       # For Windows
# OR
source venv/bin/activate    # For macOS/Linux
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run database migrations

```bash
python manage.py migrate
```

### 5️⃣ Start the Django development server

```bash
python manage.py runserver
```

### 6️⃣ Open in browser

Visit → **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 📘 How It Works

1. Upload the **model answer** and **student answer**.
2. System extracts text using **OCR (Optical Character Recognition)**.
3. Text is processed with **TF-IDF** vectorization.
4. **SVM classifier** predicts a similarity score between model and student answers.
5. Final marks are displayed on the web interface.

---

## 🧑‍💻 Example Output

| Student   | Model Answer Similarity | Marks (%) |
| --------- | ----------------------- | --------- |
| Student 1 | 0.89                    | 9/10      |
| Student 2 | 0.75                    | 7/10      |
| Student 3 | 0.56                    | 5/10      |



