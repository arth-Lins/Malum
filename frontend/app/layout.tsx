import type { Metadata } from 'next';
import './globals.css';
export const metadata: Metadata = { title: 'Malum — eficiência visível', description: 'Descubra desperdícios em sua produção.' };
export default function RootLayout({ children }: Readonly<{children: React.ReactNode}>) { return <html lang="pt-BR"><body>{children}</body></html>; }
