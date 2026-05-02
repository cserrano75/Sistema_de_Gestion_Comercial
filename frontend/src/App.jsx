import React, { useState, useEffect } from 'react'
import axios from 'axios'
import SeccionBitacora from './components/SeccionBitacora'

const API_BASE = 'http://127.0.0.1:8000'

function App() {
  // 1. ESTADOS
  const [vistaActual, setVistaActual] = useState('proyectos')
  const [cargando, setCargando] = useState(true)
  const [mostrarModal, setMostrarModal] = useState(false)
  const [proyectos, setProyectos] = useState([])
  const [clientes, setClientes] = useState([])
  
  // Estados para Bitácora
  const [proyectoSeleccionado, setProyectoSeleccionado] = useState(null);
  const [eventosBitacora, setEventosBitacora] = useState([]);
  const [mostrarBitacora, setMostrarBitacora] = useState(false);

  // Estado para Estadísticas (Reportabilidad)
  const [stats, setStats] = useState({
      monto_adjudicado: 0,
      monto_en_estudio: 0,
      monto_perdido: 0,
      tasa_conversion: 0
  });

  const [nuevoCliente, setNuevoCliente] = useState({ rut: '', razon_social: '', giro: '', direccion: '' })
  const [nuevoProyecto, setNuevoProyecto] = useState({ nombre: '', cliente_id: '', presupuesto: 0, estado: 'Lead o Prospecto' })

  // Filtros de estados
  const [filtroEstado, setFiltroEstado] = useState("Todos");
  const estadosFiltro = ["Todos", "Lead o Prospecto", "Estudio", "Cotizado", "Adjudicado", "Perdido", "Anulado o Postergado"];

  const proyectosFiltrados = proyectos.filter(p => 
      filtroEstado === "Todos" ? true : p.estado === filtroEstado
  );

  // 2. FUNCIONES DE CARGA (UNIFICADA)
  const cargarTodo = async () => {
    try {
      setCargando(true)
      
      // Lanzamos todas las peticiones en paralelo para mayor velocidad
      const [resProy, resCli, resStats] = await Promise.all([
        axios.get(`${API_BASE}/proyectos/`),
        axios.get(`${API_BASE}/clientes/`),
        axios.get(`${API_BASE}/proyectos/stats/resumen`)
      ]);

      setProyectos(resProy.data || [])
      setClientes(resCli.data || [])
      setStats(resStats.data || {
          monto_adjudicado: 0,
          monto_en_estudio: 0,
          monto_perdido: 0,
          tasa_conversion: 0
      });

    } catch (e) { 
      console.error("Fallo al cargar datos:", e) 
    } finally { 
      setCargando(false) 
    }
  }

  useEffect(() => { cargarTodo() }, [])

  // 3. LÓGICA DE NEGOCIO
  const guardarCliente = async (e) => {
    e.preventDefault()
    try {
      await axios.post(`${API_BASE}/clientes/`, nuevoCliente)
      setNuevoCliente({ rut: '', razon_social: '', giro: '', direccion: '' })
      setMostrarModal(false)
      cargarTodo()
    } catch (e) { alert("Error al guardar cliente") }
  }

  const manejarGuardarProyecto = async (e) => {
    e.preventDefault()
    if (!nuevoProyecto.cliente_id) return alert("Seleccione cliente")
    try {
      await axios.post(`${API_BASE}/proyectos/`, nuevoProyecto)
      setNuevoProyecto({ nombre: '', cliente_id: '', presupuesto: 0, estado: 'Lead o Prospecto' })
      setMostrarModal(false)
      cargarTodo()
    } catch (e) { alert("Error al guardar proyecto") }
  }

  const abrirBitacora = async (proyecto) => {
    try {
      const res = await axios.get(`${API_BASE}/bitacora/${proyecto.id}`);
      setEventosBitacora(res.data);
      setProyectoSeleccionado(proyecto);
      setMostrarBitacora(true);
    } catch (error) {
      console.error("Error al cargar bitácora:", error);
    }
  };

  const guardarEnBitacora = async (nuevaEntrada) => {
    try {
        await axios.post(`${API_BASE}/bitacora/`, nuevaEntrada);
        // Recargamos todo para actualizar la tabla, los filtros y los KPIs de arriba
        cargarTodo(); 
        setMostrarBitacora(false);
    } catch (error) {
        alert("Error al guardar en bitácora");
    }
  };

  // 4. RENDERIZADO
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
                
                {/* --- NUEVA SECCIÓN DE KPIs --- */}
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
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {clientes.map(c => (
                  <div key={c.id} className="bg-white p-6 rounded-xl shadow border border-slate-100">
                    <div className="text-[10px] font-black text-slate-300 mb-2">{c.rut}</div>
                    <h3 className="font-black text-slate-800 uppercase">{c.razon_social}</h3>
                    <p className="text-xs text-slate-400 mt-1">{c.giro}</p>
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
    </div>
  )
}

export default App