"use client";
import { useEffect, useState } from "react";

export default function Navbar() {
  const [theme, setTheme] = useState<"dim" | "lofi">("dim"); // consistent SSR default
  const [mounted, setMounted] = useState(false);

  // only run after hydration
  useEffect(() => {
    setMounted(true);
    const stored = localStorage.getItem("theme") as "dim" | "lofi" | null;
    const initial = stored || "dim";
    setTheme(initial);
    document.documentElement.setAttribute("data-theme", initial);
  }, []);

  useEffect(() => {
    if (mounted) {
      document.documentElement.setAttribute("data-theme", theme);
      localStorage.setItem("theme", theme);
    }
  }, [theme, mounted]);

  const toggleTheme = () => {
    setTheme(theme === "lofi" ? "dim" : "lofi");
  };

  // 🚨 prevent hydration mismatch: render nothing until client mounts
  if (!mounted) {
    return null;
  }

  return (
    <div className="navbar bg-base-300 shadow-md">
      <div className="navbar-start flex items-center gap-2">
        {/* Logo + Title */}
        <img src="/logo.png" alt="TerasGrid Logo" className="h-10 w-auto" />
        <a className="btn btn-ghost normal-case text-xl">TerasGrid UI</a>
      </div>

      <div className="navbar-center">
        <ul className="menu menu-horizontal px-1 gap-x-4">
          <li>
            <a href="/">Dashboard</a>
          </li>
          <li>
            <a href="/setup">Setup</a>
          </li>
          <li>
            <a href="/dataViewer">Data Viewer</a>
          </li>
          <li>
            <a href="/baselineAutomation">Baseline Automation</a>
          </li>
        </ul>
      </div>

      <div className="navbar-end">
        <button onClick={toggleTheme} className="btn btn-sm btn-outline">
          {theme === "lofi" ? "🌙 Dark" : "☀️ Light"}
        </button>
      </div>
    </div>
  );
}
