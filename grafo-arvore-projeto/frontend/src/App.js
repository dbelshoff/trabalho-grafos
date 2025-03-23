import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Por favor, selecione um arquivo antes de enviar.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file, file.name); // Adiciona o nome do arquivo corretamente

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/upload/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      console.log("Arquivo enviado com sucesso:", response.data);
      setResult(response.data);
    } catch (error) {
      console.error("Erro ao enviar arquivo:", error.response?.data || error);
      alert(`Erro ao enviar arquivo: ${error.response?.data?.detail || "Erro desconhecido"}`);
    }
  };

  return (
    <div className="container">
      <h1>Analisador de Grafos</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Enviar</button>

      {result && (
        <div>
          <h2>Resultados:</h2>
          <p><strong>É uma árvore?</strong> {result.eh_arvore ? "Sim" : "Não"}</p>
          <p><strong>Tipo de Árvore:</strong> {result.tipo_arvore}</p>
          <p><strong>Altura:</strong> {result.altura}</p>
          <h3>Caminhos Possíveis:</h3>

          {/* Exibindo os caminhos por tipo */}
          <div>
            <h4>Pré-ordem:</h4>
            <ul>
              {result.caminhos?.pre_ordem?.map((caminho, idx) => (
                <li key={idx}>{caminho.join(" -> ")}</li>
              ))}
            </ul>
          </div>
          
          <div>
            <h4>Em ordem:</h4>
            <ul>
              {result.caminhos?.em_ordem?.map((caminho, idx) => (
                <li key={idx}>{caminho.join(" -> ")}</li>
              ))}
            </ul>
          </div>
          
          <div>
            <h4>Pós-ordem:</h4>
            <ul>
              {result.caminhos?.pos_ordem?.map((caminho, idx) => (
                <li key={idx}>{caminho.join(" -> ")}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
