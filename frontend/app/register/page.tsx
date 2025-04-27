'use client';

import { useState, useEffect, FormEvent } from 'react';
import { useRouter } from 'next/navigation';
import API from '@/lib/api';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { useAuth } from '@/context/AuthContext';

type Company = { id: number; name: string };

export default function RegisterPage() {
  const router = useRouter();
  const { login } = useAuth();

  const [companies, setCompanies] = useState<Company[]>([]);
  const [form, setForm] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    firstName: '',
    lastName: '',
    companyId: '',
  });
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    API.get('companies/')
      .then(res => setCompanies(res.data))
      .catch(console.error);
  }, []);

  function handleChange(e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) {
    const { name, value } = e.target;
    setForm(f => ({ ...f, [name]: value }));
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    if (form.password !== form.confirmPassword) {
      setError("Passwords don't match");
      return;
    }
    setLoading(true);
    setError(null);

    try {
      await API.post('auth/register/', {
        username:   form.username,
        email:      form.email,
        password:   form.password,
        first_name: form.firstName,
        last_name:  form.lastName,
        company_id: form.companyId,
      });
      // now login and redirect
      await login(form.username, form.password);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed');
      setLoading(false);
    }
  }

  return (
    <main className="max-w-md mx-auto py-10 px-4">
      <h1 className="text-2xl font-bold mb-6">Create an Account</h1>
      {error && (
        <div className="mb-4 p-2 text-red-700 bg-red-100 rounded">
          {error}
        </div>
      )}
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          name="username"
          placeholder="Username"
          value={form.username}
          onChange={handleChange}
          required
        />
        <Input
          name="email"
          type="email"
          placeholder="Email"
          value={form.email}
          onChange={handleChange}
          required
        />
        <div>
          <label htmlFor="companyId" className="block mb-1 font-medium">
            Company
          </label>
          <select
            id="companyId"
            name="companyId"
            value={form.companyId}
            onChange={handleChange}
            required
            className="w-full px-3 py-2 border rounded"
          >
            <option value="">Select your company</option>
            {companies.map(c => (
              <option key={c.id} value={c.id}>
                {c.name}
              </option>
            ))}
          </select>
        </div>
        <Input
          name="firstName"
          placeholder="First Name"
          value={form.firstName}
          onChange={handleChange}
        />
        <Input
          name="lastName"
          placeholder="Last Name"
          value={form.lastName}
          onChange={handleChange}
        />
        <Input
          name="password"
          type="password"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
          required
        />
        <Input
          name="confirmPassword"
          type="password"
          placeholder="Confirm Password"
          value={form.confirmPassword}
          onChange={handleChange}
          required
        />
        <Button type="submit" disabled={loading} className="w-full">
          {loading ? 'Registering…' : 'Register'}
        </Button>
      </form>
      <p className="mt-4 text-sm text-center">
        Already have an account?{' '}
        <a href="/login" className="text-blue-600 hover:underline">
          Sign in
        </a>
      </p>
    </main>
  );
}
