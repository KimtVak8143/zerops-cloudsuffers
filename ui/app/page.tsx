import TrendDashboard from "./components/TrendDashboard";

const apiUrl = process.env.NEXT_PUBLIC_API_URL;

export default async function Home() {
  const trends = apiUrl
    ? await fetch(`${apiUrl}/api/v1/trends`, { cache: "no-store" }).then((res) => {
        if (!res.ok) throw new Error("Failed to load trends from the API");
        return res.json();
      })
    : [];

  return (
    <main className="page-shell">
      <div className="page-content">
        <TrendDashboard initialTrends={trends} />
      </div>
    </main>
  );
}
