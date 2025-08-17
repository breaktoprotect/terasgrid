"use client";
import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";

export default function Navbar() {
  const [theme, setTheme] = useState<"dim" | "lofi">("dim");
  const [mounted, setMounted] = useState(false);
  const pathname = usePathname();

  // Ensure component only renders after client mount
  useEffect(() => {
    setMounted(true);
    const stored = localStorage.getItem("theme") as "dim" | "lofi" | null;
    const initial = stored || "dim";
    setTheme(initial);
    document.documentElement.setAttribute("data-theme", initial);
  }, []);

  useEffect(() => {
    if (!mounted) return;
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }, [theme, mounted]);

  const toggleTheme = () => {
    setTheme(theme === "lofi" ? "dim" : "lofi");
  };

  // 🚨 Prevent hydration mismatch by not rendering until mounted
  if (!mounted) return null;

  return (
    <div className="navbar bg-base-300 shadow-md">
      <div className="navbar-start flex items-center gap-2">
        <img src="/logo.png" alt="TerasGrid Logo" className="h-10 w-auto" />
        <span className="text-xl font-bold">TerasGrid UI</span>
      </div>

      <div className="navbar-center">
        <ul className="menu menu-horizontal px-1 gap-x-4">
          <li>
            <a href="/" className={pathname === "/" ? "active font-semibold" : ""}>
              Dashboard
            </a>
          </li>
          <li>
            <a href="/setup" className={pathname === "/setup" ? "active font-semibold" : ""}>
              Setup
            </a>
          </li>
          <li>
            <a href="/dataViewer" className={pathname === "/dataViewer" ? "active font-semibold" : ""}>
              Data Viewer
            </a>
          </li>
          <li>
            <a href="/baselineAutomation" className={pathname === "/baselineAutomation" ? "active font-semibold" : ""}>
              Baseline Automation
            </a>
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
