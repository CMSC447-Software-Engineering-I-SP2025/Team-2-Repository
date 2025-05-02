import { useRef, useEffect, useState } from 'react';

export default function LoginRegisterModal({ show, onClose }) {
  const modalRef = useRef();
  const emailInputRef = useRef();
  const [isRegistering, setIsRegistering] = useState(false);
  const [isForgotPassword, setIsForgotPassword] = useState(false);
  const [email, setEmail] = useState('');
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
    if (show && emailInputRef.current) {
      emailInputRef.current.focus();
    }
  }, [show]);

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

    if (isForgotPassword) {
      endpoint = '/forgot-password';
      payload = { email };
    } else {
      endpoint = isRegistering ? '/register' : '/login';
      payload = isRegistering
        ? { email, password, username }
        : { email, password };
    }

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(payload),
      });

      let data = null;
      const text = await response.text();

      try {
        data = text ? JSON.parse(text) : {};
      } catch (err) {
        data = {}; // if parsing fails, treat as empty object
      }

      if (!response.ok) {
        throw new Error(data.message || 'Invalid email or password.');
      }

      if (isForgotPassword) {
        setSuccessMessage('If an account with that email exists, a reset link was sent.');
        setIsForgotPassword(false);
      } else {
        onClose();
      }
    } catch (error) {
      console.error('Error:', error);
      setErrorMessage(error.message || 'Something went wrong.');
    } finally {
      setIsSubmitting(false);
    }
  }

  function resetForm() {
    setEmail('');
    setPassword('');
    setUsername('');
    setErrorMessage('');
    setSuccessMessage('');
    setIsForgotPassword(false);
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
          {isForgotPassword
            ? 'Reset Password'
            : isRegistering
            ? 'Register'
            : 'Login'}
        </h2>

        <form className="modal-form" onSubmit={handleSubmit}>
          {isRegistering && (
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          )}

          <input
            type="email"
            placeholder="Email"
            ref={emailInputRef}
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          {!isForgotPassword && (
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          )}

          <button type="submit" disabled={isSubmitting}>
            {isSubmitting
              ? 'Submitting...'
              : isForgotPassword
              ? 'Send Reset Link'
              : isRegistering
              ? 'Create Account'
              : 'Login'}
          </button>
        </form>

        {errorMessage && <p className="error-message">{errorMessage}</p>}
        {successMessage && <p className="success-message">{successMessage}</p>}

        <p>
          {!isForgotPassword && (
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

        {!isRegistering && !isForgotPassword && (
          <p>
            <button
              className="forgot-password-button"
              onClick={() => setIsForgotPassword(true)}
            >
              Forgot your password?
            </button>
          </p>
        )}

        {isForgotPassword && (
          <p>
            Remembered your password?{' '}
            <button
              className="switch-button"
              onClick={() => setIsForgotPassword(false)}
            >
              Back to Login
            </button>
          </p>
        )}
      </div>
    </div>
  );
}
