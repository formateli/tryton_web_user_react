import Container from 'react-bootstrap/Container';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import FlashProvider from './contexts/FlashProvider';
import ApiProvider from './contexts/ApiProvider';
import UserProvider from './contexts/UserProvider';
import Header from './components/Header';
import PublicRoute from './components/PublicRoute';
import PrivateRoute from './components/PrivateRoute';
import ProfilePage from './pages/ProfilePage'
import WelcomePage from './pages/WelcomePage';
import EmailVerificationPage from './pages/EmailVerificationPage'
import PasswordChangePage from './pages/PasswordChangePage'
import LoginPage from './pages/LoginPage';
import RegistrationPage from './pages/RegistrationPage';

export default function App() {
  return (
    <Container fluid className="App">
      <BrowserRouter>
        <FlashProvider>
          <ApiProvider>
            <UserProvider>
              <Header />
              <Routes>
                <Route path="/web-user-login" element={
                  <PublicRoute><LoginPage /></PublicRoute>
                } />
                <Route path="/web-user-register" element={
                  <PublicRoute><RegistrationPage /></PublicRoute>
                } />
                <Route path="/web-user-email-verify" element={
                  <PublicRoute><EmailVerificationPage /></PublicRoute>
                } />
                <Route path="*" element={
                  <PrivateRoute>
                    <Routes>
                      <Route path="/" element={<WelcomePage />} />
                      <Route path="/profile" element={<ProfilePage />} />
                      <Route path="/password" element={<PasswordChangePage />} />
                      <Route path="*" element={<Navigate to="/" />} />
                    </Routes>
                  </PrivateRoute>
                } />
              </Routes>
            </UserProvider>
          </ApiProvider>
        </FlashProvider>
      </BrowserRouter>
    </Container>
  );
}
