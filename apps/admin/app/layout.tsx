import type { ReactNode } from 'react';
import './globals.css';

export const metadata = { title: 'Admin | Cleaning Platform', description: 'Cleaning Platform MVP' };

export default function Layout({ children }: { children: ReactNode }) {
  return <html lang="en"><body>{children}</body></html>;
}
