"use client";
import { useState } from "react";
import api from "@/utils/api";

interface UploadModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function UploadModal({ isOpen, onClose }: UploadModalProps) {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    setMessage(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("start_page", "36");

    try {
      const res = await api.post("/baseline/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setMessage("✅ Upload successful: " + res.data.message);
    } catch (err: any) {
      setMessage("❌ Upload failed: " + (err.response?.data?.detail || err.message));
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className={`modal ${isOpen ? "modal-open" : ""}`} onClick={onClose}>
      <div className="modal-box max-w-xl" onClick={(e) => e.stopPropagation()}>
        {/* DaisyUI ✕ button */}
        <button onClick={onClose} className="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">
          ✕
        </button>

        <h3 className="font-bold text-lg mb-4">Upload CIS Benchmark PDF</h3>

        <input
          type="file"
          accept="application/pdf"
          className="file-input file-input-bordered w-full mb-4"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          disabled={uploading}
        />

        {uploading && (
          <div className="my-4">
            <progress className="progress w-full"></progress>
            <p className="mt-2 text-sm text-gray-500">Extracting benchmark… please wait</p>
          </div>
        )}

        <div className="flex justify-end gap-2">
          <button className="btn" onClick={onClose} disabled={uploading}>
            Cancel
          </button>
          <button onClick={handleUpload} disabled={!file || uploading} className="btn btn-primary">
            {uploading ? <span className="loading loading-spinner"></span> : "Upload"}
          </button>
        </div>

        {message && <p className="mt-4 text-sm">{message}</p>}
      </div>
    </div>
  );
}
