import React, { useState } from 'react';
import axios from 'axios';

const QuestionGenerator = ({ courseId, onQuestionsGenerated }) => {
  const [topic, setTopic] = useState('');
  const [count, setCount] = useState(5);
  const [difficulty, setDifficulty] = useState('mixed');
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState('');
  
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
        `/api/course/${courseId}/generate-questions`,
        { topic, count, difficulty },
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        }
      );
      
      // Call the callback function with the generated questions
      if (onQuestionsGenerated) {
        onQuestionsGenerated(response.data.questions);
      }
      
    } catch (err) {
      console.error('Error generating questions:', err);
      setError(err.response?.data?.error || 'Failed to generate questions. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };
  
  return (
    <div className="card mb-4">
      <div className="card-header bg-info text-white">
        <h5 className="mb-0">AI Question Generator</h5>
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
              placeholder="Enter the topic for practice questions"
              required
            />
          </div>
          
          <div className="mb-3">
            <label htmlFor="count" className="form-label">Number of Questions</label>
            <input
              type="number"
              className="form-control"
              id="count"
              value={count}
              onChange={(e) => setCount(Math.min(20, Math.max(1, parseInt(e.target.value) || 1)))}
              min="1"
              max="20"
            />
            <div className="form-text">Maximum 20 questions per request</div>
          </div>
          
          <div className="mb-3">
            <label htmlFor="difficulty" className="form-label">Difficulty</label>
            <select
              className="form-select"
              id="difficulty"
              value={difficulty}
              onChange={(e) => setDifficulty(e.target.value)}
            >
              <option value="mixed">Mixed</option>
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
          </div>
          
          <button
            type="submit"
            className="btn btn-info"
            disabled={isGenerating}
          >
            {isGenerating ? (
              <>
                <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                Generating...
              </>
            ) : 'Generate Questions'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default QuestionGenerator;