import type { Metadata } from "next";
import "@xyflow/react/dist/style.css";
import "./globals.css";

export const metadata: Metadata = {
  title: "Jiraya · Automation Builder",
  description: "User-configurable personal AI automations",
  verification: {
    google: "XgPI9z9r58QUxOp-Oyy4TGBqI9U8220RXheeaVdmvt0",
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
