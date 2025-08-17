"use client";
import { useEffect, useState } from "react";
import api from "@/utils/api";
import UploadModal from "@/components/UploadModal";

interface TableStats {
  total: number;
  reviewed: number;
  unreviewed: number;
}

export default function BaselineAutomation() {
  const [isUploadOpen, setUploadOpen] = useState(false);
  const [tables, setTables] = useState<string[]>([]);
  const [stats, setStats] = useState<Record<string, TableStats>>({});
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchTablesAndStats();
  }, []);

  const fetchTablesAndStats = async () => {
    try {
      setLoading(true);
      const res = await api.get("/data_viewer/cis/tables");
      const tableNames: string[] = res.data;

      setTables(tableNames);

      // fetch stats for each table
      const statsObj: Record<string, TableStats> = {};
      for (const t of tableNames) {
        const s = await api.get(`/data_viewer/cis/${t}/stats`);
        statsObj[t] = s.data;
      }
      setStats(statsObj);
    } catch (err) {
      console.error("Failed to fetch CIS tables:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleHarden = async (table: string) => {
    try {
      await api.post("/baseline/harden", null, { params: { table_name: table } });
      pollProgress(table);
    } catch (err) {
      console.error("Error starting hardening:", err);
    }
  };

  const pollProgress = (table: string) => {
    const interval = setInterval(async () => {
      try {
        const res = await api.get(`/baseline/progress/${table}`);
        const p = res.data;

        setStats((prev) => ({
          ...prev,
          [table]: {
            total: p.total,
            reviewed: p.done,
            unreviewed: p.total - p.done,
          },
        }));

        if (p.status === "complete") {
          clearInterval(interval);
        }
      } catch (err) {
        console.error("Error polling progress:", err);
        clearInterval(interval);
      }
    }, 1000);
  };

  return (
    <div className="p-6">
      {/* Upload trigger */}
      <div className="flex justify-end mb-4">
        <button className="btn btn-outline btn-primary" onClick={() => setUploadOpen(true)}>
          Upload a benchmark
        </button>
      </div>

      <h2 className="text-2xl font-bold mb-6">CIS Baseline Automation</h2>

      {/* Upload modal */}
      <UploadModal isOpen={isUploadOpen} onClose={() => setUploadOpen(false)} />

      {/* Show CIS table cards */}
      {loading && <p>Loading tables…</p>}
      <div className="grid gap-4">
        {tables.map((t) => {
          const s = stats[t];
          const pct = s ? Math.round((s.reviewed / s.total) * 100) : 0;
          return (
            <div key={t} className="card bg-base-100 shadow-md p-4">
              <h3 className="font-semibold text-lg mb-2">{t}</h3>
              {s && (
                <>
                  <progress className="progress progress-primary w-full" value={s.reviewed} max={s.total}></progress>
                  <div className="text-sm mt-2 flex justify-between">
                    <span>{pct}% reviewed</span>
                    <span>
                      {s.unreviewed} unreviewed / {s.total} total
                    </span>
                  </div>
                  <div className="mt-3">
                    <button className="btn btn-sm btn-accent" onClick={() => handleHarden(t)}>
                      Harden
                    </button>
                  </div>
                </>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
