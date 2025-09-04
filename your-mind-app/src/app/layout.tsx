import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "your-mind-app",
  description: "Framer Motion + Mask Player",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <body className="antialiased min-h-screen bg-slate-950 text-slate-100">
        {children}
      </body>
    </html>
  );
}
