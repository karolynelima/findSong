import React, { useState } from 'react';
import './styles.css';

function App() {
  const [cantor, setCantor] = useState('');
  const [frase, setFrase] = useState('');
  const [resultados, setResultados] = useState([]);
  const [carregando, setCarregando] = useState(false);

  const buscarMusicas = async () => {
    setCarregando(true);
    try {
      const response = await fetch('http://localhost:5000/buscar', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ cantor, frase }),
      });
      const data = await response.json();
      setResultados(data);
    } catch (error) {
      console.error('Erro ao buscar músicas:', error);
    } finally {
      setCarregando(false);
    }
  };

  return (
    <div className="App">
      <h1>Buscar Frases em Músicas</h1>
      <div className="formulario">
        <input
          type="text"
          placeholder="Nome do Cantor"
          value={cantor}
          onChange={(e) => setCantor(e.target.value)}
        />
        <input
          type="text"
          placeholder="Frase"
          value={frase}
          onChange={(e) => setFrase(e.target.value)}
        />
        <button onClick={buscarMusicas} disabled={carregando}>
          {carregando ? 'Buscando...' : 'Buscar'}
        </button>
      </div>
      <div className="resultados">
        {resultados.map((resultado, index) => (
          <div key={index} className="resultado">
            <h2>{resultado.musica}</h2>
            <p>{resultado.estrofe}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;