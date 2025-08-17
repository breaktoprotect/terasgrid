export default function Dashboard() {
  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Dashboard</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Stats */}
        <div className="stats shadow">
          <div className="stat">
            <div className="stat-title">Total Configs</div>
            <div className="stat-value">123</div>
            <div className="stat-desc">In Core DB</div>
          </div>
          <div className="stat">
            <div className="stat-title">Pending</div>
            <div className="stat-value">15</div>
            <div className="stat-desc">Awaiting Review</div>
          </div>
        </div>

        {/* Chart placeholders */}
        <div className="card bg-base-100 shadow-md p-6">
          <h3 className="font-semibold mb-2">Radar Chart</h3>
          <div className="h-48 flex items-center justify-center text-gray-400">
            [Radar Chart Placeholder]
          </div>
        </div>
        <div className="card bg-base-100 shadow-md p-6">
          <h3 className="font-semibold mb-2">Heatmap</h3>
          <div className="h-48 flex items-center justify-center text-gray-400">
            [Heatmap Placeholder]
          </div>
        </div>
      </div>
    </div>
  );
}
