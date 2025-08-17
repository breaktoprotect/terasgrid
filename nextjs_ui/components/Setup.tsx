"use client";

import { useState } from "react";
import api from "@/utils/api";

export default function Setup() {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const handleResetAndIngest = async () => {
    setLoading(true);
    setMessage(null);

    try {
      // ✅ remove /api/v1 here, since it's already in lib/api.ts
      const response = await api.post("/setup/reset-and-ingest");
      setMessage(response.data.message || "Reset and ingest completed.");
    } catch (error: any) {
      console.error("Error:", error);
      setMessage(error.response?.data?.detail || "Failed to reset and ingest database.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 bg-base-100 rounded-lg shadow-md">
      <h2 className="text-xl font-bold mb-2">Baseline Automation Setup</h2>
      <p className="mb-4">Reset the database and ingest the baseline configs from CSV (POC).</p>
      <button className="btn btn-primary" onClick={handleResetAndIngest} disabled={loading}>
        {loading ? "Processing..." : "Reset & Ingest"}
      </button>
      {message && <p className="mt-4 text-sm text-info whitespace-pre-wrap">{message}</p>}
    </div>
  );
}
