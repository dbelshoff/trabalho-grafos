from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from .utils import Grafo

# Classe responsável pelo endpoint da API que permite o upload de um arquivo contendo um grafo(arvore)
class UploadGrafoView(APIView):
    # Define que esta API aceita arquivos no formato multipart/form-data (necessário para upload de arquivos)
    parser_classes = [MultiPartParser]

    # Método para tratar requisições POST
    def post(self, request, format=None):
        # Verifica se um arquivo foi enviado na requisição
        # O request.FILES contém todos os arquivos enviados via upload
        if 'file' not in request.FILES:
            # Se nenhum arquivo for encontrado, retorna uma resposta de erro com status HTTP 400 (Bad Request)
            return Response({"error": "Nenhum arquivo enviado."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Obtém o arquivo enviado pelo cliente
        file = request.FILES['file']
        
        try:
            # Lê o conteúdo do arquivo e converte os bytes para string utilizando decodificação UTF-8
            texto = file.read().decode('utf-8')
            
            # Cria uma instância da classe Grafo passando o conteúdo do arquivo como argumento
            # essa classe irá processar os dados e criar uma estrutura de grafo
            grafo = Grafo(texto)

            # Retorna uma resposta HTTP 200 (OK) com os dados processados do grafo
            return Response({
                "tipo_arvore": grafo.tipo_arvore(),  # Obtém o tipo da árvore gerada a partir do grafo
                "altura": grafo.altura(),  # Calcula a altura da árvore gerada
                "caminhos": grafo.caminhos()  # Determina os caminhos existentes dentro do grafo
            })

        except Exception as e:
            # Se ocorrer qualquer erro durante o processamento do arquivo ou do grafo, retorna um erro HTTP 500 (Internal Server Error)
            # A mensagem do erro é incluída para ajudar na depuração
            return Response({"error": f"Erro ao processar o grafo: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
