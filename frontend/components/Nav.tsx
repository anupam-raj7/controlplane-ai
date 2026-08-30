"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const LINKS = [
  { href: "/", label: "Overview" },
  { href: "/costs", label: "Cost" },
  { href: "/incidents", label: "Incidents" },
];

export default function Nav() {
  const pathname = usePathname();

  return (
    <nav className="w-56 shrink-0 border-r border-base-700 bg-base-900 px-4 py-6">
      <div className="mb-8 px-2">
        <div className="text-sm font-medium text-base-200">ControlPlane.ai</div>
        <div className="text-xs text-base-400">Risk control layer</div>
      </div>
      <ul className="space-y-1">
        {LINKS.map((link) => {
          const active = pathname === link.href;
          return (
            <li key={link.href}>
              <Link
                href={link.href}
                className={`block rounded-md px-3 py-2 text-sm transition-colors ${
                  active
                    ? "bg-base-700 text-base-200"
                    : "text-base-400 hover:bg-base-800 hover:text-base-200"
                }`}
              >
                {link.label}
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
