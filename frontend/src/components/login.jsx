import React, { useState } from 'react';
import axios from 'axios';

const Login = ({ onLoginSuccess }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    // FastAPI espera los datos en formato FormData para el endpoint de token
    const formData = new FormData();
    formData.append('username', email); // FastAPI usa 'username' por defecto
    formData.append('password', password);

    try {
      const response = await axios.post('http://127.0.0.1:8000/auth/token', formData);
      
      // 1. EXTRAEMOS EL TOKEN
      const token = response.data.access_token;

      // 2. LO GUARDAMOS (Esta es la llave que el Interceptor usará)
      localStorage.setItem('token', token);

      // 3. NOTIFICAMOS AL APP.JSX
      onLoginSuccess();
      
    } catch (err) {
      setError('Credenciales incorrectas o servidor fuera de línea');
      console.error("Login error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-900 px-4">
      <div className="max-w-md w-full bg-white rounded-2xl shadow-2xl p-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-black italic text-slate-900">
            CRM <span className="text-blue-600">IND</span>
          </h1>
          <p className="text-slate-500 font-medium">Ingresa a tu panel de control</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {error && (
            <div className="bg-red-50 text-red-600 p-3 rounded-lg text-sm font-bold border border-red-100">
              {error}
            </div>
          )}
          
          <div>
            <label className="block text-xs font-black uppercase text-slate-400 mb-2">Email</label>
            <input
              type="email"
              required
              className="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-blue-500 transition-all"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="correo@ejemplo.com"
            />
          </div>

          <div>
            <label className="block text-xs font-black uppercase text-slate-400 mb-2">Contraseña</label>
            <input
              type="password"
              required
              className="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-blue-500 transition-all"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className={`w-full py-4 rounded-xl font-black text-white transition-all ${
              loading ? 'bg-slate-400' : 'bg-blue-600 hover:bg-blue-700 shadow-lg shadow-blue-200'
            }`}
          >
            {loading ? 'VERIFICANDO...' : 'ENTRAR AL SISTEMA'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;