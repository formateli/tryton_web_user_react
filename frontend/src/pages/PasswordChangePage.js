import { useState, useEffect, useRef } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import { useNavigate } from 'react-router-dom';
import Body from '../components/Body';
import InputField from '../components/InputField';
import { useApi } from '../contexts/ApiProvider';
import { useFlash } from '../contexts/FlashProvider';
import { useUser } from '../contexts/UserProvider';

const TRYTON_SERVER = process.env.REACT_APP_TRYTON_SERVER;
const TRYTON_DATABASE = process.env.REACT_APP_TRYTON_DATABASE;

export default function PasswordChangePage() {
  const [formErrors, setFormErrors] = useState({});
  const oldPasswordField = useRef();
  const passwordField = useRef();
  const password2Field = useRef();
  const navigate = useNavigate();
  const api = useApi();
  const flash = useFlash();
  const { logout } = useUser();

  useEffect(() => {
    oldPasswordField.current.focus();
  }, []);

  const onSubmit = async (event) => {
    event.preventDefault();

    const password_1 = passwordField.current.value
    const password_2 = password2Field.current.value
    const old_password = oldPasswordField.current.value

    if (password_1 !== password_2) {
      setFormErrors({password2: "New passwords don't match"});
      return;
    }
    if (password_1 === old_password) {
      setFormErrors({password2: "Passwords must be diferents."});
      return;
    }
    
    const response = await api.put(TRYTON_SERVER, TRYTON_DATABASE, '/web-user-password', {
      old_password: old_password,
      password: password_1
    });
    if (response.ok) {
      setFormErrors({});
      flash(response.body.message, 'success');
      logout()
      navigate('/login');
    }
    else {
      flash(response.body, 'danger')
    }
  };

  return (
    <Body sidebar={true}>
      <h1>Change Your Password</h1>
      <Form onSubmit={onSubmit}>
        <InputField
          name="old_password" label="Old Password" type="password"
          error={formErrors.old_password} fieldRef={oldPasswordField} />
        <InputField
          name="password_1" label="New Password" type="password"
          error={formErrors.password} fieldRef={passwordField} />
        <InputField
          name="password_2" label="New Password Again" type="password"
          error={formErrors.password2} fieldRef={password2Field} />
        <Button variant="primary" type="submit">Change Password</Button>
      </Form>
    </Body>
  );
}
