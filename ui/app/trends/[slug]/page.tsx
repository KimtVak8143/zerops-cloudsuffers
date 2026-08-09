import Link from "next/link";

interface TrendPageProps {
  params: {
    slug: string;
  };
}

export default function TrendDetail({ params }: TrendPageProps) {
  return (
    <main className="trend-detail-page">
      <div className="trend-detail-shell">
        <p className="eyebrow">Trend detail</p>
        <h1>{params.slug.replace(/-/g, " ")}</h1>
        <p>This trend page is a placeholder. The AI Radar dashboard is the current demo experience.</p>
        <Link href="/" className="back-link">
          ← Back to AI Radar
        </Link>
      </div>
    </main>
  );
}
