'use client';

import { useState } from 'react';

const jobs = [
  { id: 'CLN-10291', service: '2 BHK Deep Cleaning', area: 'Whitefield', time: '10:00 AM', payout: 2100, distance: '3.2 km' },
  { id: 'CLN-10293', service: 'Kitchen Deep Clean', area: 'Mahadevapura', time: '3:00 PM', payout: 850, distance: '1.8 km' },
];

export default function PartnerPage() {
  const [available, setAvailable] = useState(true);
  const [accepted, setAccepted] = useState<string[]>([]);

  return <>
    <nav className="nav"><div className="brand">CLEANLY PARTNER</div><button className={available ? 'btn' : 'btn secondary'} onClick={() => setAvailable(!available)}>{available ? 'Available' : 'Unavailable'}</button></nav>
    <main className="container">
      <section className="hero"><span className="pill">Partner dashboard</span><h1>Good evening, Demo Partner.</h1><p className="muted">Accept nearby jobs when you choose to work.</p></section>
      <div className="grid grid-3">
        <div className="card"><div className="muted">Today earnings</div><div className="stat">₹1,850</div></div>
        <div className="card"><div className="muted">This month</div><div className="stat">₹31,450</div></div>
        <div className="card"><div className="muted">Rating</div><div className="stat">4.82 ★</div></div>
      </div>
      <section className="card" style={{marginTop:16}}><h2>Nearby jobs</h2>{jobs.map(j => <div className="item" key={j.id}><div><strong>{j.service}</strong><div className="muted">{j.area} · {j.time} · {j.distance}</div></div><div className="row"><strong>₹{j.payout.toLocaleString('en-IN')}</strong><button className="btn" onClick={() => setAccepted(a => a.includes(j.id) ? a : [...a, j.id])}>{accepted.includes(j.id) ? 'Accepted ✓' : 'Accept'}</button></div></div>)}</section>
    </main>
  </>;
}
