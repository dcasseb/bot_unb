'use client';

import { useEffect, useState } from 'react';
import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { AppLayout } from '@/components/layout';
import { withAuth } from '@/lib/api';

export default function MonitoramentoDetalhePage({ params }: { params: { id: string } }) {
  const [history, setHistory] = useState<any[]>([]);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) return;
    withAuth(token).get(`/api/monitorings/${params.id}/history`).then((res) => setHistory(res.data));
  }, [params.id]);

  return (
    <AppLayout>
      <h1 className="mb-4 text-2xl font-semibold">Histórico da turma</h1>
      <div className="h-72 rounded-xl border border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-900">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={history.reverse()}>
            <XAxis dataKey="observed_at" hide />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="available_seats" stroke="#2563eb" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </AppLayout>
  );
}
