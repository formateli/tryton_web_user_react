import { useState, useEffect, useRef } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import { useNavigate } from 'react-router-dom';
import Body from '../components/Body';
import InputField from '../components/InputField';
import { useApi } from '../contexts/ApiProvider';
import { useUser } from '../contexts/UserProvider';
import { useFlash } from '../contexts/FlashProvider';

const TRYTON_SERVER = process.env.REACT_APP_TRYTON_SERVER;
const TRYTON_DATABASE = process.env.REACT_APP_TRYTON_DATABASE;

export default function ProfilePage() {
  const [formErrors, setFormErrors] = useState({});
  const nameField = useRef();
  const emailField = useRef();
  const aboutMeField = useRef();
  const api = useApi();
  const { user, setUser } = useUser();
  const flash = useFlash();
  const navigate = useNavigate();

  useEffect(() => {
    nameField.current.value = user.data.name;
    emailField.current.value = user.data.email;
    nameField.current.focus();
  }, [user]);

  const onSubmit = async (event) => {
    event.preventDefault();
    const response = await api.put(TRYTON_SERVER, TRYTON_DATABASE, '/web-user-me', {
      name: nameField.current.value
    });
    if (response.ok) {
      setFormErrors({});
      setUser(response.body);
      flash('User updated.', 'success');
      navigate('/profile');
    }
    else {
      flash(response.body, 'danger')
    }
  };

  return (
    <Body sidebar>
      <Form onSubmit={onSubmit}>
        <InputField
          name="name" label="name"
          error={formErrors.username} fieldRef={nameField} />
        <InputField
          name="email" label="Email"
          error={formErrors.email} fieldRef={emailField} />
        <Button variant="primary" type="submit">Save</Button>
      </Form>
    </Body>
  );
}
