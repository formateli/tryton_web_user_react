import Body from '../components/Body';
import { useUser } from '../contexts/UserProvider';

export default function ProfilePage() {
const { user } = useUser();

  return (
    <Body sidebar>
      <h3>Name: {user.name}</h3>
      <h3>Email: {user.email}</h3>
    </Body>
  ); 
}
