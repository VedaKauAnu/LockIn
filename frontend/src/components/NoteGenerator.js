import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const NoteGenerator = ({ courseId }) => {
  const [topic, setTopic] = useState('');
  const [detailLevel, setDetailLevel] = useState('medium');
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState('');
  
  const navigate = useNavigate();
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!topic.trim()) {
      setError('Please enter a topic');
      return;
    }
    
    setIsGenerating(true);
    setError('');
    
    try {
      const token = localStorage.getItem('token');
      
      const response = await axios.post(
        `/api/course/${courseId}/generate-notes`,
        { topic, detail_level: detailLevel },
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        }
      );
      
      // Navigate to view the new note
      navigate(`/course/${courseId}/note/${response.data.id}`);
      
    } catch (err) {
      console.error('Error generating notes:', err);
      setError(err.response?.data?.error || 'Failed to generate notes. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };
  
  return (
    <div className="card mb-4">
      <div className="card-header bg-primary text-white">
        <h5 className="mb-0">AI Note Generator</h5>
      </div>
      <div className="card-body">
        {error && <div className="alert alert-danger">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="topic" className="form-label">Topic</label>
            <input
              type="text"
              className="form-control"
              id="topic"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="Enter the topic you want notes for"
              required
            />
          </div>
          
          <div className="mb-3">
            <label htmlFor="detailLevel" className="form-label">Detail Level</label>
            <select
              className="form-select"
              id="detailLevel"
              value={detailLevel}
              onChange={(e) => setDetailLevel(e.target.value)}
            >
              <option value="brief">Brief</option>
              <option value="medium">Medium</option>
              <option value="detailed">Detailed</option>
            </select>
          </div>
          
          <button
            type="submit"
            className="btn btn-primary"
            disabled={isGenerating}
          >
            {isGenerating ? (
              <>
                <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                Generating...
              </>
            ) : 'Generate Notes'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default NoteGenerator;