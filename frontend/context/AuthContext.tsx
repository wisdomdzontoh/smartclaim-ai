'use client';

import {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from 'react';
import { useRouter } from 'next/navigation';
import API from '@/lib/api';

interface User {
  username: string;
  email: string;
  role?: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // Fetch the user's profile from the API
  const fetchProfile = async () => {
    try {
      const { data } = await API.get('auth/users/me/');
      setUser({
        username: data.username,
        email: data.email,
        role: data.role,
      });
    } catch (err) {
      console.error('Failed to fetch user profile:', err);
      logout();
    }
  };

  // On mount, verify token and load profile
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      API.post('auth/token/verify/', { token })
        .then(fetchProfile)
        .catch(() => {
          logout();
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  // Log in, store tokens, fetch profile, redirect
  const login = async (username: string, password: string) => {
    setLoading(true);
    try {
      const { data } = await API.post('auth/token/', { username, password });
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
      await fetchProfile();
      router.push('/dashboard');
    } catch (err) {
      console.error('Login failed:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Log out, clear state & storage, redirect
  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
    router.push('/login');
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook for easy access
export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return ctx;
};
