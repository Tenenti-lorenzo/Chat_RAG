import openai
import os
import openai
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from llama_index.core import SimpleDirectoryReader
from uuid import uuid4
from langchain_core.documents import Document

# Configurazione chiave API OpenAI

class ChatService:
    _instance = None  # Variabile per memorizzare l'istanza unica della classe

    def __new__(cls, openai_api_key, vector_store_path, embeddings):
        """
        Metodo per creare o restituire l'istanza unica della classe.
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.__init__(openai_api_key, vector_store_path, embeddings)
        return cls._instance

    def __init__(self, openai_api_key, vector_store_path, embeddings):
        """
        Inizializzazione dell'istanza del servizio di chat.
        """
        # Inizializzazione solo se la classe non è stata già inizializzata
        if not hasattr(self, "initialized"):
            openai.api_key = openai_api_key  # Imposta la chiave API di OpenAI
            self.embeddings = embeddings
            self.vector_store_path = vector_store_path
            self.new_vector_store = FAISS.load_local(vector_store_path, embeddings, allow_dangerous_deserialization=True)
            self.initialized = True  # Segna come inizializzato
            self.client = openai.OpenAI(
                    # This is the default and can be omitted
                    api_key=os.environ.get("OPENAI_API_KEY"),
                )
            
    # Load and encode documents using SimpleDirectoryReader
    def encode_documents_with_reader(self,directory_path):
        loader = SimpleDirectoryReader(directory_path)
        documents = loader.load_data()
        doc_ids = [str(uuid4()) for _ in documents]
        print("encode")
        # Convert documents to LangChain Document format if necessary
        langchain_documents = [
            Document(page_content=doc.text, metadata=doc.metadata)
            for doc in documents
        ]
        print("add lingestion")
        self.new_vector_store.add_documents(documents=langchain_documents, ids=doc_ids)
        print("end lingestion")

    def query_index(self, query):
        """
        Esegui la ricerca nei documenti locali tramite il vector store
        """
        # Ottieni l'embedding della query
        query_embedding = self.embeddings.embed_query(query)
        
        # Esegui la ricerca per similitudine
        results = self.new_vector_store.similarity_search_by_vector(query_embedding, k=3)
        
        # Concatenare il testo dei documenti più pertinenti
        relevant_content = "\n".join([result.page_content for result in results])  # Ottieni il contenuto dei documenti più rilevanti
        
        return relevant_content
    
    def give_me_a_question(self, query):
        """
        Usa OpenAI per rispondere alla query, utilizzando i contenuti rilevanti trovati tramite `query_index`.
        """
        # Ottieni i contenuti rilevanti per la query
        relevant_content = self.query_index(query)
        
        # Prepara il prompt per il modello GPT-3.5 o GPT-4
        prompt = f"Context: {relevant_content} rispondi in italiano\n\nQuestion: {query}"
        
        # Esegui la richiesta al modello OpenAI
        response =  self.client.chat.completions.create(
            model="gpt-3.5-turbo",  
            temperature=0.0,
            top_p=0.0,
            messages=[
                {"role": "system", "content": "Documental RAG for retrive information of documantation."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Restituisci la risposta del modello
        return response


# Funzione di utilità per ottenere una risposta tramite ChatService
def get_chat_response(query):
    """
    Funzione di utilità per interagire con il servizio di chat (questa è la funzione che chiamerai nel backend Django).
    """
    openai_api_key = os.environ.get("OPENAI_API_KEY")  # Recupera la chiave API da variabili di ambiente
    vector_store_path = "./chat/bando_faiss"  # Specifica il percorso del tuo vector store
    embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
    print(os.getcwd())
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)

    # Crea o recupera l'istanza singleton della classe ChatService
    chat_service = ChatService(openai_api_key, vector_store_path, embeddings)
    
    # Ottieni la risposta dalla funzione give_me_a_question
    response = chat_service.give_me_a_question(query)
    print(response.choices[0].message.content)
    # Restituisci solo il contenuto del messaggio della risposta
    return response.choices[0].message.content

def delete_all_files_in_directory(directory_path):
    try:
        # Controlla se la directory esiste
        if os.path.exists(directory_path) and os.path.isdir(directory_path):
            # Cicla su tutti gli elementi nella directory
            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)
                # Verifica se è un file e non una cartella
                if os.path.isfile(file_path):
                    #os.remove(file_path)  # Elimina il file
                    print(f"File {filename} rimosso.")
                else:
                    print(f"{filename} non è un file, saltato.")
        else:
            print(f"La directory {directory_path} non esiste o non è una directory.")
    except Exception as e:
        print(f"Errore durante l'eliminazione dei file: {e}")
# Funzione di utilità per ottenere una risposta tramite ChatService
def add_doc():
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    # Imposta il percorso del vector store, dove sono memorizzati i vettori di embedding
    vector_store_path = "./chat/bando_faiss"  # Specifica il percorso del tuo vector store
    # Specifica il modello di embedding che verrà utilizzato per generare i vettori
    embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Stampa la directory di lavoro corrente (utile per il debug)
    print(os.getcwd())

    # Crea un'istanza dell'oggetto HuggingFaceEmbeddings, che gestisce gli embeddings
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)

    # Crea o recupera l'istanza singleton della classe ChatService, passando la chiave API di OpenAI,
    # il percorso del vector store, e l'oggetto embeddings appena creato.
    chat_service = ChatService(openai_api_key, vector_store_path, embeddings)
    
    # Usa la funzione 'encode_documents_with_reader' della classe ChatService per codificare i documenti
    # dalla cartella "./media" e memorizzarli nel vector store per una futura ricerca.
    print("Iniziamo lingestion")
    response = chat_service.encode_documents_with_reader("./media")
    delete_all_files_in_directory("./media")
    print("end delete")
    # La funzione non restituisce nulla (None), quindi non c'è un valore di ritorno esplicito.
    return