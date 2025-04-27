// app/layout.tsx
import Link from 'next/link';
import { AuthProvider } from '@/context/AuthContext';
import '@/app/globals.css';


export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          <header className="p-4 bg-white shadow-sm">
            <nav className="max-w-3xl mx-auto flex justify-between">
              <Link href="/" className="font-bold text-xl">SmartClaim AI</Link>
              <div className="space-x-4">
                <Link href="/login">Login</Link>
                <Link href="/register">Register</Link>
              </div>
            </nav>
          </header>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
