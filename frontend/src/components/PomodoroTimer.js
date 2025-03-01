import React, { useState, useEffect, useRef } from 'react';

const PomodoroTimer = () => {
  // Timer states
  const [minutes, setMinutes] = useState(25);
  const [seconds, setSeconds] = useState(0);
  const [isActive, setIsActive] = useState(false);
  const [mode, setMode] = useState('focus'); // 'focus' or 'break'
  const [sessions, setSessions] = useState(0);
  
  // Settings
  const [focusTime, setFocusTime] = useState(25);
  const [breakTime, setBreakTime] = useState(5);
  const [longBreakTime, setLongBreakTime] = useState(15);
  const [enableNotifications, setEnableNotifications] = useState(false);
  
  // Refs
  const timerRef = useRef(null);
  const audioRef = useRef(null);
  
  // Effect to handle timer countdown
  useEffect(() => {
    if (isActive) {
      timerRef.current = setInterval(() => {
        if (seconds > 0) {
          setSeconds(seconds - 1);
        } else if (minutes > 0) {
          setMinutes(minutes - 1);
          setSeconds(59);
        } else {
          // Timer completed
          handleTimerComplete();
        }
      }, 1000);
    } else {
      clearInterval(timerRef.current);
    }
    
    return () => clearInterval(timerRef.current);
  }, [isActive, minutes, seconds]);
  
  // Handle timer completion
  const handleTimerComplete = () => {
    // Play sound notification
    if (audioRef.current) {
      audioRef.current.play();
    }
    
    // Show browser notification if enabled
    if (enableNotifications) {
      if ('Notification' in window) {
        if (Notification.permission === 'granted') {
          new Notification(
            mode === 'focus' ? 'Break Time!' : 'Focus Time!', 
            { 
              body: mode === 'focus' 
                ? 'Great job! Take a break.' 
                : 'Break is over. Time to focus!'
            }
          );
        } else if (Notification.permission !== 'denied') {
          Notification.requestPermission();
        }
      }
    }
    
    // Switch modes
    if (mode === 'focus') {
      const newSessions = sessions + 1;
      setSessions(newSessions);
      
      // After 4 focus sessions, take a long break
      if (newSessions % 4 === 0) {
        setMode('longBreak');
        setMinutes(longBreakTime);
      } else {
        setMode('break');
        setMinutes(breakTime);
      }
    } else {
      setMode('focus');
      setMinutes(focusTime);
    }
    
    setSeconds(0);
    setIsActive(false);
  };
  
  // Start the timer
  const startTimer = () => {
    setIsActive(true);
  };
  
  // Pause the timer
  const pauseTimer = () => {
    setIsActive(false);
  };
  
  // Reset the timer
  const resetTimer = () => {
    setIsActive(false);
    if (mode === 'focus') {
      setMinutes(focusTime);
    } else if (mode === 'break') {
      setMinutes(breakTime);
    } else {
      setMinutes(longBreakTime);
    }
    setSeconds(0);
  };
  
  // Skip to the next timer
  const skipTimer = () => {
    handleTimerComplete();
  };
  
  // Format time as MM:SS
  const formatTime = () => {
    const formattedMinutes = minutes < 10 ? `0${minutes}` : minutes;
    const formattedSeconds = seconds < 10 ? `0${seconds}` : seconds;
    return `${formattedMinutes}:${formattedSeconds}`;
  };
  
  // Request notification permission
  const requestNotificationPermission = () => {
    if ('Notification' in window) {
      Notification.requestPermission().then(permission => {
        if (permission === 'granted') {
          setEnableNotifications(true);
        }
      });
    }
  };
  
  return (
    <div className="card">
      <div className="card-header bg-warning text-dark">
        <h5 className="mb-0">Pomodoro Study Timer</h5>
      </div>
      <div className="card-body text-center">
        <div className="display-1 mb-4">{formatTime()}</div>
        
        <div className="d-flex justify-content-center gap-2 mb-4">
          {!isActive ? (
            <button className="btn btn-lg btn-success" onClick={startTimer}>
              Start
            </button>
          ) : (
            <button className="btn btn-lg btn-secondary" onClick={pauseTimer}>
              Pause
            </button>
          )}
          <button className="btn btn-lg btn-danger" onClick={resetTimer}>
            Reset
          </button>
          <button className="btn btn-lg btn-warning" onClick={skipTimer}>
            Skip
          </button>
        </div>
        
        <div className="mb-4">
          <h6>Current Mode: {mode === 'focus' ? 'Focus Time' : mode === 'break' ? 'Break Time' : 'Long Break'}</h6>
          {mode === 'focus' && <div className="text-muted">Stay focused and work on your task</div>}
          {mode === 'break' && <div className="text-muted">Take a short break, stretch, hydrate</div>}
          {mode === 'longBreak' && <div className="text-muted">Great job! Take a longer break</div>}
        </div>
        
        <div className="mt-4">
          <div className="form-check form-switch d-flex justify-content-center align-items-center gap-2">
            <input 
              className="form-check-input" 
              type="checkbox" 
              id="notification-toggle"
              checked={enableNotifications}
              onChange={() => {
                if (!enableNotifications) {
                  requestNotificationPermission();
                } else {
                  setEnableNotifications(false);
                }
              }}
            />
            <label className="form-check-label" htmlFor="notification-toggle">
              Enable notifications
            </label>
          </div>
        </div>
        
        {/* Hidden audio element for notification sound */}
        <audio ref={audioRef} src="/notification-sound.mp3" />
      </div>
      <div className="card-footer">
        <div className="d-flex justify-content-between">
          <div>Sessions: {sessions}/4</div>
          <div>Focus: {focusTime}min | Break: {breakTime}min</div>
        </div>
      </div>
    </div>
  );
};

export default PomodoroTimer;