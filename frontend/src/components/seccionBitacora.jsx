import React, { useState } from 'react';

const SeccionBitacora = ({ eventos, proyectoId, alGuardar, alCerrar }) => {
    const [nuevaEntrada, setNuevaEntrada] = useState({
        tipo_entrada: 'Llamada',
        contenido: ''
    });
    const [estadoSeleccionado, setEstadoSeleccionado] = useState(null);

    // Tus 6 estados oficiales
    const estadosPipeline = [
        'Lead o Prospecto', 'Estudio', 'Cotizado', 
        'Adjudicado', 'Perdido', 'Anulado o Postergado'
    ];

    const handleSubmit = (e) => {
        e.preventDefault();
        
        // BLINDAJE: Enviamos los datos asegurándonos de limpiar espacios en blanco.
        // Si tu backend usa snake_case o nombres específicos, asegúrate de mapearlos aquí si es necesario.
        alGuardar({ 
            proyecto_id: parseInt(proyectoId), // Aseguramos que sea un número entero
            tipo_entrada: nuevaEntrada.tipo_entrada,
            contenido: nuevaEntrada.contenido.trim(), 
            estado_nuevo: estadoSeleccionado // Puede ir como string o null si no se seleccionó ninguno
        });
        
        // Limpiar formulario
        setNuevaEntrada({ ...nuevaEntrada, contenido: '' });
        setEstadoSeleccionado(null);
    };

    return (
        <div className="bg-white h-full shadow-2xl flex flex-col border-l border-slate-200 w-full">
            {/* CABECERA */}
            <div className="p-6 border-b bg-slate-900 text-white flex justify-between items-center">
                <div>
                    <h2 className="text-xl font-black italic">HISTORIAL Y ESTADO</h2>
                </div>
                <button onClick={alCerrar} className="text-2xl">✕</button>
            </div>

            {/* FORMULARIO */}
            <div className="p-6 bg-slate-50 border-b">
                <form onSubmit={handleSubmit} className="space-y-4">
                    {/* Selector de Tipo */}
                    <select 
                        className="w-full p-2 border rounded-lg font-bold text-sm"
                        value={nuevaEntrada.tipo_entrada}
                        onChange={(e) => setNuevaEntrada({...nuevaEntrada, tipo_entrada: e.target.value})}
                    >
                        <option value="Llamada">📞 Llamada</option>
                        <option value="Reunión">🤝 Reunión</option>
                        <option value="Correo">📧 Correo</option>
                        <option value="Hito">🚩 Hito</option>
                    </select>

                    {/* Selector de Pipeline (Tus 6 estados) */}
                    <div className="bg-white p-3 rounded-xl border border-slate-200">
                        <label className="text-[10px] font-black text-slate-400 uppercase mb-2 block">Actualizar Estado del Proyecto</label>
                        <div className="grid grid-cols-2 gap-2">
                            {estadosPipeline.map(estado => (
                                <button
                                    key={estado}
                                    type="button"
                                    onClick={() => setEstadoSeleccionado(estado === estadoSeleccionado ? null : estado)} // Permite deseleccionar si haces click de nuevo
                                    className={`text-[9px] p-2 rounded-lg border font-bold transition-all ${
                                        estadoSeleccionado === estado 
                                        ? 'bg-blue-600 text-white border-blue-600 shadow-md' 
                                        : 'bg-slate-50 text-slate-500 border-slate-100 hover:border-blue-300'
                                    }`}
                                >
                                    {estado}
                                </button>
                            ))}
                        </div>
                    </div>

                    <textarea 
                        className="w-full p-3 border rounded-lg text-sm min-h-[80px]"
                        placeholder="Escribe el detalle aquí..."
                        value={nuevaEntrada.contenido}
                        onChange={(e) => setNuevaEntrada({...nuevaEntrada, contenido: e.target.value})}
                        required
                    />

                    <button type="submit" className="w-full py-3 bg-blue-600 text-white rounded-lg font-black text-xs uppercase tracking-widest shadow-lg">
                        Registrar y Actualizar
                    </button>
                </form>
            </div>

            {/* LISTA DE EVENTOS */}
            <div className="flex-1 overflow-y-auto p-6 space-y-4">
                {eventos && eventos.map((ev) => (
                    <div key={ev.id || ev.fecha_registro} className="border-l-4 border-blue-500 pl-4 py-1 bg-slate-50 rounded-r-lg p-3">
                        <div className="flex justify-between items-start">
                            <span className="text-[10px] font-black text-blue-600 uppercase">{ev.tipo_entrada}</span>
                            {ev.estado_nuevo && (
                                <span className="text-[9px] bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full font-bold">
                                    ➜ {ev.estado_nuevo}
                                </span>
                            )}
                        </div>
                        <p className="text-sm text-slate-700 mt-1">{ev.contenido}</p>
                        <small className="text-[9px] text-slate-400 font-bold block mt-2">
                            {ev.fecha_registro ? new Date(ev.fecha_registro).toLocaleString() : 'Reciente'}
                        </small>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default SeccionBitacora;