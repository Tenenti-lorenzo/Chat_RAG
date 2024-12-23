from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .chat_service import get_chat_response,add_doc  # Assicurati di importare correttamente la funzione
from django.core.files.storage import FileSystemStorage

@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        # Verifica se c'è un messaggio nel corpo della richiesta
        if 'message' in request.POST:
            message = request.POST['message']
            
            response = get_chat_response(message)
            print(JsonResponse({"message": message,"response": response}))
            # Restituisce il messaggio e la risposta in formato JSON
            return JsonResponse({
                "message": message,
                "response": response
            })

        # Se è un file
        elif 'file' in request.FILES:
            file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            file_url = fs.url(filename)
            add_doc()

            return JsonResponse({"file_url": file_url})

    # Rende la pagina della chat quando la richiesta è GET
    return render(request, 'chat/chat.html')
