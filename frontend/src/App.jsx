import React, { useState, useEffect } from 'react'
import axios from 'axios'

// Configuración base de API para no repetir la URL
const API_BASE = 'http://localhost:8000'

function App() {
  // --- ESTADOS DE NAVEGACIÓN Y CARGA ---
  const [vistaActual, setVistaActual] = useState('proyectos')
  const [cargando, setCargando] = useState(true)
  const [mostrarModal, setMostrarModal] = useState(false)

  // --- ESTADOS DE DATOS (Lo que viene de la BD) ---
  const [proyectos, setProyectos] = useState([])
  const [clientes, setClientes] = useState([])

  // --- ESTADOS DE FORMULARIOS (Lo que el usuario escribe) ---
  const [nuevoCliente, setNuevoCliente] = useState({
    rut: '', razon_social: '', giro: '', direccion: ''
  })
  
  const [nuevoProyecto, setNuevoProyecto] = useState({
    nombre: '', cliente_id: '', presupuesto: 0, estado: 'Cotización'
  })

  // --- EFECTOS ---
  useEffect(() => {
    cargarTodo()
  }, [])

  // --- FUNCIONES DE LÓGICA (API) ---
  const cargarTodo = async () => {
    setCargando(true)
    try {
      const [resProy, resCli] = await Promise.all([
        axios.get(`${API_BASE}/proyectos/`),
        axios.get(`${API_BASE}/clientes/`)
      ])
      setProyectos(resProy.data)
      setClientes(resCli.data)
    } catch (e) {
      console.error("Error al sincronizar con PostgreSQL", e)
    } finally {
      setCargando(false)
    }
  }

  const guardarCliente = async (e) => {
    e.preventDefault()
    try {
      await axios.post(`${API_BASE}/clientes/`, nuevoCliente)
      setNuevoCliente({ rut: '', razon_social: '', giro: '', direccion: '' })
      setMostrarModal(false)
      cargarTodo()
    } catch (e) {
      alert("Error: El RUT ya existe o los datos son inválidos.")
    }
  }

  const manejarGuardarProyecto = async (e) => {
    e.preventDefault()
    // Validación básica: que el ID no sea un string vacío
    if (!nuevoProyecto.cliente_id) {
      alert("Por favor, seleccione un cliente del maestro.")
      return
    }

    try {
      await axios.post(`${API_BASE}/proyectos/`, nuevoProyecto)
      setNuevoProyecto({ nombre: '', cliente_id: '', presupuesto: 0, estado: 'Cotización' })
      setMostrarModal(false)
      cargarTodo()
    } catch (e) {
      alert("Error al vincular el proyecto. Revise la conexión con el servidor.")
    }
  }

  // --- RENDERIZADO ---
  return (
    <div className="flex h-screen bg-slate-50 font-sans text-slate-900">
      
      {/* SIDEBAR */}
      <aside className="w-64 bg-slate-900 text-white flex flex-col shadow-2xl">
        <div className="p-8 text-2xl font-black border-b border-slate-800 tracking-tighter italic">
          CRM <span className="text-blue-500">IND.</span>
        </div>
        <nav className="flex-1 p-4 space-y-2 mt-4">
          <button 
            onClick={() => { setVistaActual('proyectos'); setMostrarModal(false); }}
            className={`w-full text-left p-4 rounded-2xl transition-all font-bold text-sm ${vistaActual === 'proyectos' ? 'bg-blue-600 shadow-lg' : 'hover:bg-slate-800 text-slate-400'}`}
          >
            📊 DASHBOARD PROYECTOS
          </button>
          <button 
            onClick={() => { setVistaActual('clientes'); setMostrarModal(false); }}
            className={`w-full text-left p-4 rounded-2xl transition-all font-bold text-sm ${vistaActual === 'clientes' ? 'bg-blue-600 shadow-lg' : 'hover:bg-slate-800 text-slate-400'}`}
          >
            🏢 MAESTRO CLIENTES
          </button>
        </nav>
        <div className="p-6 border-t border-slate-800 text-[10px] text-slate-500 text-center font-black">
          Claudio Serrano • v1.2
        </div>
      </aside>

      {/* CONTENIDO PRINCIPAL */}
      <main className="flex-1 flex flex-col overflow-hidden">
        <header className="h-20 bg-white border-b border-slate-200 flex items-center justify-between px-10">
          <h2 className="text-2xl font-black text-slate-800 uppercase italic">
            {vistaActual === 'proyectos' ? 'Gestión de Proyectos' : 'Maestro de Clientes'}
          </h2>
          <button 
            onClick={() => setMostrarModal(true)}
            className="bg-slate-900 text-white px-6 py-3 rounded-2xl hover:bg-blue-600 transition-all font-bold text-[10px] tracking-widest shadow-xl"
          >
            + AGREGAR {vistaActual === 'proyectos' ? 'PROYECTO' : 'CLIENTE'}
          </button>
        </header>

        <section className="p-10 overflow-y-auto">
          {cargando ? (
            <div className="flex flex-col items-center justify-center h-64 text-slate-400 font-bold">
               <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600 mb-4"></div>
               Sincronizando...
            </div>
          ) : (
            <>
              {vistaActual === 'proyectos' ? (
                /* TABLA DE PROYECTOS */
                <div className="bg-white rounded-[2.5rem] shadow-sm border border-slate-100 overflow-hidden">
                  <table className="w-full text-left">
                    <thead className="bg-slate-50/50">
                      <tr className="text-slate-400 text-[10px] uppercase font-black tracking-widest">
                        <th className="p-6">Proyecto</th>
                        <th className="p-6">ID Cliente</th>
                        <th className="p-6">Presupuesto</th>
                        <th className="p-6">Estado</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-50">
                      {proyectos.map(p => (
                        <tr key={p.id} className="hover:bg-slate-50/30 transition-colors">
                          <td className="p-6 font-bold text-slate-700">{p.nombre}</td>
                          <td className="p-6 text-slate-400 font-mono text-xs">#{p.cliente_id}</td>
                          <td className="p-6 font-mono font-bold text-blue-600">${p.presupuesto.toLocaleString('es-CL')}</td>
                          <td className="p-6">
                            <span className="bg-blue-50 text-blue-700 px-3 py-1 rounded-full text-[10px] font-black uppercase">{p.estado}</span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                /* GRILLA DE CLIENTES */
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {clientes.map(c => (
                    <div key={c.id} className="bg-white p-8 rounded-[2rem] shadow-sm border border-slate-100 hover:shadow-xl transition-all group">
                      <div className="flex justify-between items-start mb-4">
                        <div className="bg-slate-900 text-white p-3 rounded-2xl group-hover:bg-blue-600 transition-colors italic font-bold">Cli</div>
                        <span className="text-[10px] font-black text-slate-300 tracking-widest">{c.rut}</span>
                      </div>
                      <h3 className="text-lg font-black text-slate-800 leading-tight mb-2 uppercase">{c.razon_social}</h3>
                      <p className="text-sm text-slate-400 font-medium">{c.giro || 'Industrial'}</p>
                    </div>
                  ))}
                </div>
              )}
            </>
          )}
        </section>
      </main>

      {/* --- MODALES --- */}

      {/* MODAL CLIENTE */}
      {mostrarModal && vistaActual === 'clientes' && (
        <div className="fixed inset-0 bg-slate-900/80 backdrop-blur-md flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-[2.5rem] shadow-2xl w-full max-w-md p-10 relative border border-white/20">
            <button onClick={() => setMostrarModal(false)} className="absolute top-8 right-8 text-slate-300 hover:text-red-500 font-bold">✕</button>
            <h2 className="text-3xl font-black text-slate-800 mb-8 italic">Nuevo Cliente</h2>
            <form onSubmit={guardarCliente} className="space-y-4">
              <input required type="text" placeholder="RUT Empresa" className="w-full p-4 bg-slate-50 rounded-2xl outline-none font-bold" value={nuevoCliente.rut} onChange={(e) => setNuevoCliente({...nuevoCliente, rut: e.target.value})}/>
              <input required type="text" placeholder="Razón Social" className="w-full p-4 bg-slate-50 rounded-2xl outline-none font-bold" value={nuevoCliente.razon_social} onChange={(e) => setNuevoCliente({...nuevoCliente, razon_social: e.target.value})}/>
              <input type="text" placeholder="Giro" className="w-full p-4 bg-slate-50 rounded-2xl outline-none font-bold" value={nuevoCliente.giro} onChange={(e) => setNuevoCliente({...nuevoCliente, giro: e.target.value})}/>
              <button type="submit" className="w-full py-5 bg-blue-600 text-white rounded-2xl text-xs font-black tracking-widest shadow-xl uppercase">Registrar en Maestro</button>
            </form>
          </div>
        </div>
      )}

      {/* MODAL PROYECTO */}
      {mostrarModal && vistaActual === 'proyectos' && (
        <div className="fixed inset-0 bg-slate-900/80 backdrop-blur-md flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-[2.5rem] shadow-2xl w-full max-w-md p-10 relative border border-white/20">
            <button onClick={() => setMostrarModal(false)} className="absolute top-8 right-8 text-slate-300 hover:text-red-500 font-bold">✕</button>
            <h2 className="text-3xl font-black text-slate-800 mb-8 italic">Nuevo Proyecto</h2>
            <form onSubmit={manejarGuardarProyecto} className="space-y-4">
              <input required type="text" placeholder="Nombre del Proyecto" className="w-full p-4 bg-slate-50 rounded-2xl outline-none font-bold" value={nuevoProyecto.nombre} onChange={(e) => setNuevoProyecto({...nuevoProyecto, nombre: e.target.value})}/>
              
              <select 
                required 
                className="w-full p-4 bg-slate-50 rounded-2xl outline-none font-bold text-slate-700"
                value={nuevoProyecto.cliente_id}
                onChange={(e) => setNuevoProyecto({...nuevoProyecto, cliente_id: e.target.value})}
              >
                <option value="">-- Seleccione Cliente --</option>
                {clientes.map(c => (
                  <option key={c.id} value={c.id}>{c.razon_social}</option>
                ))}
              </select>

              <input required type="number" placeholder="Presupuesto" className="w-full p-4 bg-slate-50 rounded-2xl outline-none font-mono font-bold" value={nuevoProyecto.presupuesto} onChange={(e) => setNuevoProyecto({...nuevoProyecto, presupuesto: parseFloat(e.target.value)})}/>
              
              <button type="submit" className="w-full py-5 bg-blue-600 text-white rounded-2xl text-xs font-black tracking-widest shadow-xl uppercase">Vincular y Guardar</button>
            </form>
          </div>
        </div>
      )}

    </div>
  )
}

export default App