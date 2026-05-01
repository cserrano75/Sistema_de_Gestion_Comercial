// src/components/SeccionBitacora.jsx
import React, { useState } from 'react';

const SeccionBitacora = ({ eventos, proyectoId, alGuardar, alCerrar }) => {
    const [nuevaEntrada, setNuevaEntrada] = useState({
        tipo_entrada: 'Llamada',
        contenido: '',
        accion_pendiente: false
    });

    const handleSubmit = (e) => {
        e.preventDefault();
        alGuardar({ ...nuevaEntrada, proyecto_id: proyectoId });
        setNuevaEntrada({ ...nuevaEntrada, contenido: '' });
    };

    return (
        <div className="bg-white h-full shadow-2xl flex flex-col border-l border-slate-200">
            {/* CABECERA */}
            <div className="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-900 text-white">
                <div>
                    <h2 className="text-xl font-black italic">HISTORIAL</h2>
                    <p className="text-[10px] uppercase text-blue-400 font-bold tracking-widest">Seguimiento de Proyecto</p>
                </div>
                <button onClick={alCerrar} className="text-white hover:text-blue-400 text-2xl font-bold">✕</button>
            </div>

            {/* FORMULARIO */}
            <div className="p-6 bg-slate-50 border-b">
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="text-[10px] font-black text-slate-400 uppercase mb-1 block">Tipo de Interacción</label>
                        <select 
                            className="w-full p-3 bg-white border border-slate-200 rounded-lg outline-none text-sm font-bold shadow-sm"
                            value={nuevaEntrada.tipo_entrada}
                            onChange={(e) => setNuevaEntrada({...nuevaEntrada, tipo_entrada: e.target.value})}
                        >
                            <option value="Llamada">📞 Llamada Telefónica</option>
                            <option value="Reunión">🤝 Reunión</option>
                            <option value="Correo">📧 Correo Electrónico</option>
                            <option value="Hito">🚩 Hito / Avance</option>
                        </select>
                    </div>

                    <div>
                        <label className="text-[10px] font-black text-slate-400 uppercase mb-1 block">Detalle</label>
                        <textarea 
                            className="w-full p-3 bg-white border border-slate-200 rounded-lg outline-none text-sm shadow-sm min-h-[100px]"
                            value={nuevaEntrada.contenido}
                            onChange={(e) => setNuevaEntrada({...nuevaEntrada, contenido: e.target.value})}
                            placeholder="Acuerdos, notas o próximos pasos..."
                            required
                        />
                    </div>

                    <button type="submit" className="w-full py-3 bg-blue-600 text-white rounded-lg font-bold text-sm shadow-lg shadow-blue-200 hover:bg-blue-700 transition-colors">
                        REGISTRAR EVENTO
                    </button>
                </form>
            </div>

            {/* LISTA DE EVENTOS (TIMELINE) */}
            <div className="flex-1 overflow-y-auto p-6 space-y-6">
                {eventos.length === 0 ? (
                    <div className="text-center py-10">
                        <p className="text-slate-300 font-bold italic">No hay registros aún.</p>
                    </div>
                ) : (
                    eventos.map((ev) => (
                        <div key={ev.id} className="relative pl-6 border-l-2 border-blue-500 py-1">
                            <div className="absolute -left-[9px] top-0 w-4 h-4 bg-blue-500 rounded-full border-4 border-white shadow-sm"></div>
                            <div className="bg-white border border-slate-100 p-4 rounded-xl shadow-sm">
                                <div className="flex justify-between items-start mb-2">
                                    <span className="text-[10px] font-black text-blue-600 uppercase">{ev.tipo_entrada}</span>
                                    <span className="text-[9px] font-bold text-slate-400">{new Date(ev.fecha_registro).toLocaleString('es-CL')}</span>
                                </div>
                                <p className="text-slate-700 text-sm leading-relaxed">{ev.contenido}</p>
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default SeccionBitacora;