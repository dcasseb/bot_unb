'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { AppLayout } from '@/components/layout';
import { withAuth } from '@/lib/api';

export default function MonitoramentosPage() {
  const [items, setItems] = useState<any[]>([]);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) return;
    withAuth(token).get('/api/monitorings').then((res) => setItems(res.data));
  }, []);

  return (
    <AppLayout>
      <div className="mb-4 flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Monitoramentos</h1>
        <Link href="/monitoramentos/novo" className="rounded-md bg-slate-900 px-3 py-2 text-white">Novo</Link>
      </div>
      <div className="overflow-hidden rounded-xl border border-slate-200 dark:border-slate-800">
        <table className="w-full text-sm">
          <thead className="bg-slate-100 dark:bg-slate-900">
            <tr><th className="p-3 text-left">Disciplina</th><th>Turma</th><th>Vagas livres</th><th>Status</th></tr>
          </thead>
          <tbody>
            {items.map((m) => (
              <tr key={m.id} className="border-t border-slate-200 dark:border-slate-800">
                <td className="p-3">{m.discipline_code}</td><td>{m.class_group}</td><td>{m.last_state?.available_seats ?? '-'}</td><td>{m.last_state?.status ?? '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </AppLayout>
  );
}
