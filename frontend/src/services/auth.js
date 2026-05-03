import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/auth';

export const login = async (email, password) => {
    // OAuth2 espera "username" y "password" como Form Data, no como JSON
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    const response = await axios.post(`${API_URL}/token`, formData);
    
    if (response.data.access_token) {
        // Guardamos el token en el almacenamiento local del navegador
        localStorage.setItem('token', response.data.access_token);
    }
    return response.data;
};

export const logout = () => {
    localStorage.removeItem('token');
};