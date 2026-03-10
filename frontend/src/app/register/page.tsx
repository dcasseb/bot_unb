'use client';

import { FormEvent, useState } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';

export default function RegisterPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter();

  async function submit(e: FormEvent) {
    e.preventDefault();
    const res = await api.post('/api/auth/register', { email, password });
    localStorage.setItem('token', res.data.access_token);
    router.push('/dashboard');
  }

  return (
    <div className="mx-auto mt-24 max-w-md rounded-xl border border-slate-200 bg-white p-6 dark:border-slate-800 dark:bg-slate-900">
      <h1 className="mb-4 text-xl font-semibold">Criar conta</h1>
      <form className="space-y-3" onSubmit={submit}>
        <input className="w-full rounded-md border p-2" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input className="w-full rounded-md border p-2" placeholder="Senha" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <button className="w-full rounded-md bg-slate-900 p-2 text-white">Registrar</button>
      </form>
    </div>
  );
}
