import React from 'react';

const NoteCard = ({ note, isActive, onClick, onDelete }) => {
  return (
    <div 
      className={`list-group-item list-group-item-action d-flex justify-content-between align-items-center ${isActive ? 'active' : ''}`}
      onClick={onClick}
      style={{ cursor: 'pointer' }}
    >
      <div className="text-truncate">{note.title}</div>
      <button 
        className="btn btn-sm btn-danger"
        onClick={(e) => {
          e.stopPropagation();
          onDelete(note.id);
        }}
      >
        Delete
      </button>
    </div>
  );
};

export default NoteCard;