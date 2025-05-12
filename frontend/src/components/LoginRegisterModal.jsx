import { useRef, useEffect, useState } from 'react';

export default function LoginRegisterModal({ show, onClose, isLoggedIn, setIsLoggedIn, verifiedUsername, setVerifiedUsername}) {
  const modalRef = useRef();
  const [isRegistering, setIsRegistering] = useState(false);
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    function handleClickOutside(event) {
      if (modalRef.current && !modalRef.current.contains(event.target)) {
        onClose();
      }
    }
    if (show) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [show, onClose]);

  useEffect(() => {
    if (errorMessage || successMessage) {
      const timer = setTimeout(() => {
        setErrorMessage('');
        setSuccessMessage('');
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [errorMessage, successMessage]);

  if (!show) return null;

  async function handleSubmit(e) {
    e.preventDefault();
    setErrorMessage('');
    setSuccessMessage('');
    setIsSubmitting(true);

    let endpoint;
    let payload;

    
    endpoint = isRegistering ? '/register' : '/login';
    payload = isRegistering
      ? { password, username }
      : { username, password };
    

    try {
      const serverBaseURLString = "http://localhost:8080";
      const serverBaseURL = new URL(serverBaseURLString); 
      const fullPath = new URL(endpoint, serverBaseURL);
      const response = await fetch(fullPath, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(payload),
      });
      const text = await response.text();
      if(endpoint == '/login' && response.ok && text.length > 0) {
        setIsLoggedIn(true);
        setVerifiedUsername(text);
      }
      
      let data = null;
      try {
        data = text ? JSON.parse(text) : {};
      } catch (err) {
        data = {}; // if parsing fails, treat as empty object
      }

      if (!response.ok) {
        if(response.status == 409) throw new Error(data.message || 'That username has been taken.');
        throw new Error(data.message || 'Invalid username or password.');
      }

    } catch (error) {
      console.error('Error:', error);
      setErrorMessage(error.message || 'Something went wrong.');
    } finally {
      setIsSubmitting(false);
    }
  }

  function attemptLogOut() {
    const serverBaseURLString = "http://localhost:8080";
    const serverBaseURL = new URL(serverBaseURLString); 
    const logOutEndpoint = new URL("/logout", serverBaseURL);

    fetch(logOutEndpoint, {
      method: 'POST',
      credentials: 'include'
    })
    .then(response => {if(response.ok) {setIsLoggedIn(false); setVerifiedUsername("");}})
  }

  function resetForm() {
    setPassword('');
    setUsername('');
    setErrorMessage('');
    setSuccessMessage('');
    setIsRegistering(false);
    setIsSubmitting(false);
  }

  return (
    <div className="modal-overlay">
      <div className="modal-content" ref={modalRef}>
        <button
          className="close-button"
          onClick={() => {
            resetForm();
            onClose();
          }}
        >
          ✖
        </button>
        <h2>
          {isLoggedIn ? 
            <>{'Logged in as: '} <span style={{color: "maroon"}}>{verifiedUsername}</span></>
            : isRegistering
            ? 'Register'
            : 'Login'
          }
        </h2>
        
        
        {!isLoggedIn && <form className="modal-form" onSubmit={handleSubmit}>      
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />

        
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button type="submit" disabled={isSubmitting}>
            {isSubmitting
              ? 'Submitting...'
              :  isRegistering
              ? 'Create Account'
              : 'Login'}
          </button>
        </form>}

        {errorMessage && <p className="error-message">{errorMessage}</p>}
        {successMessage && <p className="success-message">{successMessage}</p>}

        <p>
          {!isLoggedIn && (
            <>
              {isRegistering
                ? 'Already have an account?'
                : "Don't have an account?"}{' '}
              <button
                className="switch-button"
                onClick={() => setIsRegistering(!isRegistering)}
              >
                {isRegistering ? 'Login' : 'Register'}
              </button>
            </>
          )}
        </p>

        {isLoggedIn && (
          <p>
            <button
              className="log-out-button"
              onClick={() => attemptLogOut()}
            >
              Log Out
            </button>
          </p>
        )}
      </div>
    </div>
  );
}
