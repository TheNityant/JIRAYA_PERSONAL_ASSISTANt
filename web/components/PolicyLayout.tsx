import Link from "next/link";
import type { ReactNode } from "react";

export default function PolicyLayout({title, children}: {title: string; children: ReactNode}) {
  return <main className="policy-shell">
    <nav aria-label="Policy navigation"><Link href="/">← Jiraya Personal Assistant</Link><div><Link href="/privacy">Privacy</Link><Link href="/terms">Terms</Link></div></nav>
    <article><span className="eyebrow">Jiraya · Public information</span><h1>{title}</h1>
      <p className="policy-updated">Last updated: 1 November 2026</p>{children}
    </article>
    <footer>Questions? <a href="mailto:nityant.tiwari2404@gmail.com">nityant.tiwari2404@gmail.com</a></footer>
  </main>;
}
