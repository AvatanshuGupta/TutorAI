# TutorAI

**TutorAI** is an AI-powered study assistant web application built with Django. It allows users to upload PDF, from which it can generate interactive quizzes, concise flashcards, and answer user queries using a Retrieval-Augmented Generation (RAG) chatbot. TutorAI leverages Google’s Generative AI models and ChromaDB for embeddings to deliver accurate and context-aware responses.

---

## Features

1. **PDF Upload**

   * Users can upload PDFs (up to 30 pages by default).
   * Uploaded PDFs are processed and split into manageable chunks for embedding and question generation.
   * Supports a wide range of PDF contents including textbooks, research papers, and lecture notes.

2. **RAG Chatbot**

   * The chatbot answers user queries based on the uploaded PDF and general knowledge.
   * Uses a retrieval-augmented approach:

     * **ChromaDB** stores embeddings of PDF chunks.
     * Queries are checked for retrieval need using LLM heuristics.
     * Relevant chunks are fetched from ChromaDB to provide context-aware answers.
   * Streaming responses to users with real-time text display.

3. **Flashcards**

   * Generates concise, meaningful flashcards from the PDF content.
   * Uses the `gemini-2.0-flash-lite` model for flashcard generation.
   * Each flashcard is limited to 50–150 words, focusing strictly on content from the PDF.

4. **Quizzes**

   * Generates multiple-choice questions with 4 options per question.
   * Uses `gemini-2.0-flash` model for quiz generation.
   * Only context-supported questions are generated; hallucination is avoided.
   * Correct option is clearly indicated.

5. **Embeddings**

   * Uses `google/embeddinggemma-300m` for generating embeddings of PDF content.
   * ChromaDB stores and indexes embeddings for semantic similarity search.

6. **Model Usage**

   * **Chatbot core:** `gemini-2.5-flash`
   * **Retrieval check:** `gemma-3-27b`
   * **Flashcard generation:** `gemini-2.0-flash-lite`
   * **Quiz generation:** `gemini-2.0-flash`

---

## Architecture Overview

```
+-----------------+        +------------------+        +----------------+
|  User Interface | <----> |  Django Backend  | <----> |  Generative AI |
+-----------------+        +------------------+        +----------------+
          |                        |                          |
          v                        v                          v
     File Upload               PDF Processing          Google Gemini LLMs
     & Interaction            & Embedding              (Flashcards, Quiz, Chat)
                                 |
                                 v
                             ChromaDB
                         (Embedding Storage)
```

---

## Technologies Used

* **Backend:** Django, Python 3.11
* **Frontend:** Tailwind CSS for responsive and dark-themed UI
* **RAG & LLMs:**

  * `langchain` for orchestrating LLM prompts and retrieval
  * `langchain_google_genai` for Google Gemini API integration
* **Vector Database:** ChromaDB for storing PDF embeddings
* **Parallel Processing:** `concurrent.futures.ThreadPoolExecutor` for concurrent flashcard and quiz generation
* **Environment Management:** `dotenv` for API key management

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/AvatanshuGupta/TutorAI.git

```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set environment variables in a `.env` file:

```env
GOOGLE_API_KEY_AVG=<your-gemini-2.5-flash-key>
GOOGLE_API_KEY_LUC=<your-gemma-3-27b-key>
GOOGLE_API_KEY_VIK=<your-gemini-2.0-flash-lite-key>
GOOGLE_API_KEY_ABH=<your-gemini-2.0-flash-key>
HUGGING_FACE_API=<your-huggingface-api-key>
```

5. Apply migrations and run the server:

```bash
python manage.py migrate
python manage.py runserver
```

---

## Usage

1. **Upload PDF**

   * Navigate to the home page and upload a PDF.
   * Only PDFs with ≤30 pages are allowed by default.

2. **Dashboard**

   * Access the dashboard after PDF upload.
   * View the following options:

     * **Flashcards:** Browse automatically generated flashcards.
     * **Quiz:** Attempt a multiple-choice quiz based on PDF content.
     * **Tutor Chat:** Ask questions related to the PDF content or general queries.

3. **Flashcards**

   * Flashcards are concise and derived strictly from the uploaded PDF.
   * Navigate through flashcards using "Next" and "Previous" buttons.

4. **Quiz**

   * Questions are multiple-choice with 4 options.
   * Only one correct answer is marked.
   * Score is shown at the end of the quiz.

5. **RAG Chatbot**

   * Enter queries in the chatbox.
   * If retrieval is needed, relevant PDF chunks are fetched from ChromaDB.
   * Responses are streamed in real-time.

---

## Code Structure

```
tutorAi/
│
├─ components/
│  ├─ pdf_reader.py       # PDF splitting & reading
│  ├─ quiz.py             # Quiz generation using Gemini-2.0-flash
│  ├─ flashcard.py        # Flashcard generation using Gemini-2.0-flash-lite
│  ├─ embedding.py        # Embedding and similarity search (ChromaDB)
│  └─ chat.py             # Retrieval check and chat helpers
│
├─ templates/
│  ├─ home.html
│  ├─ dashboard.html
│  ├─ flashcards.html
│  └─ quiz.html
│
├─ settings.py            # Django project settings
└─ views.py               # Core views for upload, dashboard, chat
```

---

## Models and LLMs Used

| Task                           | Model                      |
| ------------------------------ | -------------------------- |
| Embeddings                     | google/embeddinggemma-300m |
| Flashcard Generation           | gemini-2.0-flash-lite      |
| Quiz Generation                | gemini-2.0-flash           |
| Retrieval Check / Context Need | gemma-3-27b                |
| Chatbot Core                   | gemini-2.5-flash           |

---

## Notes

* **Security:** Uploaded PDFs are stored temporarily in `media/temp` and removed after session expiry.
* **PDF Limit:** Default max pages is 30 to prevent overloading embeddings and LLM processing.
* **No hallucination:** Flashcards and quiz generation strictly rely on the uploaded PDF content.
* **Parallel Processing:** Flashcards and quizzes are generated concurrently using `ThreadPoolExecutor`.

---

## Future Improvements

* Add **PDF page selection** for embedding to handle very large PDFs.
* Implement **user authentication** for saving quizzes and flashcards.
* Add **multi-language support** for PDF content and flashcards.
* Enhance **chatbot capabilities** with context-aware follow-ups and summarization.
* Deploy on **cloud hosting** with proper GPU support for faster LLM inference.

---

