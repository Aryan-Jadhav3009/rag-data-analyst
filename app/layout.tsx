import type { Metadata } from 'next'
import './globals.css'
export const metadata: Metadata = { title: 'QueryIQ — Ask your data anything', description: 'A glassy AI data analyst workspace.' }
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en" className="bg-[#080b16]"><body>{children}</body></html>}
