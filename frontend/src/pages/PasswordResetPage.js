import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Body from '../components/Body';
import InputField from '../components/InputField';
import { useApi } from '../contexts/ApiProvider';
import { useFlash } from '../contexts/FlashProvider';

const TRYTON_SERVER = process.env.REACT_APP_TRYTON_SERVER;
const TRYTON_DATABASE = process.env.REACT_APP_TRYTON_DATABASE;

export default function ResetResetPage() {
  const [formErrors, setFormErrors] = useState({});
  const emailField = useRef();
  const api = useApi();
  const flash = useFlash();
  const navigate = useNavigate();

  useEffect(() => {
    emailField.current.focus();
  }, []);

  const onSubmit = async (event) => {
    event.preventDefault();
    const response = await api.post(TRYTON_SERVER, TRYTON_DATABASE, '/web-user-password-reset', {
      email: emailField.current.value,
    });
    if (!response.ok) {
      flash(response.body, 'danger');
    }
    else {
      emailField.current.value = '';
      setFormErrors({});
      flash(response.body.message, 'info');
      navigate('/web-user-login');
    }
  };

  return (
    <Body>
      <h1>Reset Your Password</h1>
      <Form onSubmit={onSubmit}>
        <InputField
          name="email" label="Email Address"
          error={formErrors.email} fieldRef={emailField} />
        <Button variant="primary" type="submit">Reset Password</Button>
      </Form>
    </Body>
  );
}
