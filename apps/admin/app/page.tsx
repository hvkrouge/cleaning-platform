'use client';

import { useState } from 'react';

export default function AdminPage() {
  const [assigned, setAssigned] = useState(false);
  return <>
    <nav className="nav"><div className="brand">CLEANLY CONTROL CENTER</div><span className="pill">Operations</span></nav>
    <main className="container">
      <section className="hero"><span className="pill">Live operations</span><h1>Run today's cleaning jobs.</h1><p className="muted">One place for bookings, partners, capacity and exceptions.</p></section>
      <div className="grid grid-3">
        {[['Bookings','37'],['Revenue','₹1.24L'],['Active jobs','9'],['Partners online','46'],['Unassigned','1'],['Complaints','1']].map(([k,v]) => <div className="card" key={k}><div className="muted">{k}</div><div className="stat">{v}</div></div>)}
      </div>
      <div className="grid grid-2" style={{marginTop:16}}>
        <section className="card"><h2>Needs attention</h2><div className="item"><div><strong>CLN-10291</strong><div className="muted">2 BHK Deep Cleaning · 10:00 AM · Whitefield</div></div><button className="btn" onClick={() => setAssigned(true)}>{assigned ? 'Assigned ✓' : 'Assign partner'}</button></div></section>
        <section className="card"><h2>Zone capacity</h2><div className="list"><div className="item"><span>Whitefield</span><strong>82%</strong></div><div className="item"><span>Mahadevapura</span><strong>61%</strong></div><div className="item"><span>Brookefield</span><strong>93%</strong></div><div className="item"><span>Marathahalli</span><strong>47%</strong></div></div></section>
      </div>
    </main>
  </>;
}
