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

  // Verifica se há nós duplicados dentro de uma mesma linha do arquivo. 
  // Para isso, percorre cada linha do arquivo, separa os valores por vírgula, 
  // remove espaços em branco e usa um conjunto (Set) para detectar duplicações.
  const checkDuplicateNodesInLines = (lines) => {
    for (let line of lines) {
      const nodes = line.split(",").map((node) => node.trim());
      if (nodes.length !== new Set(nodes).size) {
        return true;
      }
    }
    return false;
  };

  // Verifica se o grafo representado no arquivo está desconexo.
  // Constrói uma lista de adjacência para mapear conexões entre nós e usa uma busca em largura (BFS) para verificar a conectividade.
  // Se todos os nós não forem alcançados a partir de um único ponto, o grafo é considerado desconexo.
  const checkDisconnection = (lines) => {
    let adjList = {};
    let allNodes = new Set();

    lines.forEach((line) => {
      const [parent, ...children] = line.split(",").map((n) => n.trim());

      if (!adjList[parent]) adjList[parent] = [];
      children.forEach((child) => {
        if (!adjList[child]) adjList[child] = [];
        adjList[parent].push(child);
        adjList[child].push(parent);
      });

      allNodes.add(parent);
      children.forEach((child) => allNodes.add(child));
    });

    let visited = new Set();
    let queue = [Array.from(allNodes)[0]];

    while (queue.length > 0) {
      let node = queue.shift();
      if (!visited.has(node)) {
        visited.add(node);
        queue.push(...adjList[node].filter(n => !visited.has(n)));
      }
    }

    return visited.size !== allNodes.size;
  };

  // Verifica se a estrutura do arquivo contém ciclos ou arestas duplicadas.
  // Primeiro, percorre as linhas e registra todas as conexões bidirecionais em um conjunto para evitar arestas repetidas.
  // Depois, utiliza uma busca em profundidade (DFS) para detectar ciclos.
  const checkCyclesAndDuplicateEdges = (lines) => {
    let edges = new Set();
    let adjList = {};

    for (let line of lines) {
      const nodes = line.split(",").map((node) => node.trim());

      for (let i = 1; i < nodes.length; i++) {
        const edge = `${nodes[i - 1]}-${nodes[i]}`;
        if (edges.has(edge) || edges.has(`${nodes[i]}-${nodes[i - 1]}`)) {
          return true;
        }
        edges.add(edge);
      }

      const parent = nodes[0];
      const children = nodes.slice(1);
      adjList[parent] = children;
    }

    let visited = new Set();
    let stack = new Set();

    const dfs = (node) => {
      if (stack.has(node)) return true;
      if (visited.has(node)) return false;

      visited.add(node);
      stack.add(node);

      if (adjList[node]) {
        for (let neighbor of adjList[node]) {
          if (dfs(neighbor)) return true;
        }
      }

      stack.delete(node);
      return false;
    };

    for (let node in adjList) {
      if (!visited.has(node) && dfs(node)) {
        return true;
      }
    }

    return false;
  };

  // Converte os dados do arquivo para um formato adequado para visualização com a biblioteca react-d3-tree.
  // Cria um dicionário de nós e organiza suas relações de pai e filho com base nas linhas do arquivo.
  const parseTreeData = (lines) => {
    let nodes = {};
    const rootValue = lines[0].split(",")[0].trim();

    lines.forEach((line) => {
      const [parent, ...children] = line.split(",").map((n) => n.trim());

      if (!nodes[parent]) nodes[parent] = { name: parent, children: [] };

      children.forEach((child) => {
        if (!nodes[child]) nodes[child] = { name: child, children: [] };
        nodes[parent].children.push(nodes[child]);
      });
    });

    return nodes[rootValue] || null;
  };

  // Função chamada ao clicar no botão de envio. 
  // Lê o arquivo, valida a estrutura do grafo, verifica erros e envia os dados para o backend caso tudo esteja correto.
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
        return;
      }

      const lines = fileContent.split("\n");

      const regex = /^[0-9,\s]+$/;
      if (!regex.test(fileContent)) {
        setError("O arquivo contém caracteres inválidos.");
        return;
      }

      if (checkDuplicateNodesInLines(lines)) {
        setError("O arquivo contém nós duplicados.");
        return;
      }

      if (checkDisconnection(lines)) {
        setError("O arquivo representa um grafo disconexo.");
        return;
      }

      if (checkCyclesAndDuplicateEdges(lines)) {
        setError("O arquivo contém ciclos ou arestas paralelas.");
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
      <h1>Analisador de Árvores</h1>
      <h2>Arquivos .txt com a seguinte estrutura:</h2>
      <h3>#Raiz,Nós separados por virgula</h3>


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
