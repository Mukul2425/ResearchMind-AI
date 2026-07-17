import type { Metadata } from "next";
import { IBM_Plex_Serif, Space_Grotesk } from "next/font/google";

import "./globals.css";

const heading = Space_Grotesk({ subsets: ["latin"], variable: "--font-heading" });
const body = IBM_Plex_Serif({ subsets: ["latin"], weight: ["400", "500", "600"], variable: "--font-body" });

export const metadata: Metadata = {
  title: "ResearchMind AI",
  description: "AI-powered research companion",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${heading.variable} ${body.variable}`}>
      <body className="research-grid font-[family-name:var(--font-body)]">{children}</body>
    </html>
  );
}
