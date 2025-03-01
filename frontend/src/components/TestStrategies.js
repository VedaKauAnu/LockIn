import React, { useState } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

const TestStrategies = () => {
  const [testType, setTestType] = useState('multiple-choice');
  const [problems, setProblems] = useState([]);
  const [strategies, setStrategies] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Define common test problems for the checkboxes
  const commonProblems = [
    { id: 'time', text: 'Time management' },
    { id: 'anxiety', text: 'Test anxiety' },
    { id: 'focus', text: 'Difficulty focusing' },
    { id: 'memory', text: 'Trouble remembering material' },
    { id: 'preparation', text: 'Lack of preparation' },
    { id: 'confidence', text: 'Low confidence' }
  ];
  
  // Define test types
  const testTypes = [
    { value: 'multiple-choice', label: 'Multiple Choice' },
    { value: 'essay', label: 'Essay' },
    { value: 'short-answer', label: 'Short Answer' },
    { value: 'programming', label: 'Programming/Coding' },
    { value: 'math', label: 'Mathematics' },
    { value: 'open-book', label: 'Open Book' }
  ];
  
  // Handle checkbox changes
  const handleProblemChange = (problemId) => {
    if (problems.includes(problemId)) {
      setProblems(problems.filter(id => id !== problemId));
    } else {
      setProblems([...problems, problemId]);
    }
  };
  
  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    setIsLoading(true);
    setError('');
    
    try {
      const token = localStorage.getItem('token');
      
      // Get the text description of each selected problem
      const problemTexts = problems.map(
        problemId => commonProblems.find(p => p.id === problemId).text
      );
      
      const response = await axios.post(
        '/api/test-strategies',
        { 
          test_type: testType,
          problems: problemTexts
        },
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        }
      );
      
      setStrategies(response.data.strategies);
      
    } catch (err) {
      console.error('Error generating test strategies:', err);
      setError(err.response?.data?.error || 'Failed to generate strategies. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="container mt-4">
      <div className="row">
        <div className="col-md-4">
          <div className="card">
            <div className="card-header bg-success text-white">
              <h5 className="mb-0">Test-Taking Strategies</h5>
            </div>
            <div className="card-body">
              {error && <div className="alert alert-danger">{error}</div>}
              
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label htmlFor="testType" className="form-label">Test Type</label>
                  <select
                    className="form-select"
                    id="testType"
                    value={testType}
                    onChange={(e) => setTestType(e.target.value)}
                  >
                    {testTypes.map(type => (
                      <option key={type.value} value={type.value}>
                        {type.label}
                      </option>
                    ))}
                  </select>
                </div>
                
                <div className="mb-3">
                  <label className="form-label">What challenges do you face?</label>
                  {commonProblems.map(problem => (
                    <div className="form-check" key={problem.id}>
                      <input
                        className="form-check-input"
                        type="checkbox"
                        id={`problem-${problem.id}`}
                        checked={problems.includes(problem.id)}
                        onChange={() => handleProblemChange(problem.id)}
                      />
                      <label className="form-check-label" htmlFor={`problem-${problem.id}`}>
                        {problem.text}
                      </label>
                    </div>
                  ))}
                </div>
                
                <button
                  type="submit"
                  className="btn btn-success"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                      Generating...
                    </>
                  ) : 'Get Strategies'}
                </button>
              </form>
            </div>
          </div>
        </div>
        
        <div className="col-md-8">
          {strategies ? (
            <div className="card">
              <div className="card-header">
                <h5>Your Personalized Test Strategies</h5>
              </div>
              <div className="card-body">
                <ReactMarkdown>{strategies}</ReactMarkdown>
              </div>
              <div className="card-footer">
                <button
                  className="btn btn-outline-primary"
                  onClick={() => window.print()}
                >
                  Print Strategies
                </button>
              </div>
            </div>
          ) : (
            <div className="card">
              <div className="card-body text-center py-5">
                <p className="mb-0 text-muted">
                  Complete the form to get personalized test-taking strategies.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TestStrategies;