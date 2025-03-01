import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import NoteGenerator from '../components/NoteGenerator';
import QuestionGenerator from '../components/QuestionGenerator';
import QuestionCard from '../components/QuestionCard';
import PomodoroTimer from '../components/PomodoroTimer';
import { Tab, Tabs, Alert } from 'react-bootstrap';

const StudyPage = () => {
  const { courseId } = useParams();
  const navigate = useNavigate();
  
  const [course, setCourse] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('notes');
  const [generatedQuestions, setGeneratedQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [showAnswer, setShowAnswer] = useState(false);
  const [confidenceScores, setConfidenceScores] = useState({});

  useEffect(() => {
    // Fetch course data
    const fetchCourse = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`/api/courses/${courseId}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        setCourse(response.data);
      } catch (err) {
        console.error('Error fetching course:', err);
        setError('Failed to load course. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchCourse();
  }, [courseId]);

  const handleQuestionsGenerated = (questions) => {
    setGeneratedQuestions(questions);
    setCurrentQuestionIndex(0);
    setShowAnswer(false);
    setConfidenceScores({});
  };

  const handleShowAnswer = () => {
    setShowAnswer(true);
  };

  const handleConfidenceSelect = (level) => {
    setConfidenceScores({
      ...confidenceScores,
      [currentQuestionIndex]: level
    });
  };

  const handleNextQuestion = () => {
    if (currentQuestionIndex < generatedQuestions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
      setShowAnswer(false);
    } else {
      // End of questions
      // Here you could save progress or show a summary
      alert('You have completed all questions!');
    }
  };

  const calculateProgress = () => {
    if (generatedQuestions.length === 0) return 0;
    return (Object.keys(confidenceScores).length / generatedQuestions.length) * 100;
  };

  if (loading) {
    return <div className="text-center my-5"><div className="spinner-border" role="status"></div></div>;
  }

  if (error) {
    return <Alert variant="danger">{error}</Alert>;
  }

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>{course?.title} - Study Session</h2>
        <button 
          className="btn btn-outline-secondary"
          onClick={() => navigate(`/course/${courseId}`)}
        >
          Back to Course
        </button>
      </div>

      <Tabs
        activeKey={activeTab}
        onSelect={(k) => setActiveTab(k)}
        className="mb-4"
      >
        <Tab eventKey="notes" title="Generate Notes">
          <div className="row">
            <div className="col-md-6">
              <NoteGenerator courseId={courseId} />
<<<<<<< Tabnine <<<<<<<
          </div>
>>>>>>> Tabnine >>>>>>>// {"conversationId":"c49eacb7-ef09-435f-beb5-f67fa37f65f2","source":"instruct"}
            <div className="col-md-6">
              <div className="card">
                <div className="card-header">
                  <h5>Why Use AI-Generated Notes?</h5>
                </div>
                <div className="card-body">
                  <ul className="list-group list-group-flush">
                    <li className="list-group-item">✅ Get organized notes on any topic instantly</li>
                    <li className="list-group-item">✅ Fill gaps in your understanding</li>
                    <li className="list-group-item">✅ Different perspective on complex concepts</li>
                    <li className="list-group-item">✅ Create study guides for any topic</li>
                    <li className="list-group-item">✅ Save time on note-taking</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </Tab>
        
        <Tab eventKey="practice" title="Practice Questions">
          <div className="row">
            <div className="col-md-4">
              <QuestionGenerator 
                courseId={courseId} 
                onQuestionsGenerated={handleQuestionsGenerated} 
              />
              
              {generatedQuestions.length > 0 && (
                <div className="card mt-3">
                  <div className="card-header">
                    <h5>Progress</h5>
                  </div>
                  <div className="card-body">
                    <div className="progress mb-3">
                      <div 
                        className="progress-bar bg-success" 
                        role="progressbar" 
                        style={{ width: `${calculateProgress()}%` }} 
                        aria-valuenow={calculateProgress()} 
                        aria-valuemin="0" 
                        aria-valuemax="100"
                      >
                        {Math.round(calculateProgress())}%
                      </div>
                    </div>
                    <p>Question {currentQuestionIndex + 1} of {generatedQuestions.length}</p>
                  </div>
                </div>
              )}
            </div>
            
            <div className="col-md-8">
              {generatedQuestions.length > 0 ? (
                <QuestionCard 
                  question={generatedQuestions[currentQuestionIndex]}
                  showAnswer={showAnswer}
                  onShowAnswer={handleShowAnswer}
                  onConfidenceSelect={handleConfidenceSelect}
                  onNext={handleNextQuestion}
                />
              ) : (
                <div className="card">
                  <div className="card-body text-center py-5">
                    <p className="mb-3">Generate practice questions to start studying!</p>
                    <div className="text-muted">
                      <small>Questions will appear here after generation</small>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </Tab>
        
        <Tab eventKey="strategies" title="Test Strategies">
          <iframe 
            src="/test-strategies" 
            style={{ 
              width: '100%', 
              height: '650px', 
              border: 'none', 
              borderRadius: '0.25rem',
              boxShadow: '0 0.125rem 0.25rem rgba(0, 0, 0, 0.075)'
            }}
            title="Test Strategies"
          />
        </Tab>
        
        Enable notifications
                      </label>
                    </div>
                  </div>
                </div>
                <div className="card-footer">
                  <div className="d-flex justify-content-between">
                    <div>Sessions: 0/4</div>
                    <div>Focus: 25min | Break: 5min</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </Tab>
      </Tabs>
    </div>
  );
};

export default StudyPage;