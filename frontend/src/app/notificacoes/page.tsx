'use client';

import { useEffect, useState } from 'react';
import { AppLayout } from '@/components/layout';
import { withAuth } from '@/lib/api';

export default function NotificacoesPage() {
  const [items, setItems] = useState<any[]>([]);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) return;
    withAuth(token).get('/api/notifications').then((res) => setItems(res.data));
  }, []);

  return (
    <AppLayout>
      <h1 className="mb-4 text-2xl font-semibold">Notificações</h1>
      <ul className="space-y-2">
        {items.map((i) => (
          <li key={i.id} className="rounded-lg border border-slate-200 bg-white p-3 dark:border-slate-800 dark:bg-slate-900">{i.message}</li>
        ))}
      </ul>
    </AppLayout>
  );
}
