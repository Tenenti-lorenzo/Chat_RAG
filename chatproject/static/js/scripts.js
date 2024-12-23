// Funzione per aggiornare la chat nella pagina
function updateChat(message, response) {
    const chatBox = document.getElementById('chatBox');
    chatBox.innerHTML += `<p><b>Tu:</b> ${message}</p>`;
    chatBox.innerHTML += `<p><b>Risposta:</b> ${response}</p>`;
    chatBox.scrollTop = chatBox.scrollHeight;  // Scorre automaticamente in fondo alla chat
}

// Funzione per inviare il messaggio e ottenere la risposta
function sendMessage() {
    const message = document.getElementById('message').value;
    
    // Verifica se c'è un messaggio da inviare
    if (message.trim() !== '') {
        // Aggiorna la chat immediatamente con il messaggio inviato
        updateChat(message, 'In attesa della risposta...');

        // Svuota il campo di input del messaggio
        document.getElementById('message').value = '';
        
        // Ottieni il token CSRF dal meta tag
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        
        // Invia il messaggio al backend
        fetch('/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken  // Includi il token CSRF nell'intestazione
            },
            body: new URLSearchParams({
                'message': message,
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Dati ricevuti dal backend:", data);
            if (data.message && data.response) {
                updateChat(data.message, data.response);
            } else {
                console.error("Errore: dati non validi ricevuti.");
            }
        })
        .catch(error => {
            console.error('Errore:', error);
        });
    }
}

// Funzione per caricare il file
function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    fetch('/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert('File caricato con successo: ' + data.file_url);
    })
    .catch(error => {
        console.error('Errore nel caricamento del file:', error);
    });
}

// Funzione per inviare il messaggio quando si preme il tasto "Enter"
function checkEnter(event) {
    if (event.key === 'Enter') {
        event.preventDefault();  // Evita il salto di linea
        sendMessage();  // Invia il messaggio
    }
}
