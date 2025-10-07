import { BrowserRouter, Link, Navigate, Route, Routes, useLocation } from 'react-router-dom'
import Login from './pages/Login'

function Page({ title }: { title: string }) {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold">{title}</h1>
      <p className="text-slate-500 mt-2">Coming soon.</p>
    </div>
  )
}

function Layout() {
  const location = useLocation()
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null
  if (!token && location.pathname !== '/login') {
    return <Navigate to="/login" replace />
  }
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <aside className="fixed inset-y-0 left-0 w-60 bg-white border-r border-slate-200 p-4 hidden md:block">
        <div className="text-xl font-bold mb-6">KenyaPOS</div>
        <nav className="flex flex-col gap-2">
          <Link className="hover:bg-slate-100 rounded px-3 py-2" to="/">Dashboard</Link>
          <Link className="hover:bg-slate-100 rounded px-3 py-2" to="/sales">Sales</Link>
          <Link className="hover:bg-slate-100 rounded px-3 py-2" to="/inventory">Inventory</Link>
          <Link className="hover:bg-slate-100 rounded px-3 py-2" to="/customers">Customers</Link>
          <Link className="hover:bg-slate-100 rounded px-3 py-2" to="/purchases">Purchases</Link>
          <Link className="hover:bg-slate-100 rounded px-3 py-2" to="/reports">Reports</Link>
          <Link className="hover:bg-slate-100 rounded px-3 py-2" to="/settings">Settings</Link>
        </nav>
      </aside>
      <main className="md:ml-60">
        <header className="sticky top-0 bg-white border-b border-slate-200 p-4 flex items-center justify-between">
          <div className="font-medium">Welcome</div>
          <div className="flex items-center gap-2">
            <button className="rounded px-3 py-1.5 bg-slate-900 text-white text-sm">Dark</button>
          </div>
        </header>
        <Routes>
          <Route path="/" element={<Page title="Dashboard" />} />
          <Route path="/sales" element={<Page title="Sales" />} />
          <Route path="/inventory" element={<Page title="Inventory" />} />
          <Route path="/customers" element={<Page title="Customers" />} />
          <Route path="/purchases" element={<Page title="Purchases" />} />
          <Route path="/reports" element={<Page title="Reports" />} />
          <Route path="/settings" element={<Page title="Settings" />} />
          <Route path="*" element={<Navigate to="/" replace />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </main>
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <Layout />
    </BrowserRouter>
  )
}
