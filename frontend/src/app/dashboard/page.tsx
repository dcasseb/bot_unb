'use client';

import { useEffect, useState } from 'react';
import { AppLayout } from '@/components/layout';
import { withAuth } from '@/lib/api';

export default function DashboardPage() {
  const [data, setData] = useState<any[]>([]);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) return;
    withAuth(token).get('/api/monitorings').then((res) => setData(res.data));
  }, []);

  const vagasAbertas = data.filter((m) => (m.last_state?.available_seats ?? 0) > 0).length;

  return (
    <AppLayout>
      <h1 className="mb-4 text-2xl font-semibold">Dashboard</h1>
      <div className="grid gap-4 md:grid-cols-3">
        <Card title="Monitoramentos" value={String(data.length)} />
        <Card title="Turmas com vaga" value={String(vagasAbertas)} />
        <Card title="Última atualização" value={new Date().toLocaleTimeString('pt-BR')} />
      </div>
    </AppLayout>
  );
}

function Card({ title, value }: { title: string; value: string }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-800 dark:bg-slate-900">
      <p className="text-sm text-slate-500">{title}</p>
      <p className="text-2xl font-semibold">{value}</p>
    </div>
  );
}
