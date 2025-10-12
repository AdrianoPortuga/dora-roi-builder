import axios from 'axios'
const baseURL = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'
const instance = axios.create({ baseURL, timeout: 10000 })
let bearer = ''
function setToken(t){ bearer = t }
instance.interceptors.request.use((config) => { if (bearer) { config.headers = config.headers || {}; config.headers.Authorization = `Bearer ${bearer}` } return config })
const login = async (email, password) => (await instance.post('/api/auth/login', { email, password })).data
const me = async () => (await instance.get('/api/auth/me')).data
const getVendors = async () => (await instance.get('/api/vendors/')).data
const createVendor = async (payload) => (await instance.post('/api/vendors/', payload)).data
const updateVendor = async (id, payload) => (await instance.put(`/api/vendors/${id}`, payload)).data
const deleteVendor = async (id) => (await instance.delete(`/api/vendors/${id}`)).data
export default { setToken, login, me, getVendors, createVendor, updateVendor, deleteVendor }
