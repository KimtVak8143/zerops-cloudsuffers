import TrendDashboard from "./components/TrendDashboard";

const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export default async function Home() {
  let trends = [];

  try {
    const response = await fetch(`${apiUrl}/api/v1/trends`, { cache: "no-store" });

    if (!response.ok) {
      console.warn(`Trend API returned ${response.status} ${response.statusText}`);
    } else {
      trends = await response.json();
    }
  } catch (error) {
    console.warn("Failed to load trends from the API", error);
  }

  return (
    <main className="page-shell">
      <div className="page-content">
        <TrendDashboard initialTrends={trends} />
      </div>
    </main>
  );
}
