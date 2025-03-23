import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null); // Para armazenar o erro

  // Função para lidar com a mudança de arquivo
  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    
    // Validar o formato do arquivo
    if (selectedFile && selectedFile.type !== "text/plain") {
      setError("Formato de arquivo inválido. Por favor, envie um arquivo .txt.");
      setFile(null);
      return;
    }

    setError(null);
    setFile(selectedFile);
  };

 

  // Função para verificar ciclos e arestas duplas
  const checkCyclesAndDuplicateEdges = (lines) => {
    let edges = new Set();

    for (let line of lines) {
      const nodes = line.split(",").map((node) => node.trim());
      for (let i = 1; i < nodes.length; i++) {
        const edge = `${nodes[i - 1]}-${nodes[i]}`;
        if (edges.has(edge) || edges.has(`${nodes[i]}-${nodes[i - 1]}`)) {
          return true; // Aresta duplicada
        }
        edges.add(edge);
      }
    }

    let visited = new Set();
    let stack = new Set();

    // Função de DFS para detectar ciclos
    const dfs = (node, adjList) => {
      if (stack.has(node)) return true; // Se já estiver no stack, temos um ciclo
      if (visited.has(node)) return false;

      visited.add(node);
      stack.add(node);

      if (adjList[node]) {
        for (let neighbor of adjList[node]) {
          if (dfs(neighbor, adjList)) return true;
        }
      }

      stack.delete(node);
      return false;
    };

    let adjList = {};
    for (let line of lines) {
      const nodes = line.split(",").map((node) => node.trim());
      const parent = nodes[0];
      const children = nodes.slice(1);
      adjList[parent] = children;
    }

    for (let node in adjList) {
      if (dfs(node, adjList)) {
        return true; // Ciclo encontrado
      }
    }

    return false;
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Por favor, selecione um arquivo antes de enviar.");
      return;
    }
  
    const formData = new FormData();
    formData.append("file", file, file.name);
  
    // Usando FileReader para ler o conteúdo do arquivo
    const reader = new FileReader();
    reader.onload = async () => {
      const fileContent = reader.result;
  
      // Verificar se o arquivo está vazio
      if (!fileContent || fileContent.trim() === "") {
        setError("O arquivo está vazio. Por favor, forneça um arquivo com dados.");
        return;
      }
  
      const lines = fileContent.split("\n");
  
      try {
        const response = await axios.post("http://127.0.0.1:8000/api/upload/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
  
        // Verificar se o arquivo contém erros
        const { data } = response;
        const { caminhos, eh_arvore } = data;
  
        // Verificar ciclos e arestas duplas
        if (checkCyclesAndDuplicateEdges(lines)) {
          setError("O arquivo informado não é uma arvore, pois contém ciclos ou arestas duplicadas.");
          return;
        }
  
        setError(null); // Limpar o erro
        setResult(data); // Armazenar o resultado da resposta
      } catch (error) {
        //console.error("Erro ao enviar arquivo:", error.response?.data || error);
        //alert(`Erro ao enviar arquivo: ${error.response?.data?.detail || "Erro desconhecido"}`);
        setError("Formato de arquivo invalido");
      }
    };
  
    reader.onerror = () => {
      alert("Erro ao ler o arquivo.");
    };
  
    reader.readAsText(file);
  };
  
  // Função para renderizar os caminhos em uma linha
const renderCaminhos = (caminhos) => {
  if (!caminhos || typeof caminhos !== "object") {
    return <p>Dados inválidos ou não encontrados.</p>;
  }

  return (
    <div>
      {caminhos.pre_ordem && Array.isArray(caminhos.pre_ordem) && (
        <div>
          <h4>Pré-ordem:</h4>
          <div style={{ display: "flex", flexWrap: "wrap" }}>
            {caminhos.pre_ordem.map((caminho, idx) => (
              <span key={idx} style={{ marginRight: "10px" }}>
                {caminho}
              </span>
            ))}
          </div>
        </div>
      )}

      {caminhos.em_ordem && Array.isArray(caminhos.em_ordem) && (
        <div>
          <h4>Em ordem:</h4>
          <div style={{ display: "flex", flexWrap: "wrap" }}>
            {caminhos.em_ordem.map((caminho, idx) => (
              <span key={idx} style={{ marginRight: "10px" }}>
                {caminho}
              </span>
            ))}
          </div>
        </div>
      )}

      {caminhos.pos_ordem && Array.isArray(caminhos.pos_ordem) && (
        <div>
          <h4>Pós-ordem:</h4>
          <div style={{ display: "flex", flexWrap: "wrap" }}>
            {caminhos.pos_ordem.map((caminho, idx) => (
              <span key={idx} style={{ marginRight: "10px" }}>
                {caminho}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

// Dentro do JSX de renderização
return (
  <div className="container">
    <h1>Analisador de Grafos</h1>
    
    {/* Mensagem de erro, se houver */}
    {error && <div style={{ color: "red" }}>{error}</div>}

    {/* Campo para selecionar o arquivo */}
    <input type="file" onChange={handleFileChange} />
    
    {/* Botão para enviar o arquivo */}
    <button onClick={handleUpload}>Enviar</button>

    {/* Se houver resultados, exibe-os */}
    {result && (
      <div>
        <h2>Resultados:</h2>
        <p><strong>É uma árvore?</strong> {result.eh_arvore ? "Sim" : "Não"}</p>
        <p><strong>Tipo de Árvore:</strong> {result.tipo_arvore}</p>
        <p><strong>Altura:</strong> {result.altura}</p>

        {/* Só renderiza os caminhos se for uma árvore binária */}
        {result.eh_arvore && renderCaminhos(result.caminhos)}
      </div>
    )}
  </div>
);

}

export default App;
