import React from 'react';
import { Link } from 'react-router-dom';

const CourseCard = ({ course, onDelete }) => {
  return (
    <div className="card study-card h-100">
      <div className="card-body">
        <h5 className="card-title">{course.title}</h5>
        <p className="card-text">{course.description}</p>
      </div>
      <div className="card-footer bg-transparent border-top-0">
        <div className="d-flex justify-content-between">
          <Link 
            to={`/course/${course.id}`} 
            className="btn btn-primary btn-sm"
          >
            View Course
          </Link>
          <button
            className="btn btn-danger btn-sm"
            onClick={() => onDelete(course.id)}
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
};

export default CourseCard;