import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'DealMind - AI Real Estate Underwriting',
  description: 'Paste a deal. Get the numbers. Talk to the deal. Decide faster.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
