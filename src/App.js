import React, { useState } from 'react';
import './styles.css';

function App() {
  const [frase, setFrase] = useState('');
  const [resultados, setResultados] = useState([]);
  const [carregando, setCarregando] = useState(false);

  const buscarMusicas = async () => {
    setCarregando(true);
    try {
      const response = await fetch('http://localhost:8000/buscar', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ frase }),
      });
      const data = await response.json();
      setResultados(data);
    } catch (error) {
      console.error('Erro ao buscar músicas:', error);
    } finally {
      setCarregando(false);
    }
  };

  // Função para destacar a palavra/frase na estrofe
  const destacarFrase = (estrofe, frase) => {
    if (!frase) return estrofe;

    const regex = new RegExp(`(${frase})`, 'gi');
    return estrofe.replace(regex, `<span class="destaque">$1</span>`);
  };

  return (
    <div className="App">
      <h1>Ariana Grande's Musics Finder</h1>
      <div className="formulario">
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
            <h2>{resultado.musica} ({resultado.album})</h2>
            <p dangerouslySetInnerHTML={{ __html: destacarFrase(resultado.estrofe, frase) }} />
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
