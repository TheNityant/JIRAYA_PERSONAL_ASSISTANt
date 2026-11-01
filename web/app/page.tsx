import AccountGate from "@/components/AccountGate";
import Link from "next/link";

export default function Home() {
  return <><AccountGate /><footer className="public-site-footer">
    <div><strong>Jiraya Personal Assistant</strong><p>Connect Gmail, Google Calendar and GitHub to automate personal workflows with AI interpretation and outcome tracking. Optional local tools support Git checkpoints and Meet attendance.</p></div>
    <nav aria-label="Public information"><Link href="/privacy">Privacy Policy</Link><Link href="/terms">Terms of Service</Link><a href="mailto:nityant.tiwari2404@gmail.com">Contact support</a></nav>
  </footer></>;
}
