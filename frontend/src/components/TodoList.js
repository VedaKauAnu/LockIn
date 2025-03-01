import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { format } from 'date-fns';

const TodoList = () => {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [newTodoText, setNewTodoText] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [selectedDate, setSelectedDate] = useState('');

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/api/progress/todos', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setTodos(response.data);
    } catch (err) {
      console.error('Error fetching todos:', err);
      setError('Failed to load todo list. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleAddTodo = async (e) => {
    e.preventDefault();
    
    if (!newTodoText.trim()) {
      return;
    }
    
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        '/api/progress/todos',
        { 
          text: newTodoText,
          due_date: selectedDate || null
        },
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        }
      );
      
      // Add new todo to state
      setTodos([response.data, ...todos]);
      
      // Reset form
      setNewTodoText('');
      setSelectedDate('');
      setShowForm(false);
      
    } catch (err) {
      console.error('Error adding todo:', err);
      setError('Failed to add todo. Please try again.');
    }
  };

  const handleToggleTodo = async (id, completed) => {
    try {
      const token = localStorage.getItem('token');
      await axios.put(
        `/api/progress/todos/${id}`,
        { completed: !completed },
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        }
      );
      
      // Update todo in state
      setTodos(todos.map(todo => 
        todo.id === id ? { ...todo, completed: !todo.completed } : todo
      ));
      
    } catch (err) {
      console.error('Error updating todo:', err);
      setError('Failed to update todo. Please try again.');
    }
  };

  const handleDeleteTodo = async (id) => {
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`/api/progress/todos/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      // Remove todo from state
      setTodos(todos.filter(todo => todo.id !== id));
      
    } catch (err) {
      console.error('Error deleting todo:', err);
      setError('Failed to delete todo. Please try again.');
    }
  };

  if (loading && todos.length === 0) {
    return <div className="text-center my-3"><div className="spinner-border spinner-border-sm" role="status"></div></div>;
  }

  return (
    <div className="card mb-4">
      <div className="card-header d-flex justify-content-between align-items-center">
        <h5 className="mb-0">To-Do List</h5>
        <button 
          className="btn btn-sm btn-outline-primary"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? 'Cancel' : 'Add Task'}
        </button>
      </div>
      
      <div className="card-body">
        {error && <div className="alert alert-danger">{error}</div>}
        
        {showForm && (
          <form onSubmit={handleAddTodo} className="mb-3">
            <div className="mb-2">
              <input
                type="text"
                className="form-control"
                placeholder="Enter task..."
                value={newTodoText}
                onChange={(e) => setNewTodoText(e.target.value)}
                required
              />
            </div>
            <div className="mb-2">
              <input
                type="date"
                className="form-control"
                value={selectedDate}
                onChange={(e) => setSelectedDate(e.target.value)}
              />
              <small className="text-muted">Optional due date</small>
            </div>
            <button type="submit" className="btn btn-primary">Add Task</button>
          </form>
        )}
        
        {todos.length === 0 ? (
          <p className="text-muted">No tasks to display</p>
        ) : (
          <ul className="list-group">
            {todos.map(todo => (
              <li 
                key={todo.id} 
                className="list-group-item d-flex justify-content-between align-items-center"
              >
                <div className="d-flex align-items-center">
                  <div className="form-check">
                    <input
                      className="form-check-input"
                      type="checkbox"
                      checked={todo.completed}
                      onChange={() => handleToggleTodo(todo.id, todo.completed)}
                      id={`todo-${todo.id}`}
                    />
                    <label 
                      className={`form-check-label ${todo.completed ? 'text-decoration-line-through text-muted' : ''}`} 
                      htmlFor={`todo-${todo.id}`}
                    >
                      {todo.text}
                    </label>
                  </div>
                  
                  {todo.due_date && (
                    <span className="badge bg-secondary ms-2">
                      Due: {format(new Date(todo.due_date), 'MMM d')}
                    </span>
                  )}
                </div>
                
                <button 
                  className="btn btn-sm btn-outline-danger"
                  onClick={() => handleDeleteTodo(todo.id)}
                >
                  <i className="bi bi-trash"></i>
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default TodoList;