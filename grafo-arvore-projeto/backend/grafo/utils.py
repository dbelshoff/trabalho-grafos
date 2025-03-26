class No:
    def __init__(self, valor):
        self.valor = valor  # O valor do nó é atribuído ao atributo 'valor'.
        self.filhos = []  # Inicializa a lista de filhos do nó, que estará vazia inicialmente.

class Grafo:
    def __init__(self, texto):
        self.grafo = self._parse_texto(texto)  # Converte o texto de entrada para um grafo.
        self.raiz = self._encontrar_raiz()  # Encontra e atribui a raiz do grafo.

    def _parse_texto(self, texto):
        grafo = {}  # Dicionário que representará o grafo.
        for linha in texto.strip().split("\n"):  # Itera sobre cada linha do texto.
            elementos = list(map(int, linha.split(",")))  # Converte os elementos da linha para inteiros.
            no_raiz = elementos[0]  # O primeiro elemento é a raiz.
            filhos = elementos[1:]  # Os demais elementos são os filhos da raiz.
            if no_raiz not in grafo:  # Se a raiz não está no grafo, cria um nó para ela.
                grafo[no_raiz] = No(no_raiz)
            for filho in filhos:  # Para cada filho na lista de filhos:
                if filho not in grafo:  # Se o filho não estiver no grafo, cria um nó para ele.
                    grafo[filho] = No(filho)
                grafo[no_raiz].filhos.append(grafo[filho])  # Adiciona o filho à lista de filhos do nó raiz.
        return grafo  # Retorna o grafo construído.

    def _encontrar_raiz(self):
        possiveis_raizes = set(self.grafo.keys())  # Inicializa um conjunto com todas as chaves do grafo (nós).
        for no in self.grafo.values():  # Itera sobre os valores do grafo (os nós).
            for filho in no.filhos:  # Para cada filho de um nó:
                if filho.valor in possiveis_raizes:  # Se o filho for uma raiz possível:
                    possiveis_raizes.remove(filho.valor)  # Remove esse filho das raízes possíveis.
        return self.grafo[possiveis_raizes.pop()] if len(possiveis_raizes) == 1 else None  # Retorna o nó raiz se houver apenas uma raiz possível.

    def eh_binaria(self):
        return all(len(no.filhos) <= 2 for no in self.grafo.values())  # Verifica se todos os nós têm no máximo 2 filhos.

    def eh_completa(self):
        if not self.eh_binaria():  # Se a árvore não for binária, não pode ser completa.
            return False
        fila = [self.raiz]  # Fila para a busca em largura.
        encontrou_folha = False  # Flag que indica se uma folha foi encontrada.

        while fila:
            no = fila.pop(0)  # Retira o primeiro nó da fila.
            if len(no.filhos) < 2:  # Se o nó tem menos de 2 filhos, é uma folha.
                encontrou_folha = True  # Marca que uma folha foi encontrada.
            elif encontrou_folha:  # Se já encontrou uma folha, e o nó atual não tem 2 filhos, não é completa.
                return False
            fila.extend(no.filhos)  # Adiciona os filhos do nó à fila.
        
        return True  # Se o loop terminou sem problemas, a árvore é completa.

    def eh_cheia(self):
        if not self.eh_binaria():  # Se a árvore não for binária, não pode ser cheia.
            return False

        # Fila para a busca em largura
        fila = [(self.raiz, 0)]  # Cada item é uma tupla (nó, nível)
        nivel_folhas = None  # Vamos armazenar o nível das folhas
        while fila:
            no, nivel = fila.pop(0)  # Retira o primeiro nó da fila e o seu nível.
        
            # Verifica se o nó é folha
            if len(no.filhos) == 0:
                # Se ainda não definimos o nível das folhas, definimos agora
                if nivel_folhas is None:
                    nivel_folhas = nivel
                # Se o nível da folha não for o mesmo que o nível das outras folhas, não é cheia
                elif nivel != nivel_folhas:
                    return False
            # Verifica se o nó interno tem exatamente 2 filhos
            elif len(no.filhos) != 2:
                return False
        
            # Adiciona os filhos à fila, incrementando o nível
            for filho in no.filhos:
                fila.append((filho, nivel + 1))
    
        return True  # Se todos os critérios foram cumpridos, a árvore é cheia.

    def eh_bst(self, no=None, min_val=float('-inf'), max_val=float('inf')): 
        if not no:  # Se não for fornecido um nó, começa pela raiz.
            no = self.raiz
        if not self.eh_binaria():  # Se a árvore não for binária, não pode ser uma BST.
            return False  
        if not (min_val < no.valor < max_val):  # Se o valor do nó não estiver dentro dos limites, não é BST.
            return False
        # Verifica recursivamente os filhos esquerdo e direito.
        left_check = self.eh_bst(no.filhos[0], min_val, no.valor) if len(no.filhos) > 0 else True
        right_check = self.eh_bst(no.filhos[1], no.valor, max_val) if len(no.filhos) > 1 else True
        return left_check and right_check  # Retorna True se ambos os lados estiverem corretos.

    def eh_avl(self, no=None):
        if not no:  # Se não for fornecido um nó, começa pela raiz.
            no = self.raiz
        if not self.eh_bst():  # Uma AVL precisa ser uma BST primeiro.
            return False

        # Função recursiva para verificar a altura e o balanceamento.
        def altura_e_balanceada(no):
            if not no:
                return 0, True  # Altura 0 e balanceada.
            # Verifica a altura e balanceamento dos filhos.
            altura_esq, balanceada_esq = altura_e_balanceada(no.filhos[0]) if len(no.filhos) > 0 else (0, True)
            altura_dir, balanceada_dir = altura_e_balanceada(no.filhos[1]) if len(no.filhos) > 1 else (0, True)
            balanceada = abs(altura_esq - altura_dir) <= 1  # A árvore é balanceada se a diferença de altura for no máximo 1.
            return 1 + max(altura_esq, altura_dir), balanceada and balanceada_esq and balanceada_dir  # Retorna altura e balanceamento.

        _, balanceada = altura_e_balanceada(self.raiz)  # Calcula a altura e verifica se está balanceada.
        return balanceada  # Retorna True se a árvore for AVL.

    def tipo_arvore(self):
        if not self.eh_binaria():  # Se não for binária, retorna "Árvore não binária".
            return "Árvore não binária"
        if self.eh_avl():  # Se for uma AVL, retorna "Árvore AVL".
            return "Árvore AVL (Balanceada)"
        if self.eh_bst():  # Se for uma BST, retorna "Árvore BST".
            return "Árvore BST"
        if self.eh_cheia():  # Se for cheia, retorna "Árvore binária cheia".
            return "Árvore binária cheia"
        if self.eh_completa():  # Se for completa, retorna "Árvore binária completa".
            return "Árvore binária completa"
        return "Árvore binária"  # Se não for nenhuma das anteriores, retorna "Árvore binária".

    def altura(self, no=None):
        if not no:  # Se não for fornecido um nó, começa pela raiz.
            no = self.raiz
        if not no.filhos:  # Se o nó não tem filhos, a altura é 0.
            return 0
        # Calcula a altura recursivamente.
        return 1 + max(self.altura(filho) for filho in no.filhos)

    def pre_ordem(self, no=None):
        if not no:  # Se não for fornecido um nó, começa pela raiz.
            no = self.raiz
        resultado = [no.valor]  # A primeira coisa é o valor do nó.
        for filho in no.filhos:  # Percorre todos os filhos.
            resultado.extend(self.pre_ordem(filho))  # Adiciona os valores dos filhos na lista.
        return resultado  # Retorna a lista com a ordem de visitação.

    def em_ordem(self, no=None):
        if not no:  # Se não for fornecido um nó, começa pela raiz.
            no = self.raiz
        resultado = []
        if len(no.filhos) >= 1:  # Se houver pelo menos um filho, percorre o filho esquerdo.
            resultado.extend(self.em_ordem(no.filhos[0]))
        
        resultado.append(no.valor)  # Adiciona o valor do nó atual.
        
        if len(no.filhos) == 2:  # Se houver dois filhos, percorre o filho direito.
            resultado.extend(self.em_ordem(no.filhos[1]))
        
        return resultado  # Retorna a lista com a ordem de visitação.

    def pos_ordem(self, no=None):
        if not no:  # Se não for fornecido um nó, começa pela raiz.
            no = self.raiz
        resultado = []
        for filho in no.filhos:  # Percorre todos os filhos.
            resultado.extend(self.pos_ordem(filho))  # Adiciona os valores dos filhos na lista.
        resultado.append(no.valor)  # Adiciona o valor do nó atual no final.
        return resultado  # Retorna a lista com a ordem de visitação.

    def caminhos(self):       
        if not self.eh_binaria():  # Se a árvore não for binária, não possui caminhos definidos.
            return {"error": "Árvore não é binária e nao possui caminhos"}
    
        # Obtendo os caminhos em pré-ordem, em-ordem e pós-ordem
        pre_ordem_result = self.pre_ordem()
        em_ordem_result = self.em_ordem()
        pos_ordem_result = self.pos_ordem()

        return {
            "pre_ordem": pre_ordem_result,  # Retorna o resultado da pré-ordem.
            "em_ordem": em_ordem_result,    # Retorna o resultado da em-ordem.
            "pos_ordem": pos_ordem_result   # Retorna o resultado da pós-ordem.
        }
