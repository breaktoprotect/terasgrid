"use client";

import { useEffect, useState } from "react";
import api from "@/utils/api";
import React from "react";

interface CoreConfig {
  config_id: string;
  status: string;
  config_name: string;
  config_desc: string;
  os_version_applicability?: string;
  role_applicability?: string;
  [key: string]: any;
}

interface CisRecord {
  number: string;
  reviewed: number;
  title: string;
  profile_applicability: string;
  description: string;
  [key: string]: any;
}

export default function DataViewer() {
  const [activeTab, setActiveTab] = useState<"core" | string>("core");
  const [coreConfigs, setCoreConfigs] = useState<CoreConfig[]>([]);
  const [cisTables, setCisTables] = useState<string[]>([]);
  const [cisData, setCisData] = useState<CisRecord[]>([]);
  const [loading, setLoading] = useState(false);
  const [expandedRow, setExpandedRow] = useState<string | null>(null);

  const toggleExpand = (rowKey: string) => {
    setExpandedRow((prev) => (prev === rowKey ? null : rowKey));
  };

  // Load core configs
  useEffect(() => {
    if (activeTab === "core") {
      setLoading(true);
      api
        .get("/data_viewer/core")
        .then((res) => setCoreConfigs(res.data))
        .finally(() => setLoading(false));
    }
  }, [activeTab]);

  // Load CIS tables list once
  useEffect(() => {
    api.get("/data_viewer/cis/tables").then((res) => setCisTables(res.data));
  }, []);

  // Load CIS table when activeTab is a cis table
  useEffect(() => {
    if (activeTab !== "core" && cisTables.includes(activeTab)) {
      setLoading(true);
      api
        .get(`/data_viewer/cis/${activeTab}`)
        .then((res) => setCisData(res.data))
        .finally(() => setLoading(false));
    }
  }, [activeTab, cisTables]);

  return (
    <div className="bg-base-100 p-4 rounded-lg shadow-md">
      {/* Navigation Tabs using DaisyUI radio style */}
      <div className="tabs tabs-box mb-4">
        <input
          type="radio"
          name="data_tabs"
          role="tab"
          className="tab"
          aria-label="Core Configs"
          checked={activeTab === "core"}
          onChange={() => setActiveTab("core")}
        />

        {cisTables.map((tbl) => (
          <input
            key={tbl}
            type="radio"
            name="data_tabs"
            role="tab"
            className="tab"
            aria-label={tbl}
            checked={activeTab === tbl}
            onChange={() => setActiveTab(tbl)}
          />
        ))}
      </div>

      {/* Table Display */}
      {loading ? (
        <p>Loading...</p>
      ) : activeTab === "core" ? (
        <table className="table table-zebra w-full">
          <thead>
            <tr>
              <th>ID</th>
              <th>Status</th>
              <th>Name</th>
              <th>Description</th>
              <th>OS Version</th>
              <th>Role</th>
            </tr>
          </thead>
          <tbody>
            {coreConfigs.map((row) => (
              <React.Fragment key={row.config_id}>
                <tr className="cursor-pointer hover:bg-base-200" onClick={() => toggleExpand(row.config_id)}>
                  <td>{row.config_id}</td>
                  <td>{row.status}</td>
                  <td>{row.config_name}</td>
                  <td>{row.config_desc}</td>
                  <td>{row.os_version_applicability || "-"}</td>
                  <td>{row.role_applicability || "-"}</td>
                </tr>
                {expandedRow === row.config_id && (
                  <tr>
                    <td colSpan={6}>
                      <div className="collapse collapse-open bg-base-200">
                        <div className="collapse-title font-bold">Full Details</div>
                        <div className="collapse-content">
                          {Object.entries(row).map(([k, v]) => (
                            <p key={k}>
                              <strong>{k}: </strong>
                              {String(v)}
                            </p>
                          ))}
                        </div>
                      </div>
                    </td>
                  </tr>
                )}
              </React.Fragment>
            ))}
          </tbody>
        </table>
      ) : (
        <table className="table table-zebra w-full">
          <thead>
            <tr>
              <th>Number</th>
              <th>Reviewed</th>
              <th>Title</th>
              <th>Profile</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            {cisData.map((row) => (
              <React.Fragment key={row.number}>
                <tr className="cursor-pointer hover:bg-base-200" onClick={() => toggleExpand(row.number)}>
                  <td>{row.number}</td>
                  <td>{row.reviewed ? "✅" : "❌"}</td>
                  <td>{row.title}</td>
                  <td>{row.profile_applicability}</td>
                  <td>{row.description}</td>
                </tr>
                {expandedRow === row.number && (
                  <tr>
                    <td colSpan={5}>
                      <div className="collapse collapse-open bg-base-200">
                        <div className="collapse-title font-bold">Full Details</div>
                        <div className="collapse-content">
                          {Object.entries(row).map(([k, v]) => (
                            <p key={k}>
                              <strong>{k}: </strong>
                              {String(v)}
                            </p>
                          ))}
                        </div>
                      </div>
                    </td>
                  </tr>
                )}
              </React.Fragment>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
