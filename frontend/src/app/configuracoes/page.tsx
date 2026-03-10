import { AppLayout } from '@/components/layout';

export default function ConfiguracoesPage() {
  return (
    <AppLayout>
      <h1 className="mb-4 text-2xl font-semibold">Configurações</h1>
      <div className="grid gap-3 rounded-xl border border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-900">
        <label className="flex items-center gap-2"><input type="checkbox" defaultChecked /> Telegram</label>
        <label className="flex items-center gap-2"><input type="checkbox" defaultChecked /> Email</label>
        <label className="flex items-center gap-2"><input type="checkbox" defaultChecked /> Browser push</label>
      </div>
    </AppLayout>
  );
}
