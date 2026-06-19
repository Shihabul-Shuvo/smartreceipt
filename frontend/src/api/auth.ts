import apiClient from './client'

export interface User {
  id: number
  email: string
  full_name: string
  created_at: string
}

interface ApiEnvelope<T> {
  data: T
  message: string
  status: string
}

export interface RegisterPayload {
  email: string
  full_name: string
  password: string
}

export interface LoginPayload {
  email: string
  password: string
}

export async function register(payload: RegisterPayload): Promise<User> {
  const response = await apiClient.post<ApiEnvelope<User>>('/api/auth/register/', payload)
  return response.data.data
}

export async function login(payload: LoginPayload): Promise<User> {
  const response = await apiClient.post<ApiEnvelope<User>>('/api/auth/login/', payload)
  return response.data.data
}

export async function logout(): Promise<void> {
  await apiClient.post('/api/auth/logout/')
}

export async function getMe(): Promise<User> {
  const response = await apiClient.get<ApiEnvelope<User>>('/api/auth/me/')
  return response.data.data
}
