import React, { useState, useEffect } from 'react';
import { Bar, Line, Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import axios from 'axios';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const ProgressTracking = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('overview');
  
  // Sample data - In a real app, this would come from your API
  const [studyData, setStudyData] = useState({
    weeklyStudyHours: {
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      data: [1.5, 2, 0.5, 3, 1, 0, 2.5]
    },
    subjectPerformance: {
      labels: ['Mathematics', 'Computer Science', 'Database Design'],
      data: [75, 82, 65]
    },
    questionConfidence: {
      labels: ['High', 'Medium', 'Low'],
      data: [65, 25, 10]
    }
  });
  
  useEffect(() => {
    // Simulate API call to fetch progress data
    const fetchProgressData = async () => {
      setLoading(true);
      
      try {
        // In a real app, you would fetch data from your API
        // const token = localStorage.getItem('token');
        // const response = await axios.get('/api/progress', {
        //   headers: {
        //     'Authorization': `Bearer ${token}`
        //   }
        // });
        // setStudyData(response.data);
        
        // Simulate API delay
        setTimeout(() => {
          setLoading(false);
        }, 1000);
      } catch (err) {
        console.error('Error fetching progress data:', err);
        setError('Failed to load progress data. Please try again.');
        setLoading(false);
      }
    };
    
    fetchProgressData();
  }, []);
  
  // Configure chart options
  const barOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Weekly Study Hours',
      },
    },
  };
  
  const lineOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Subject Performance (%)',
      },
    },
    scales: {
      y: {
        min: 0,
        max: 100,
      },
    },
  };
  
  const doughnutOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Question Confidence Distribution',
      },
    },
  };
  
  // Prepare chart data
  const weeklyData = {
    labels: studyData.weeklyStudyHours.labels,
    datasets: [
      {
        label: 'Hours',
        data: studyData.weeklyStudyHours.data,
        backgroundColor: 'rgba(53, 162, 235, 0.5)',
      },
    ],
  };
  
  const performanceData = {
    labels: studyData.subjectPerformance.labels,
    datasets: [
      {
        label: 'Performance',
        data: studyData.subjectPerformance.data,
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
        tension: 0.2,
      },
    ],
  };
  
  const confidenceData = {
    labels: studyData.questionConfidence.labels,
    datasets: [
      {
        label: 'Confidence',
        data: studyData.questionConfidence.data,
        backgroundColor: [
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(255, 99, 132, 0.6)',
        ],
        borderColor: [
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(255, 99, 132, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };
  
  // Calculate total study hours
  const totalStudyHours = studyData.weeklyStudyHours.data.reduce((total, hours) => total + hours, 0);
  
  // Calculate average performance
  const avgPerformance = studyData.subjectPerformance.data.reduce((total, score) => total + score, 0) / 
                        studyData.subjectPerformance.data.length;
  
  if (loading) {
    return <div className="text-center my-5"><div className="spinner-border" role="status"></div></div>;
  }
  
  if (error) {
    return <div className="alert alert-danger">{error}</div>;
  }
  
  return (
    <div className="container mt-4">
      <h2 className="mb-4">Your Progress</h2>
      
      <div className="row mb-4">
        <div className="col-md-4">
          <div className="card h-100">
            <div className="card-body text-center">
              <h5 className="card-title">Weekly Study Time</h5>
              <h3 className="display-4">{totalStudyHours.toFixed(1)}</h3>
              <p className="text-muted">hours this week</p>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card h-100">
            <div className="card-body text-center">
              <h5 className="card-title">Average Performance</h5>
              <h3 className="display-4">{avgPerformance.toFixed(1)}%</h3>
              <p className="text-muted">across all subjects</p>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card h-100">
            <div className="card-body text-center">
              <h5 className="card-title">Study Streak</h5>
              <h3 className="display-4">3</h3>
              <p className="text-muted">consecutive days</p>
            </div>
          </div>
        </div>
      </div>
      
      <div className="card">
        <div className="card-header">
          <ul className="nav nav-tabs card-header-tabs">
            <li className="nav-item">
              <button 
                className={`nav-link ${activeTab === 'overview' ? 'active' : ''}`}
                onClick={() => setActiveTab('overview')}
              >
                Overview
              </button>
            </li>
            <li className="nav-item">
              <button 
                className={`nav-link ${activeTab === 'subjects' ? 'active' : ''}`}
                onClick={() => setActiveTab('subjects')}
              >
                Subject Performance
              </button>
            </li>
            <li className="nav-item">
              <button 
                className={`nav-link ${activeTab === 'confidence' ? 'active' : ''}`}
                onClick={() => setActiveTab('confidence')}
              >
                Question Confidence
              </button>
            </li>
          </ul>
        </div>
        <div className="card-body">
          {activeTab === 'overview' && (
            <div>
              <div className="row">
                <div className="col-md-8">
                  <div style={{ height: '300px' }}>
                    <Bar options={barOptions} data={weeklyData} />
                  </div>
                </div>
                <div className="col-md-4">
                  <div className="card">
                    <div className="card-body">
                      <h5 className="card-title">Study Insights</h5>
                      <ul className="list-group list-group-flush">
                        <li className="list-group-item d-flex justify-content-between align-items-center">
                          Most productive day
                          <span className="badge bg-primary">Thursday</span>
                        </li>
                        <li className="list-group-item d-flex justify-content-between align-items-center">
                          Average daily study
                          <span className="badge bg-primary">{(totalStudyHours / 7).toFixed(1)} hrs</span>
                        </li>
                        <li className="list-group-item d-flex justify-content-between align-items-center">
                          Session count
                          <span className="badge bg-primary">12</span>
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="alert alert-info mt-4">
                <h5 className="alert-heading">Weekly Progress Report</h5>
                <p>
                  You've studied for <strong>{totalStudyHours} hours</strong> this week, with Thursday being your most productive day.
                  Your average performance across subjects is <strong>{avgPerformance.toFixed(1)}%</strong>.
                </p>
                <p className="mb-0">
                  Tip: Try to maintain consistent study sessions throughout the week. Consider adding a short study session on Saturday.
                </p>
              </div>
            </div>
          )}
          
          {activeTab === 'subjects' && (
            <div>
              <div style={{ height: '300px' }}>
                <Line options={lineOptions} data={performanceData} />
              </div>
              
              <div className="mt-4">
                <h5>Subject Breakdown</h5>
                <div className="table-responsive">
                  <table className="table table-hover">
                    <thead>
                      <tr>
                        <th>Subject</th>
                        <th>Performance</th>
                        <th>Practice Questions</th>
                        <th>Study Time</th>
                        <th>Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>Mathematics</td>
                        <td>
                          <div className="progress">
                            <div 
                              className="progress-bar bg-success" 
                              role="progressbar" 
                              style={{ width: '75%' }} 
                              aria-valuenow="75" 
                              aria-valuemin="0" 
                              aria-valuemax="100"
                            >
                              75%
                            </div>
                          </div>
                        </td>
                        <td>42 completed</td>
                        <td>3.5 hours</td>
                        <td><span className="badge bg-success">Good</span></td>
                      </tr>
                      <tr>
                        <td>Computer Science</td>
                        <td>
                          <div className="progress">
                            <div 
                              className="progress-bar bg-success" 
                              role="progressbar" 
                              style={{ width: '82%' }} 
                              aria-valuenow="82" 
                              aria-valuemin="0" 
                              aria-valuemax="100"
                            >
                              82%
                            </div>
                          </div>
                        </td>
                        <td>56 completed</td>
                        <td>5.2 hours</td>
                        <td><span className="badge bg-success">Excellent</span></td>
                      </tr>
                      <tr>
                        <td>Database Design</td>
                        <td>
                          <div className="progress">
                            <div 
                              className="progress-bar bg-warning" 
                              role="progressbar" 
                              style={{ width: '65%' }} 
                              aria-valuenow="65" 
                              aria-valuemin="0" 
                              aria-valuemax="100"
                            >
                              65%
                            </div>
                          </div>
                        </td>
                        <td>28 completed</td>
                        <td>2.8 hours</td>
                        <td><span className="badge bg-warning">Needs Work</span></td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}
          
          {activeTab === 'confidence' && (
            <div>
              <div className="row">
                <div className="col-md-6 offset-md-3">
                  <div style={{ height: '300px' }}>
                    <Doughnut options={doughnutOptions} data={confidenceData} />
                  </div>
                </div>
              </div>
              
              <div className="alert alert-success mt-4">
                <h5 className="alert-heading">Confidence Analysis</h5>
                <p>
                  You've answered questions with high confidence {confidenceData.datasets[0].data[0]}% of the time.
                  Focus on improving areas where your confidence is lowest to maximize your test performance.
                </p>
              </div>
              
              <div className="card mt-4">
                <div className="card-header">
                  <h5 className="mb-0">Confidence Improvement Plan</h5>
                </div>
                <div className="card-body">
                  <div className="row">
                    <div className="col-md-4">
                      <div className="card mb-3">
                        <div className="card-body text-center">
                          <h5 className="card-title">Spaced Repetition</h5>
                          <p className="card-text">Focus on low-confidence questions using spaced repetition technique</p>
                          <button className="btn btn-primary">Start Practice</button>
                        </div>
                      </div>
                    </div>
                    <div className="col-md-4">
                      <div className="card mb-3">
                        <div className="card-body text-center">
                          <h5 className="card-title">Topic Review</h5>
                          <p className="card-text">Generate notes for topics with lowest confidence scores</p>
                          <button className="btn btn-primary">Generate Notes</button>
                        </div>
                      </div>
                    </div>
                    <div className="col-md-4">
                      <div className="card mb-3">
                        <div className="card-body text-center">
                          <h5 className="card-title">Test Strategies</h5>
                          <p className="card-text">Learn techniques to boost your test-taking confidence</p>
                          <button className="btn btn-primary">View Strategies</button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProgressTracking;