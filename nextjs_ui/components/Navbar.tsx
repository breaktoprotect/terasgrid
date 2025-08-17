"use client";
import { useEffect, useState } from "react";

export default function Navbar() {
  const [theme, setTheme] = useState("dim"); // default = dark

  // On mount: load theme from localStorage or fallback to "dim"
  useEffect(() => {
    const stored = localStorage.getItem("theme");
    const initial = stored || "dim";
    setTheme(initial);
    document.documentElement.setAttribute("data-theme", initial);
  }, []);

  // Whenever theme changes: update <html> and save to localStorage
  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(theme === "lofi" ? "dim" : "lofi");
  };

  return (
    <div className="navbar bg-base-300 shadow-md">
      <div className="navbar-start">
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
