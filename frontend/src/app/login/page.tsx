'use client';

import { FormEvent, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import api from '@/lib/api';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  async function submit(e: FormEvent) {
    e.preventDefault();
    const res = await api.post('/api/auth/login', { email, password });
    localStorage.setItem('token', res.data.access_token);
    router.push('/dashboard');
  }

  return (
    <div className="mx-auto mt-24 max-w-md rounded-xl border border-slate-200 bg-white p-6 dark:border-slate-800 dark:bg-slate-900">
      <h1 className="mb-4 text-xl font-semibold">Entrar</h1>
      <form className="space-y-3" onSubmit={submit}>
        <input className="w-full rounded-md border p-2" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input className="w-full rounded-md border p-2" placeholder="Senha" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <button className="w-full rounded-md bg-slate-900 p-2 text-white">Login</button>
      </form>
      <p className="mt-4 text-center text-sm text-slate-600 dark:text-slate-300">
        Ainda não tem conta?{' '}
        <Link className="font-medium text-slate-900 underline dark:text-white" href="/register">
          Registrar
        </Link>
      </p>
    </div>
  );
}
