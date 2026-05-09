import axios from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000',
});

// INTERCEPTOR DE PETICIÓN: Pega el token antes de que salga la llamada
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// INTERCEPTOR DE RESPUESTA: Maneja si el token caduca (Error 401)
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            // Si el servidor dice "No autorizado", limpiamos y reiniciamos
            localStorage.removeItem('token');
            window.location.href = '/'; // Redirige al login
        }
        return Promise.reject(error);
    }
);

export default api;