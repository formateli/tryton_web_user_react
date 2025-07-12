import { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Body from '../components/Body';
import { useApi } from '../contexts/ApiProvider';
import { useFlash } from '../contexts/FlashProvider';
import { useUser } from '../contexts/UserProvider';

const TRYTON_SERVER = process.env.REACT_APP_TRYTON_SERVER;
const TRYTON_DATABASE = process.env.REACT_APP_TRYTON_DATABASE;

export default function EmailVerificationPage() {
  const navigate = useNavigate();
  const { search } = useLocation();
  const api = useApi();
  const flash = useFlash();
  const token = new URLSearchParams(search).get('token');
  const { logout } = useUser();


  if (!token) {
    navigate('/');
  }

  useEffect(() => {
    const verify = async() => {
      const response = await api.put(TRYTON_SERVER, TRYTON_DATABASE, '/web-user-email-verify', {
        'token': token});

      if (response.ok){
        flash(response.body.message, 'success');
	logout()
	navigate('/web-user-login');
      }
      else{
        flash(response.body, 'danger');
      }
    }; // verify

    verify();

  }, []);

  return (
    <Body>
      <h1>Email verification</h1>
    </Body>
  );
}
