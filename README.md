# Chat Application with File Upload, FAISS Database & OpenAI Integration 💬📂🤖

Welcome to the **Chat Application with FAISS and OpenAI** repository! This project is a Django-powered web application where users can chat, upload files, and interact with the data stored in a FAISS database. The files are vectorized and stored, allowing the app to generate relevant responses using OpenAI’s language models.

## 📚 Overview

This application includes the following features:
- **File Uploads**: Users can upload files (e.g., PDFs, text files, etc.).
- **FAISS Vectorization**: Uploaded files are vectorized using the FAISS library and stored in a database for efficient similarity search.
- **OpenAI Integration**: After uploading and vectorizing the files, the app uses OpenAI’s API to answer user queries based on the contents of the files.

## 🛠️ Features
- **Chat Interface**: A simple yet effective chat interface for users to send queries and receive answers.
- **File Management**: Support for uploading and managing files, which are stored in a FAISS database.
- **Real-time Responses**: Based on the contents of the uploaded files, the app responds to questions using OpenAI’s GPT models, providing accurate and context-aware answers.
- **FAISS Search**: FAISS is used to index and search through the vectorized data, enabling fast and relevant responses.

## 🔧 Getting Started

### Prerequisites
To get started with this project, you’ll need the following:
- Python 3.x
- Django
- FAISS
- OpenAI API key (sign up at [OpenAI](https://beta.openai.com/signup/) if you don't have one yet)
- PostgreSQL (or another database supported by Django)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Tenenti-lorenzo/Chat_RAG.git
   ```

2. Navigate to the project folder:
   ```bash
   cd Chat_RAG/chatproject
   ```

3. Set up a virtual environment and install the dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

4. Set up your database. Make sure you have PostgreSQL (or the database of your choice) installed and configured. Then run:
   ```bash
   python manage.py migrate
   ```

5. Add your OpenAI API key to the environment variables:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"  # On Windows, use set instead of export
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Open your browser and go to [http://127.0.0.1:8000](http://127.0.0.1:8000) to start interacting with the application.

### How to Use
1. **Upload Files**: Use the file upload feature to upload documents (PDFs, text files, etc.).
2. **Vectorize and Store**: The application will automatically vectorize the file content and store it in the FAISS database.
3. **Ask Questions**: Use the chat interface to ask questions. The app will use the contents of the uploaded files and OpenAI’s API to generate a relevant response.

## ⚙️ Architecture

- **Django Backend**: Manages user authentication, file uploads, and API interactions.
- **FAISS Database**: Stores the vectorized content of the uploaded files for efficient similarity search.
- **OpenAI API**: Generates responses based on the file contents and user queries.

## 📝 Notable Files & Directories
- **`/app/`**: Main application code for handling uploads, file management, and interaction with FAISS/OpenAI.
- **`/templates/`**: HTML templates for the chat interface and file upload form.
- **`/static/`**: Static files for CSS and JavaScript to enhance the user interface.
- **`/settings.py`**: Django settings, including configuration for FAISS, the database, and OpenAI API keys.

## 🚀 Contributing
We welcome contributions to improve this application! Feel free to open issues, suggest features, or submit pull requests. If you want to enhance the application with new functionalities, don’t hesitate to contribute your ideas.

### Ideas for Contributions
- **File type support**: Add support for more file types like images, audio, or other document formats.
- **Advanced Query Handling**: Improve the AI model’s ability to answer more complex queries.

## 🤝 Support
If you encounter any issues or have questions about the project, please create an issue in this repository or contact me directly.

---

Happy chatting and file uploading! Let’s make AI even more helpful and accessible! 🚀

