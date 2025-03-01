import React, { useState } from 'react';

const QuestionCard = ({ question, showAnswer = false, onShowAnswer, onConfidenceSelect, onNext }) => {
  const [userConfidence, setUserConfidence] = useState(null);

  const handleConfidenceClick = (level) => {
    setUserConfidence(level);
    if (onConfidenceSelect) {
      onConfidenceSelect(level);
    }
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'easy':
        return 'success';
      case 'medium':
        return 'warning';
      case 'hard':
        return 'danger';
      default:
        return 'secondary';
    }
  };

  return (
    <div className="card mb-4">
      <div className="card-body">
        <div className="alert alert-secondary">
          <strong>Difficulty:</strong> 
          <span className={`badge ms-2 bg-${getDifficultyColor(question.difficulty)}`}>
            {question.difficulty}
          </span>
        </div>
        
        <p className="lead">{question.question}</p>
        
        {!showAnswer ? (
          <button 
            className="btn btn-primary"
            onClick={onShowAnswer}
          >
            Show Answer
          </button>
        ) : (
          <div>
            <div className="card mb-3">
              <div className="card-body">
                <h6 className="card-subtitle mb-2 text-muted">Answer:</h6>
                <p>{question.answer}</p>
              </div>
            </div>
            
            <div className="mb-3">
              <p className="mb-2">How well did you know this?</p>
              <div className="btn-group" role="group">
                <button 
                  type="button" 
                  className={`btn ${userConfidence === 1 ? 'btn-danger' : 'btn-outline-danger'}`}
                  onClick={() => handleConfidenceClick(1)}
                >
                  Not at all
                </button>
                <button 
                  type="button" 
                  className={`btn ${userConfidence === 2 ? 'btn-warning' : 'btn-outline-warning'}`}
                  onClick={() => handleConfidenceClick(2)}
                >
                  Somewhat
                </button>
                <button 
                  type="button" 
                  className={`btn ${userConfidence === 3 ? 'btn-success' : 'btn-outline-success'}`}
                  onClick={() => handleConfidenceClick(3)}
                >
                  Very well
                </button>
              </div>
            </div>
            
            <button 
              className="btn btn-primary"
              onClick={onNext}
              disabled={userConfidence === null}
            >
              Next Question
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default QuestionCard;