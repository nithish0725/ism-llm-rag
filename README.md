
# ISM AI Study Assistant Using LLM and RAG

An AI-powered study assistant designed to help students prepare for Information Storage Management (ISM) examinations using Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG).

## Overview

The system retrieves relevant information from ISM study materials and uses a language model to generate contextual answers. Students can select an answer length based on examination marks.

## Key Features

- PDF text extraction and preprocessing
- Text chunking for document retrieval
- Semantic retrieval of relevant study material
- LLM-based answer generation
- Exam-oriented responses for 2, 5, 10, 12, 15, and 20 marks
- Streamlit-based web interface
- Colab notebook for model experimentation

## Technology Stack

- Python
- Streamlit
- Hugging Face Transformers
- Qwen2.5-1.5B-Instruct
- Sentence Transformers
- ChromaDB
- FastAPI
- Google Colab

## Architecture

1. **Document Processing:** Extract text from ISM PDF study materials.
2. **Chunking:** Divide extracted text into smaller passages.
3. **Retrieval:** Find passages relevant to a student's question using semantic similarity.
4. **Answer Generation:** Supply the question and retrieved context to the language model.
5. **User Interface:** Display the generated answer through Streamlit.

## Project Structure

```text
ISM_LLM_RAG/
├── app.py
├── pdf_processor.py
├── chunking.py
├── build_vector_db.py
├── retriever.py
├── requirements.txt
├── ISM_LLM_FineTuning.ipynb
└── README.md
```

## Setup

1. Clone this repository.
2. Create and activate a Python virtual environment.
3. Install the required packages from `requirements.txt`.
4. Configure the document paths, vector database, model, and API settings.
5. Run the document processing and vector database scripts as required.
6. Start the Streamlit interface using:

```bash
streamlit run app.py
```

## Current Status

The document retrieval pipeline and Streamlit interface have been developed and tested. The hosted inference backend still requires configuration because the previous Google Colab GPU session and temporary Cloudflare tunnel are not currently available.

LoRA fine-tuning was attempted but not completed successfully.

## Future Improvements

- Reliable hosted inference
- Improved retrieval quality
- Source citations in generated answers
- Evaluation of answer relevance and faithfulness
- Enhanced deployment and error handling

## Disclaimer

This is an academic project developed for educational purposes. Generated answers should be checked against the official course materials.
