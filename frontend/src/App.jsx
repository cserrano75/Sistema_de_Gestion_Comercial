import React, { useState, useEffect } from 'react';
import api from './api';
// IMPORTACIONES DE COMPONENTES
import Login from './components/login';
import SeccionBitacora from './components/seccionBitacora';

function App() {
  // --- 1. ESTADOS DE AUTENTICACIÓN ---
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // --- 2. ESTADOS DEL CRM ---
  const [vistaActual, setVistaActual] = useState('proyectos');
  const [cargando, setCargando] = useState(true);
  const [mostrarModal, setMostrarModal] = useState(false);
  const [proyectos, setProyectos] = useState([]);
  const [clientes, setClientes] = useState([]);
  
  const [proyectoSeleccionado, setProyectoSeleccionado] = useState(null);
  const [eventosBitacora, setEventosBitacora] = useState([]);
  const [mostrarBitacora, setMostrarBitacora] = useState(false);

  // NUEVOS ESTADOS PARA EDICIÓN DE CLIENTE
  const [mostrarModalEditar, setMostrarModalEditar] = useState(false);
  const [clienteEditando, setClienteEditando] = useState(null);

  const [stats, setStats] = useState({
      monto_adjudicado: 0,
      monto_en_estudio: 0,
      monto_perdido: 0,
      tasa_conversion: 0
  });

  const [nuevoCliente, setNuevoCliente] = useState({ rut: '', razon_social: '', giro: '', direccion: '' });
  const [nuevoProyecto, setNuevoProyecto] = useState({ nombre: '', cliente_id: '', presupuesto: 0, estado: 'Lead o Prospecto' });
  const [filtroEstado, setFiltroEstado] = useState("Todos");
  const estadosFiltro = ["Todos", "Lead o Prospecto", "Estudio", "Cotizado", "Adjudicado", "Perdido", "Anulado o Postergado"];

  // --- 3. LÓGICA DE CARGA ---
  const cargarTodo = async () => {
    try {
      setCargando(true);
      // CORREGIDO: Se agregaron las barras diagonales '/' al final de cada endpoint
      const [resProy, resCli, resStats] = await Promise.all([
        api.get('/proyectos/'),
        api.get('/clientes/'),
        api.get('/proyectos/stats/resumen/')
      ]);

      setProyectos(resProy.data || []);
      setClientes(resCli.data || []);
      setStats(resStats.data || { monto_adjudicado: 0, monto_en_estudio: 0, monto_perdido: 0, tasa_conversion: 0 });
    } catch (e) { 
      console.error("Error cargando datos:", e);
    } finally { 
      setCargando(false);
    }
  };

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
      cargarTodo();
    }
  }, []);

  // --- 4. FUNCIONES AUXILIARES ---
  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
  };

  const manejarLoginExitoso = () => {
    setIsAuthenticated(true);
    cargarTodo();
  };

  const guardarCliente = async (e) => {
    e.preventDefault();
    try {
      await api.post('/clientes/', nuevoCliente);
      setNuevoCliente({ rut: '', razon_social: '', giro: '', direccion: '' });
      setMostrarModal(false);
      cargarTodo();
    } catch (e) { 
      alert("Error al guardar cliente"); 
    }
  };

  // NUEVA FUNCIÓN: Dispara los cambios del Cliente al Backend
  const manejarActualizarCliente = async (e) => {
    e.preventDefault();
    try {
      const datosLimpios = {
        rut: clienteEditando.rut,
        razon_social: clienteEditando.razon_social,
        nombre: clienteEditando.nombre || clienteEditando.razon_social, 
        giro: clienteEditando.giro || "",
        direccion: clienteEditando.direccion || ""
      };

      // CORREGIDO: Se añadió la barra diagonal '/' al final de la ruta dinámica
      await api.put(`/clientes/${clienteEditando.id}/`, datosLimpios);
      
      setMostrarModalEditar(false);
      setClienteEditando(null);
      cargarTodo(); 
    } catch (e) {
      console.error("Error detallado de la API:", e.response?.data || e);
      alert("Error al actualizar el cliente. Revisa la consola del navegador.");
    }
  };

  const abrirEditarCliente = (cliente) => {
    setClienteEditando({ ...cliente });
    setMostrarModalEditar(true);
  };

  const manejarGuardarProyecto = async (e) => {
    e.preventDefault();
    if (!nuevoProyecto.cliente_id) return alert("Seleccione cliente");
    try {
      await api.post('/proyectos/', nuevoProyecto);
      setNuevoProyecto({ nombre: '', cliente_id: '', presupuesto: 0, estado: 'Lead o Prospecto' });
      setMostrarModal(false);
      cargarTodo();
    } catch (e) { 
      alert("Error al guardar proyecto"); 
    }
  };

  const abrirBitacora = async (proyecto) => {
    try {
      // CORREGIDO: Se añadió la barra diagonal '/' al final del recurso de la bitácora
      const res = await api.get(`/proyectos/${proyecto.id}/bitacora/`);
      setEventosBitacora(res.data);
      setProyectoSeleccionado(proyecto);
      setMostrarBitacora(true);
    } catch (error) {
      console.error("Error al cargar bitácora:", error);
      alert("No se pudo cargar el historial de este proyecto");
    }
  };

  const guardarEnBitacora = async (nuevaEntrada) => {
    try {
        // CORREGIDO: Mapeamos tanto 'tipo_entrada' como 'tipo_contacto' por seguridad 
        // y removemos el emoji si el selector lo incluye (ej: "📞 Llamada" -> "Llamada")
        const tipoLimpio = (nuevaEntrada.tipo_entrada || nuevaEntrada.tipo_contacto || "Llamada")
          .replace(/[\uE000-\uF8FF]|\uD83C[\uDC00-\uDFFF]|\uD83D[\uDC00-\uDFFF]|[\u2011-\u26FF]|\uD83E[\uDD00-\uDFFF]/g, "")
          .trim();

        const datosLimpios = {
            proyecto_id: parseInt(nuevaEntrada.proyecto_id), 
            tipo_entrada: tipoLimpio, // FastAPI espera este campo limpio sin emojis
            contenido: nuevaEntrada.contenido ? nuevaEntrada.contenido.trim() : "", 
            estado_nuevo: nuevaEntrada.estado_nuevo || null 
        };

        // Forzamos la barra diagonal al final
        await api.post('/bitacora/', datosLimpios);
        
        cargarTodo(); // Refresca la interfaz
        setMostrarBitacora(false);
    } catch (error) { 
        console.error("Error detallado al guardar bitácora:", error.response?.data || error);
        alert("Error al guardar en bitácora. Revisa los campos enviados."); 
    }
  };

  const proyectosFiltrados = proyectos.filter(p => 
      filtroEstado === "Todos" ? true : p.estado === filtroEstado
  );

  if (!isAuthenticated) {
    return <Login onLoginSuccess={manejarLoginExitoso} />;
  }

  return (
    <div className="flex h-screen bg-slate-50 text-slate-900 overflow-hidden font-sans">
      
      {/* SIDEBAR */}
      <aside className="w-64 bg-slate-900 text-white flex flex-col">
        <div className="p-8 text-2xl font-black italic border-b border-slate-800">
          CRM <span className="text-blue-500">IND</span>
        </div>
        <nav className="flex-1 p-4 space-y-2 mt-4">
          <button onClick={() => setVistaActual('proyectos')} className={`w-full text-left p-4 rounded-xl font-bold ${vistaActual === 'proyectos' ? 'bg-blue-600' : 'hover:bg-slate-800'}`}>📊 PROYECTOS</button>
          <button onClick={() => setVistaActual('clientes')} className={`w-full text-left p-4 rounded-xl font-bold ${vistaActual === 'clientes' ? 'bg-blue-600' : 'hover:bg-slate-800'}`}>🏢 CLIENTES</button>
        </nav>
        <div className="p-4 border-t border-slate-800">
          <button onClick={handleLogout} className="w-full text-left p-4 rounded-xl font-bold text-red-400 hover:bg-red-900/20 transition-colors">
            🚪 CERRAR SESIÓN
          </button>
        </div>
      </aside>

      {/* CONTENIDO PRINCIPAL */}
      <main className="flex-1 flex flex-col relative">
        <header className="h-20 bg-white border-b flex items-center justify-between px-10">
          <h2 className="text-xl font-bold uppercase">{vistaActual}</h2>
          <button onClick={() => setMostrarModal(true)} className="bg-blue-600 text-white px-6 py-2 rounded-lg font-bold text-sm">+ AGREGAR</button>
        </header>

        <section className="p-10 flex-1 overflow-y-auto">
          {cargando ? (
            <div className="text-center font-bold text-slate-400">Sincronizando...</div>
          ) : (
            vistaActual === 'proyectos' ? (
              <div className="space-y-6">
                {/* KPIs */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                    <div className="bg-white p-6 rounded-2xl shadow-sm border-t-4 border-green-500">
                        <div className="text-slate-400 text-[10px] font-bold uppercase">Adjudicado</div>
                        <div className="text-2xl font-black text-slate-800">${stats.monto_adjudicado.toLocaleString('es-CL')}</div>
                    </div>
                    <div className="bg-white p-6 rounded-2xl shadow-sm border-t-4 border-purple-500">
                        <div className="text-slate-400 text-[10px] font-bold uppercase">En Estudio / Cotizado</div>
                        <div className="text-2xl font-black text-slate-800">${stats.monto_en_estudio.toLocaleString('es-CL')}</div>
                    </div>
                    <div className="bg-white p-6 rounded-2xl shadow-sm border-t-4 border-red-500">
                        <div className="text-slate-400 text-[10px] font-bold uppercase">Perdido</div>
                        <div className="text-2xl font-black text-slate-800">${stats.monto_perdido.toLocaleString('es-CL')}</div>
                    </div>
                    <div className="bg-white p-6 rounded-2xl shadow-sm border-t-4 border-blue-500">
                        <div className="text-slate-400 text-[10px] font-bold uppercase">Efectividad</div>
                        <div className="text-2xl font-black text-slate-800">{stats.tasa_conversion}%</div>
                    </div>
                </div>

                <div className="bg-white rounded-xl shadow border">
                  {/* FILTROS */}
                  <div className="p-4 border-b overflow-x-auto pb-2">
                      <div className="flex space-x-2 min-w-max">
                          {estadosFiltro.map(estado => {
                              const conteo = estado === "Todos" ? proyectos.length : proyectos.filter(p => p.estado === estado).length;
                              return (
                                  <button
                                      key={estado}
                                      onClick={() => setFiltroEstado(estado)}
                                      className={`px-4 py-2 rounded-full text-[11px] font-black uppercase transition-all flex items-center gap-2 ${
                                          filtroEstado === estado ? 'bg-blue-600 text-white shadow-lg' : 'bg-white text-slate-500 border hover:border-blue-400'
                                      }`}
                                  >
                                      {estado} <span className="opacity-50">{conteo}</span>
                                  </button>
                              );
                          })}
                      </div>
                  </div>

                  {/* TABLA PROYECTOS */}
                  <table className="w-full text-left">
                    <thead className="bg-slate-50 border-b text-[10px] uppercase font-black text-slate-400">
                      <tr>
                        <th className="p-4">Proyecto</th>
                        <th className="p-4">Presupuesto</th>
                        <th className="p-4">Estado</th>
                        <th className="p-4">Acciones</th>
                      </tr>
                    </thead>
                    <tbody>
                      {proyectosFiltrados.map(p => (
                        <tr key={p.id} className="border-b hover:bg-slate-50 text-sm">
                          <td className="p-4 font-bold">{p.nombre}</td>
                          <td className="p-4 font-mono text-blue-600 font-bold">${p.presupuesto.toLocaleString('es-CL')}</td>
                          <td className="p-4">
                            <span className={`px-3 py-1 rounded-full text-[10px] font-black uppercase ${
                              p.estado === 'Adjudicado' ? 'bg-green-100 text-green-700' :
                              p.estado === 'Perdido' ? 'bg-red-100 text-red-700' :
                              p.estado === 'Cotizado' ? 'bg-blue-100 text-blue-700' :
                              p.estado === 'Estudio' ? 'bg-purple-100 text-purple-700' :
                              'bg-slate-100 text-slate-600'
                            }`}>
                              {p.estado}
                            </span>
                          </td>
                          <td className="p-4">
                            <button onClick={() => abrirBitacora(p)} className="text-blue-600 hover:underline font-bold">Ver Historial</button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            ) : (
              /* VISTA CLIENTES */
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {clientes.map(c => (
                  <div key={c.id} className="bg-white p-6 rounded-xl shadow border border-slate-100 flex flex-col justify-between">
                    <div>
                      <div className="text-[10px] font-black text-slate-300 mb-2">{c.rut}</div>
                      <h3 className="font-black text-slate-800 uppercase">{c.razon_social}</h3>
                      {c.giro && <p className="text-xs text-slate-400 mt-1">{c.giro}</p>}
                      {c.direccion && <p className="text-xs text-slate-400 italic mt-0.5">{c.direccion}</p>}
                    </div>
                    
                    <div className="mt-4 pt-4 border-t border-slate-50 flex justify-end">
                      <button 
                        onClick={() => abrirEditarCliente(c)}
                        className="text-xs bg-slate-100 hover:bg-blue-50 hover:text-blue-600 px-3 py-1.5 rounded-lg font-bold transition-colors"
                      >
                        ✏️ Editar
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )
          )}
        </section>

        {/* PANEL DE BITÁCORA */}
        {mostrarBitacora && (
          <div className="fixed inset-0 z-40 flex justify-end">
            <div className="absolute inset-0 bg-slate-900/40" onClick={() => setMostrarBitacora(false)}></div>
            <div className="relative z-50 w-full max-w-md">
                <SeccionBitacora 
                    proyectoId={proyectoSeleccionado?.id}
                    eventos={eventosBitacora}
                    alGuardar={guardarEnBitacora}
                    alCerrar={() => setMostrarBitacora(false)}
                />
            </div>
          </div>
        )}
      </main>

      {/* MODAL DE CREACIÓN */}
      {mostrarModal && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur flex items-center justify-center z-50">
          <div className="bg-white p-8 rounded-2xl shadow-2xl w-full max-w-md relative text-sm">
            <button onClick={() => setMostrarModal(false)} className="absolute top-4 right-4 font-bold">✕</button>
            <h2 className="text-2xl font-black mb-6">Nuevo {vistaActual === 'proyectos' ? 'Proyecto' : 'Cliente'}</h2>
            {vistaActual === 'clientes' ? (
              <form onSubmit={guardarCliente} className="space-y-4">
                <input required placeholder="RUT" className="w-full p-3 bg-slate-50 rounded-lg outline-none" value={nuevoCliente.rut} onChange={e => setNuevoCliente({...nuevoCliente, rut: e.target.value})} />
                <input required placeholder="Razón Social" className="w-full p-3 bg-slate-50 rounded-lg outline-none" value={nuevoCliente.razon_social} onChange={e => setNuevoCliente({...nuevoCliente, razon_social: e.target.value})} />
                <input placeholder="Giro" className="w-full p-3 bg-slate-50 rounded-lg outline-none" value={nuevoCliente.giro || ''} onChange={e => setNuevoCliente({...nuevoCliente, giro: e.target.value})} />
                <input placeholder="Dirección" className="w-full p-3 bg-slate-50 rounded-lg outline-none" value={nuevoCliente.direccion || ''} onChange={e => setNuevoCliente({...nuevoCliente, direccion: e.target.value})} />
                <button type="submit" className="w-full py-3 bg-blue-600 text-white rounded-lg font-bold">GUARDAR CLIENTE</button>
              </form>
            ) : (
              <form onSubmit={manejarGuardarProyecto} className="space-y-4">
                <input required placeholder="Nombre Proyecto" className="w-full p-3 bg-slate-50 rounded-lg outline-none" value={nuevoProyecto.nombre} onChange={e => setNuevoProyecto({...nuevoProyecto, nombre: e.target.value})} />
                <select required className="w-full p-3 bg-slate-50 rounded-lg outline-none" value={nuevoProyecto.cliente_id} onChange={e => setNuevoProyecto({...nuevoProyecto, cliente_id: e.target.value})}>
                  <option value="">-- Seleccionar Cliente --</option>
                  {clientes.map(c => <option key={c.id} value={c.id}>{c.razon_social}</option>)}
                </select>
                <input required type="number" placeholder="Presupuesto" className="w-full p-3 bg-slate-50 rounded-lg outline-none" value={nuevoProyecto.presupuesto} onChange={e => setNuevoProyecto({...nuevoProyecto, presupuesto: parseFloat(e.target.value)})} />
                <button type="submit" className="w-full py-3 bg-blue-600 text-white rounded-lg font-bold">CREAR PROYECTO</button>
              </form>
            )}
          </div>
        </div>
      )}

      {/* MODAL DE EDICIÓN DE CLIENTE */}
      {mostrarModalEditar && clienteEditando && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur flex items-center justify-center z-50">
          <div className="bg-white p-8 rounded-2xl shadow-2xl w-full max-w-md relative text-sm">
            <button onClick={() => setMostrarModalEditar(false)} className="absolute top-4 right-4 font-bold">✕</button>
            <h2 className="text-2xl font-black mb-6">Editar Cliente</h2>
            
            <form onSubmit={manejarActualizarCliente} className="space-y-4">
              <div>
                <label className="text-[10px] uppercase font-black text-slate-400 block mb-1">RUT</label>
                <input required placeholder="RUT" className="w-full p-3 bg-slate-50 rounded-lg outline-none font-bold" value={clienteEditando.rut} onChange={e => setClienteEditando({...clienteEditando, rut: e.target.value})} />
              </div>
              <div>
                <label className="text-[10px] uppercase font-black text-slate-400 block mb-1">Razón Social</label>
                <input required placeholder="Razón Social" className="w-full p-3 bg-slate-50 rounded-lg outline-none font-bold" value={clienteEditando.razon_social} onChange={e => setClienteEditando({...clienteEditando, razon_social: e.target.value})} />
              </div>
              <div>
                <label className="text-[10px] uppercase font-black text-slate-400 block mb-1">Giro</label>
                <input placeholder="Giro (Opcional)" className="w-full p-3 bg-slate-50 rounded-lg outline-none" value={clienteEditando.giro || ''} onChange={e => setClienteEditando({...clienteEditando, giro: e.target.value})} />
              </div>
              <div>
                <label className="text-[10px] uppercase font-black text-slate-400 block mb-1">Dirección</label>
                <input placeholder="Dirección (Opcional)" className="w-full p-3 bg-slate-50 rounded-lg outline-none" value={clienteEditando.direccion || ''} onChange={e => setClienteEditando({...clienteEditando, direccion: e.target.value})} />
              </div>
              
              <button type="submit" className="w-full py-3 bg-blue-600 text-white rounded-lg font-bold shadow-lg shadow-blue-600/20 mt-4">
                GUARDAR CAMBIOS
              </button>
            </form>
          </div>
        </div>
      )}

    </div>
  );
}

export default App;