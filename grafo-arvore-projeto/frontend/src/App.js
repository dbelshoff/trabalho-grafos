import React, { useState } from "react";
import axios from "axios";
import Tree from "react-d3-tree";
import "./App.css";

function App() {
 // Estados do React para armazenar o arquivo selecionado, os resultados do processamento, 
 // mensagens de erro e os dados da árvore para visualização.
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [treeData, setTreeData] = useState(null);

  // Função chamada ao selecionar um arquivo. Ela verifica se um arquivo foi escolhido, 
  // se ele tem o formato correto (.txt) 
  // e armazena o arquivo no estado.
  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    if (!selectedFile) return;

    if (selectedFile.type !== "text/plain") {
      setError("Formato inválido. Apenas arquivos .txt são permitidos.");
      setFile(null);
      return;
    }

    setError(null);
    setFile(selectedFile);
  };

 //Esta função verifica se existem duplicações de nós ou arestas em um grafo representado por uma lista de linhas. 
 // Ela checa se algum nó já foi utilizado como filho em outra linha ou se há arestas duplicadas entre os nós. 
 // Além disso, realiza uma busca em profundidade (DFS) para detectar ciclos no grafo. 
const checkDuplicateNodesInLines = (lines) => {


  //verificação de nos duplicados

  
  // Conjunto para armazenar arestas já vistas (evita duplicações)
  let edges = new Set();
  
  // Objeto para armazenar a lista de adjacência do grafo
  let adjList = {};
  
  // Conjunto para armazenar nós que já foram usados como filhos
  let usedAsChild = new Set();

  // Itera sobre todas as linhas fornecidas
  for (let line of lines) {
      // Separa a linha por vírgulas e remove espaços extras em cada nó
      const nodes = line.split(",").map((node) => node.trim());
  
      // O primeiro nó da linha é o nó pai
      const parent = nodes[0];
      // O restante dos nós são os filhos do nó pai
      const children = nodes.slice(1);
  
      // Verifica se algum nó filho já foi utilizado como pai em uma linha anterior
      for (let child of children) {
          // Se o nó já foi usado como filho antes, retorna true indicando duplicação
          if (usedAsChild.has(child)) {
              return true;  // Nó repetido como pai após já ter sido usado como filho
          }
          // Marca o nó como filho
          usedAsChild.add(child);
      }



      //Verificação de arestas duplicadas
  
      // Verifica duplicação de arestas dentro da linha
      for (let i = 1; i < nodes.length; i++) {
          // Cria a aresta entre dois nós consecutivos
          const edge = `${nodes[i - 1]}-${nodes[i]}`;
          // Cria a aresta reversa (com a ordem invertida)
          const reverseEdge = `${nodes[i]}-${nodes[i - 1]}`;
          
          // Se a aresta ou sua reversa já foram vistas, há uma duplicação
          if (edges.has(edge) || edges.has(reverseEdge)) {
              return true;  // Duplicação de aresta detectada
          }
  
          // Adiciona a aresta ao conjunto de arestas
          edges.add(edge);
      }
  
      // Atualiza a lista de adjacência, associando o nó pai aos seus filhos
      adjList[parent] = children;
  }


  //identificação de ciclos
  
  // Conjunto para marcar os nós já visitados durante a busca em profundidade
  let visited = new Set();
  
  // Conjunto para acompanhar os nós atualmente no caminho da busca (para detectar ciclos)
  let stack = new Set();
  
  // Função de busca em profundidade (DFS) para detectar ciclos no grafo
  const dfs = (node) => {
      // Se o nó já está no caminho atual, um ciclo foi encontrado
      if (stack.has(node)) return true;
      
      // Se o nó já foi visitado, não há ciclo no caminho atual
      if (visited.has(node)) return false;
  
      // Marca o nó como visitado
      visited.add(node);
      // Adiciona o nó à pilha para o caminho atual
      stack.add(node);
  
      // Verifica os vizinhos do nó (nós adjacentes)
      if (adjList[node]) {
          for (let neighbor of adjList[node]) {
              // Se algum vizinho causar um ciclo, retorna true
              if (dfs(neighbor)) return true;
          }
      }
  
      // Remove o nó da pilha após verificar todos os vizinhos
      stack.delete(node);
      return false;
  };
  
  // Itera sobre todos os nós da lista de adjacência para verificar ciclos
  for (let node in adjList) {
      // Se o nó ainda não foi visitado e um ciclo é detectado a partir dele, retorna true
      if (!visited.has(node) && dfs(node)) {
          return true;  // Ciclo detectado
      }
  }
  
  // Se não houver ciclos ou duplicações de aresta, retorna false
  return false;
};



  // Verifica se o grafo representado no arquivo está desconexo.
  // Constrói uma lista de adjacência para mapear conexões entre nós e usa uma busca em largura (BFS) para verificar a conectividade.
  // Se todos os nós não forem alcançados a partir de um único ponto, o grafo é considerado desconexo.
const checkDisconnection = (lines) => {
  // Inicializa a lista de adjacência, onde cada nó terá uma lista de seus nós adjacentes
  let adjList = {};
  
  // Inicializa um conjunto para armazenar todos os nós encontrados no grafo
  let allNodes = new Set();

  // Processa cada linha fornecida para construir a lista de adjacência
  lines.forEach((line) => {
      // Separa a linha em um nó pai e seus filhos, utilizando a vírgula como delimitador
      const [parent, ...children] = line.split(",").map((n) => n.trim());

      // Se o nó pai ainda não existe na lista de adjacência, inicializa-o com uma lista vazia
      if (!adjList[parent]) adjList[parent] = [];

      // Para cada filho do nó pai, atualiza a lista de adjacência
      children.forEach((child) => {
          // Se o nó filho ainda não existe na lista de adjacência, inicializa-o com uma lista vazia
          if (!adjList[child]) adjList[child] = [];

          // Adiciona o nó filho na lista de adjacência do nó pai
          adjList[parent].push(child);

          // Adiciona o nó pai na lista de adjacência do nó filho
          adjList[child].push(parent);
      });

      // Adiciona o nó pai ao conjunto de todos os nós
      allNodes.add(parent);

      // Adiciona todos os filhos ao conjunto de todos os nós
      children.forEach((child) => allNodes.add(child));
  });

  // Inicializa um conjunto para armazenar os nós visitados durante a busca
  let visited = new Set();

  // Inicializa uma fila com o primeiro nó encontrado no conjunto de todos os nós
  let queue = [Array.from(allNodes)[0]];

  // Realiza a busca em largura (BFS)
  while (queue.length > 0) {
      // Remove o primeiro nó da fila
      let node = queue.shift();

      // Se o nó ainda não foi visitado
      if (!visited.has(node)) {
          // Marca o nó como visitado
          visited.add(node);

          // Adiciona todos os nós adjacentes não visitados à fila
          queue.push(...adjList[node].filter(n => !visited.has(n)));
      }
  }

  // Se o número de nós visitados for diferente do número total de nós, o grafo está desconexo
  return visited.size !== allNodes.size;
};


// Converte os dados do arquivo para um formato adequado para visualização com a biblioteca react-d3-tree.
// Cria um dicionário de nós e organiza suas relações de pai e filho com base nas linhas do arquivo.
// Função que parseia (interpreta) os dados do arquivo e monta uma estrutura de árvore a partir das linhas fornecidas
const parseTreeData = (lines) => {
  // Inicializa um objeto para armazenar os nós da árvore
  let nodes = {};

  // O primeiro valor da primeira linha (antes da vírgula) é o valor da raiz da árvore
  const rootValue = lines[0].split(",")[0].trim();

  // Itera sobre cada linha do arquivo
  lines.forEach((line) => {
      // Separa cada linha em um nó pai e seus filhos (o nó pai é o primeiro valor, os filhos são os demais)
      const [parent, ...children] = line.split(",").map((n) => n.trim());

      // Se o nó pai ainda não existe no objeto de nós, cria-o com um nome e uma lista de filhos vazia
      if (!nodes[parent]) nodes[parent] = { name: parent, children: [] };

      // Itera sobre cada filho do nó pai
      children.forEach((child) => {
          // Se o nó filho ainda não existe no objeto de nós, cria-o com um nome e uma lista de filhos vazia
          if (!nodes[child]) nodes[child] = { name: child, children: [] };

          // Adiciona o nó filho à lista de filhos do nó pai
          nodes[parent].children.push(nodes[child]);
      });
  });

  // Retorna o nó raiz da árvore, ou null se ele não for encontrado
  return nodes[rootValue] || null;
};


  // Função chamada ao clicar no botão de envio. 
  // Lê o arquivo, valida a estrutura, verifica erros e envia os dados para o backend caso tudo esteja correto.
  const handleUpload = async () => {
    if (!file) {
      alert("Por favor, selecione um arquivo antes de enviar.");
      return;
    }

    const reader = new FileReader();
    reader.onload = async () => {
      const fileContent = reader.result.trim();

      if (!fileContent) {
        setError("O arquivo está vazio. Forneça um arquivo com dados.");
        setTreeData(null);  // Limpar a árvore renderizada
        setResult(null);     // Limpar os resultados
        return;
      }

      const lines = fileContent.split("\n");

      const regex = /^[0-9,\s]+$/;
      if (!regex.test(fileContent)) {
        setError("O arquivo contém caracteres inválidos.");
        setTreeData(null);  // Limpar a árvore renderizada
        setResult(null);     // Limpar os resultados
        return;
      }

      if (checkDuplicateNodesInLines(lines)) {
        setError("O arquivo contém nós duplicados, ciclos ou arestas paralelas.");
        setTreeData(null);  // Limpar a árvore renderizada
        setResult(null);     // Limpar os resultados
        return;
      }

      if (checkDisconnection(lines)) {
        setError("O arquivo representa um grafo desconexo.");
        setTreeData(null);  // Limpar a árvore renderizada
        setResult(null);     // Limpar os resultados
        return;
      }

        try {
          const formData = new FormData();
          formData.append("file", file, file.name);
        
          const response = await axios.post("http://127.0.0.1:8000/api/upload/", formData, {
            headers: { "Content-Type": "multipart/form-data" },
          });
        
          const { data } = response;
          setError(null);
          setResult(data);
          
          setTreeData(parseTreeData(lines));
        
        } catch (error) {
          setError("Erro ao processar o arquivo.");
        }
      }        


    reader.readAsText(file);
  };

  //Se a a rovre informada for binaria, renderiza os caminhos na tela
  //e desenha a arvore usando a biblioteca react-d3-tree (independente se é binaria ou não)
  const renderCaminhos = (caminhos) => {
    if (!caminhos || typeof caminhos !== "object") {
      return <p>Dados inválidos ou não encontrados.</p>;
    }

    return (
      <div className="caminhos">
        {["pre_ordem", "em_ordem", "pos_ordem"].map((tipo) => (
          caminhos[tipo] && Array.isArray(caminhos[tipo]) && (
            <div key={tipo}>
              <h4>{tipo.replace("_", " ").toUpperCase()}:</h4>
              <div className="caminho-lista">
                {caminhos[tipo].map((caminho, idx) => (
                  <span key={idx} className="caminho-item">{caminho}</span>
                ))}
              </div>
            </div>
          )
        ))}
      </div>
    );
  };

  return (
    <div className="container">
      <h1>Análise de Árvores</h1>
      <h2>Arquivos .txt com a seguinte estrutura:</h2>
      <h2>Raiz,Nós separados por virgula</h2>
      <h3>5,3,7</h3>
      <h3>3,2,4</h3>
      <h3>7,6,8</h3>


      {error && <div className="error">{error}</div>}

      <input type="file" className="file-input" onChange={handleFileChange} />
      <button className="upload-btn" onClick={handleUpload}>Enviar</button>

      {result && (
        <div className="result-tree-container">
          <div className="resultados">
            <h2>Resultados:</h2>
            <p><strong>Tipo:</strong> {result.tipo_arvore}</p>
            <p><strong>Altura:</strong> {result.altura}</p>

            {renderCaminhos(result.caminhos)}
          </div>

          
          {treeData && <div className="tree-container"><Tree data={treeData} orientation="vertical" /></div>}
        </div>
      )}
    </div>
  );
}

export default App;
