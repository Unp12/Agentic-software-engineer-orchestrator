import { useState } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [pmPlan, setPmPlan] = useState('');
  const [generatedCode, setGeneratedCode] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const runAgenticSquad = async () => {
    if (!prompt.trim()) return;
    
    // Reset state before new run
    setIsLoading(true);
    setError('');
    setPmPlan('');
    setGeneratedCode('');

    try {
      // Talk to the FastAPI Python Server
      const response = await axios.post('http://127.0.0.1:8000/api/generate', {
        prompt: prompt
      });
      
      setPmPlan(response.data.pm_plan);
      setGeneratedCode(response.data.generated_code);
    } catch (err) {
      console.error(err);
      setError('Connection failed. Make sure your Python FastAPI server is running in another terminal!');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="dashboard-container">
      <header className="header">
        <h1>Agentic Software Engineering Orchestrator</h1>
        <p>Enterprise A2A Development Framework</p>
      </header>

      <main className="main-content">
        {/* User Input Section */}
        <div className="input-section">
          <textarea 
            placeholder="Describe the software feature you want the AI squad to build..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            rows={4}
          />
          <button 
            onClick={runAgenticSquad} 
            disabled={isLoading || !prompt}
            className={isLoading ? 'loading-btn' : ''}
          >
            {isLoading ? '⚙️ Agents are thinking...' : '🚀 Deploy AI Squad'}
          </button>
          
          {error && <div className="error-banner">{error}</div>}
        </div>

        {/* Results Section */}
        <div className="results-grid">
          {/* PM Plan Column */}
          <div className="result-card">
            <h2>🧠 Product Manager Specs</h2>
            <div className="markdown-body">
              {pmPlan ? (
                <ReactMarkdown>{pmPlan}</ReactMarkdown>
              ) : (
                <p className="empty-state">Awaiting system instructions...</p>
              )}
            </div>
          </div>

          {/* Coder Output Column */}
          <div className="result-card">
            <h2>💻 Senior Coder Output</h2>
            <div className="markdown-body">
              {generatedCode ? (
                <ReactMarkdown>{generatedCode}</ReactMarkdown>
              ) : (
                <p className="empty-state">Awaiting PM architecture plan...</p>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;