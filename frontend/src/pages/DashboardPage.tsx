import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function DashboardPage() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  async function handleLogout() {
    await logout()
    navigate('/login')
  }

  return (
    <div>
      <h1>Welcome, {user?.full_name}</h1>
      <button onClick={handleLogout}>Logout</button>
    </div>
  )
}
