from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from .utils import Grafo

class UploadGrafoView(APIView):
    parser_classes = [MultiPartParser]  # Alterado para MultiPartParser

    def post(self, request, format=None):
        # Verifica se o arquivo foi enviado
        if 'file' not in request.FILES:
            return Response({"error": "Nenhum arquivo enviado."}, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file']
        
        try:
            # Lê o conteúdo do arquivo e processa
            texto = file.read().decode('utf-8')
            grafo = Grafo(texto)

            # Retorna a resposta com os dados calculados
            return Response({
                #"eh_arvore": grafo.eh_arvore(),
                "tipo_arvore": grafo.tipo_arvore(),
                "altura": grafo.altura(),
                "caminhos": grafo.caminhos()
            })

        except Exception as e:
            return Response({"error": f"Erro ao processar o grafo: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)