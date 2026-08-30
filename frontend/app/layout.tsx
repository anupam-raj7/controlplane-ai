import type { Metadata } from "next";
import "./globals.css";
import Nav from "@/components/Nav";

export const metadata: Metadata = {
  title: "ControlPlane.ai",
  description: "A model-agnostic control layer for enterprise AI.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="flex min-h-screen">
        <Nav />
        <main className="flex-1 px-8 py-8">{children}</main>
      </body>
    </html>
  );
}
