# AskDocsAI

AskDocsAI is an AI-powered document search and question-answering application. It allows users to upload documents in various formats (PDF, DOCX, XLSX), search for relevant information within the documents, and ask questions about the content. The application uses OpenAI's language models for natural language processing and document embeddings to perform efficient search operations.

## Features

- Upload multiple documents in PDF, DOCX, or XLSX format.
- Extract text from uploaded documents using various document loaders.
- Split large documents into smaller chunks for efficient search operations.
- Create embeddings for document chunks using OpenAI's language models.
- Store document embeddings in a FAISS index for fast similarity search.
- Perform similarity search to find relevant documents based on user queries.
- Use OpenAI's language models for question-answering on the relevant documents.

## Installation

To run the AskDocsAI application, you need to follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/faisal-saddique/AskDocsAI.git
   cd AskDocsAI
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:

   The application uses environment variables for configuration. Rename the `.env.template` file to `.env` file in the project directory and set the required variables:

   ```
   OPENAI_API_KEY=<your_openai_api_key>

   ```

   Replace `<your_openai_api_key>` with your OpenAI API key. Change the other settings according to your preference.

4. Run the Streamlit application:

   ```bash
   streamlit run app.py
   ```

   The application should now be accessible at `http://localhost:8501` in your web browser.

## Usage

1. Upload Documents:

   - Go to 'Create KnowledgeBase' page.
   - Click on the "Upload one or more files" button.
   - Select one or more documents in PDF, DOCX, or XLSX format to upload.

2. Perform Search and Question-Answering:

   - Go to 'ChatBot' page.
   - Enter a question in the text input box provided.
   - Click the "Search" button.
   - The application will perform a similarity search to find relevant documents and display the top matching chunks from those documents.
   - Click on the "Show Matched Chunks" expander to see the detailed content of each matched chunk.
   - The application will then use OpenAI's language models to answer the question based on the relevant documents.

3. Explore Results:

   - The application will display the answer to the question along with the elapsed time for the search and question-answering process.

## Additional Notes

- The application uses OpenAI's language model for natural language processing. You can change the model by updating the `MODEL_NAME` environment variable in the `.env` file.

- The application uses FAISS, a library for efficient similarity search on large datasets. The document embeddings are stored in the FAISS index for fast search operations.

- The application uses FAISS to store document embeddings for efficient retrieval during similarity search.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

The AskDocsAI application uses various libraries and technologies, including:

- OpenAI GPT-3.5 Turbo language model
- Streamlit for creating interactive web applications
- FAISS for vector indexing and retrieval
- PyMuPDF and pytesseract for document parsing and text extraction
- pandas for data manipulation

## Contributions

Contributions to this project are welcome. If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request.

## Contact

If you have any questions or inquiries about the project, you can contact the project owner:

Name: [Faisal Saddique](https://github.com/faisal-saddique)

Email: [faisalsaddique7964@example.com]