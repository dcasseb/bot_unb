'use client';

import { FormEvent, useState } from 'react';
import { useRouter } from 'next/navigation';
import { AppLayout } from '@/components/layout';
import { withAuth } from '@/lib/api';

export default function NovoMonitoramentoPage() {
  const router = useRouter();
  const [form, setForm] = useState({ discipline_code: '', discipline_name: '', class_group: '', semester: '', check_interval_seconds: 120, query_url: '' });

  async function submit(e: FormEvent) {
    e.preventDefault();
    const token = localStorage.getItem('token');
    if (!token) return;
    await withAuth(token).post('/api/monitorings', form);
    router.push('/monitoramentos');
  }

  return (
    <AppLayout>
      <h1 className="mb-4 text-2xl font-semibold">Novo monitoramento</h1>
      <form onSubmit={submit} className="grid gap-3 rounded-xl border border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-900">
        {Object.entries(form).map(([key, value]) => (
          <input key={key} className="rounded-md border p-2" placeholder={key} value={String(value)} onChange={(e) => setForm({ ...form, [key]: e.target.type === 'number' ? Number(e.target.value) : e.target.value })} />
        ))}
        <button className="rounded-md bg-slate-900 p-2 text-white">Monitorar turma</button>
      </form>
    </AppLayout>
  );
}
