import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { format, addDays } from 'date-fns';
import TodoList from '../components/TodoList';

const Dashboard = () => {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  // Next test date (this would come from your API in a real app)
  const nextTestDate = addDays(new Date(), 3);
  const daysToGo = 3;
  
  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('/api/courses', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        setCourses(response.data);
      } catch (err) {
        console.error('Error fetching courses:', err);
        setError('Failed to load courses. Please try again.');
      } finally {
        setLoading(false);
      }
    };
    
    fetchCourses();
  }, []);
  
  // This space intentionally left empty after removing toggleTodoCompleted function
  
  if (loading) {
    return <div className="text-center my-5"><div className="spinner-border" role="status"></div></div>;
  }
  
  return (
    <div className="container mt-4">
      <h2 className="mb-4">Dashboard</h2>
      
      <div className="row">
        <div className="col-md-8">
          {/* Welcome and quick stats */}
          <div className="card mb-4">
            <div className="card-body">
              <h3>Welcome!</h3>
              <div className="row mt-4">
                <div className="col-md-4">
                  <div className="d-flex align-items-center">
                    <div className="p-3 bg-light rounded me-3">
                      <i className="bi bi-journal-text fs-3"></i>
                    </div>
                    <div>
                      <h6 className="mb-0">Courses</h6>
                      <div className="fs-4">{courses.length}</div>
                    </div>
                  </div>
                </div>
                <div className="col-md-4">
                  <div className="d-flex align-items-center">
                    <div className="p-3 bg-light rounded me-3">
                      <i className="bi bi-lightning fs-3"></i>
                    </div>
                    <div>
                      <h6 className="mb-0">Study Streak</h6>
                      <div className="fs-4">3 days</div>
                    </div>
                  </div>
                </div>
                <div className="col-md-4">
                  <div className="d-flex align-items-center">
                    <div className="p-3 bg-light rounded me-3">
                      <i className="bi bi-clock fs-3"></i>
                    </div>
                    <div>
                      <h6 className="mb-0">This Week</h6>
                      <div className="fs-4">4.5 hrs</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          {/* Todo list */}
          <TodoList />
          
          {/* Suggestions */}
          <div className="card mb-4">
            <div className="card-header">
              <h5 className="mb-0">Suggestions</h5>
            </div>
            <div className="card-body">
              <p className="card-text">Try these out to study better!</p>
              <div className="list-group">
                <Link to="/test-strategies" className="list-group-item list-group-item-action">
                  <div className="d-flex w-100 justify-content-between">
                    <h6 className="mb-1">Review test-taking strategies</h6>
                    <small>5 min</small>
                  </div>
                  <p className="mb-1">Boost your confidence with proven test strategies</p>
                </Link>
                <Link to="/study-mode" className="list-group-item list-group-item-action">
                  <div className="d-flex w-100 justify-content-between">
                    <h6 className="mb-1">Try a focused study session</h6>
                    <small>25 min</small>
                  </div>
                  <p className="mb-1">Use the pomodoro timer to stay focused</p>
                </Link>
              </div>
            </div>
          </div>
        </div>
        
        <div className="col-md-4">
          {/* Next Test Countdown */}
          <div className="card mb-4 border-warning">
            <div className="card-body text-center">
              <h5 className="card-title">Next test</h5>
              <h3 className="display-4 fw-bold">{format(nextTestDate, 'dd')}</h3>
              <h4>{format(nextTestDate, 'MMMM')}</h4>
              <div className="display-6 mt-2">{daysToGo}</div>
              <p className="text-muted">days to go</p>
              <Link to="/test-prep" className="btn btn-warning mt-2">
                Start Test Prep
              </Link>
            </div>
          </div>
          
          {/* Quick Access */}
          <div className="card mb-4">
            <div className="card-header">
              <h5 className="mb-0">Start Study Mode</h5>
            </div>
            <div className="card-body text-center">
              <img 
                src="/images/brain-icon.png" 
                alt="Study Mode" 
                style={{ width: "80px", height: "80px" }}
                className="mb-3"
              />
              <p>Block out distractions and study productively!</p>
              <Link to="/study-mode" className="btn btn-success btn-lg">
                Enter Study Mode
              </Link>
            </div>
          </div>
          
          {/* Recent Courses */}
          <div className="card">
            <div className="card-header d-flex justify-content-between align-items-center">
              <h5 className="mb-0">Your Courses</h5>
              <Link to="/courses" className="btn btn-sm btn-outline-primary">View All</Link>
            </div>
            <div className="card-body">
              {courses.length === 0 ? (
                <p className="text-muted">No courses to display</p>
              ) : (
                <div className="list-group">
                  {courses.slice(0, 3).map(course => (
                    <Link 
                      key={course.id} 
                      to={`/course/${course.id}`}
                      className="list-group-item list-group-item-action"
                    >
                      {course.title}
                    </Link>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;