'use client';

import { useMemo, useState } from 'react';

const addons = [
  { id: 1, name: 'Kitchen Deep Clean', price: 799 },
  { id: 2, name: 'Sofa Cleaning', price: 699 },
  { id: 3, name: 'Balcony Cleaning', price: 299 },
];

export default function CustomerPage() {
  const [bhk, setBhk] = useState(2);
  const [sqft, setSqft] = useState(1050);
  const [furnished, setFurnished] = useState(true);
  const [selected, setSelected] = useState<number[]>([]);
  const [booked, setBooked] = useState(false);

  const base = bhk === 1 ? 2499 : bhk === 2 ? 3499 : 4499;
  const sizeSurcharge = sqft > 1500 ? 800 : sqft > 1200 ? 300 : 0;
  const furnishedSurcharge = furnished ? 200 : 0;
  const addonTotal = useMemo(() => addons.filter(a => selected.includes(a.id)).reduce((n, a) => n + a.price, 0), [selected]);
  const total = base + sizeSurcharge + furnishedSurcharge + addonTotal;

  return <>
    <nav className="nav"><div className="brand">CLEANLY</div><span className="pill">Bengaluru · MVP</span></nav>
    <main className="container">
      <section className="hero">
        <span className="pill">Professional cleaning, booked in minutes</span>
        <h1>Book a cleaner for your home.</h1>
        <p className="muted">Transparent package pricing, scheduled slots and a managed cleaning team.</p>
      </section>

      <div className="grid grid-2">
        <section className="card">
          <h2>Build your cleaning</h2>
          <div className="field"><label>Property</label><select value={bhk} onChange={e => setBhk(Number(e.target.value))}><option value={1}>1 BHK</option><option value={2}>2 BHK</option><option value={3}>3 BHK</option></select></div>
          <div className="field"><label>Approx. area</label><input type="number" value={sqft} onChange={e => setSqft(Number(e.target.value))} /></div>
          <div className="field"><label>Furnished</label><select value={String(furnished)} onChange={e => setFurnished(e.target.value === 'true')}><option value="true">Yes</option><option value="false">No</option></select></div>
          <div className="field"><label>Add-ons</label>{addons.map(a => <label key={a.id} className="row"><input type="checkbox" checked={selected.includes(a.id)} onChange={() => setSelected(s => s.includes(a.id) ? s.filter(id => id !== a.id) : [...s, a.id])} /> {a.name} <span className="muted">₹{a.price}</span></label>)}</div>
        </section>

        <section className="card">
          <h2>Your quote</h2>
          <div className="list">
            <div className="item"><span>Base deep cleaning</span><strong>₹{base.toLocaleString('en-IN')}</strong></div>
            {sizeSurcharge > 0 && <div className="item"><span>Size adjustment</span><strong>₹{sizeSurcharge.toLocaleString('en-IN')}</strong></div>}
            {furnishedSurcharge > 0 && <div className="item"><span>Furnished adjustment</span><strong>₹{furnishedSurcharge.toLocaleString('en-IN')}</strong></div>}
            <div className="item"><span>Add-ons</span><strong>₹{addonTotal.toLocaleString('en-IN')}</strong></div>
          </div>
          <p className="muted">Estimated crew: 2 partners · Estimated duration: 5.5 hours</p>
          <div className="price">₹{total.toLocaleString('en-IN')}</div>
          <div className="row" style={{marginTop:18}}><button className="btn" onClick={() => setBooked(true)}>{booked ? 'Booking requested ✓' : 'Continue to slot'}</button><button className="btn secondary" onClick={() => setSelected([])}>Reset add-ons</button></div>
        </section>
      </div>
    </main>
  </>;
}
