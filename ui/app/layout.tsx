import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AI Radar",
  description: "Discover what's changing in AI.",
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
