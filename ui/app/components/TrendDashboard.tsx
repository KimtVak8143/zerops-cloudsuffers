"use client";

import Link from "next/link";
import { useMemo, useState } from "react";

export interface Trend {
  id: number;
  name: string;
  slug: string;
  category: string;
  status: string;
  tldr: string;
  why_it_matters: string;
  momentum: string;
  tech_stack: string[];
  related_trends: string[];
}

const categories = [
  "All",
  "Protocols",
  "Agents",
  "Agent Infrastructure",
  "Developer AI",
  "Models",
  "Context",
  "Security",
  "AI Infrastructure",
];

function momentumValue(momentum: string | undefined) {
  const value = Number(momentum ?? 0);
  return Number.isFinite(value) ? Math.min(100, Math.max(0, value)) : 0;
}

function highlightPriority(trend: Trend) {
  if (trend.slug === "model-context-protocol") return -1000;
  if (trend.slug === "agent2agent") return -900;
  if (trend.slug === "agentic-ai") return -800;
  return 0;
}

function TrendCard({ trend }: { trend: Trend }) {
  const momentum = momentumValue(trend.momentum);
  const related = trend.related_trends?.slice(0, 3) ?? [];

  return (
    <Link href={`/trends/${trend.slug}`} className="trend-card">
      <div className="trend-card-header">
        <span className="trend-badge">{trend.category}</span>
        <span className="trend-status">{trend.status}</span>
      </div>
      <div className="trend-card-body">
        <h3>{trend.name}</h3>
        <p>{trend.tldr}</p>
      </div>
      <div className="trend-card-meta">
        <div className="momentum-row">
          <span>Momentum</span>
          <span>{momentum}</span>
        </div>
        <div className="momentum-bar">
          <div className="momentum-fill" style={{ width: `${momentum}%` }} />
        </div>
        <div className="trend-hint">
          <span>{trend.tech_stack?.slice(0, 3).join(" • ")}</span>
          <span>•</span>
          <span>{related.length > 0 ? related.join(" • ") : "No related tags"}</span>
        </div>
      </div>
    </Link>
  );
}

export default function TrendDashboard({ initialTrends }: { initialTrends: Trend[] }) {
  const [search, setSearch] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("All");

  const trends = useMemo(
    () =>
      initialTrends.map((trend) => ({
        ...trend,
        momentumValue: momentumValue(trend.momentum),
      })),
    [initialTrends]
  );

  const filteredTrends = useMemo(() => {
    const term = search.trim().toLowerCase();
    return trends.filter((trend) => {
      const matchesCategory = selectedCategory === "All" || trend.category === selectedCategory;
      const matchesSearch =
        !term ||
        [trend.name, trend.tldr, trend.why_it_matters, trend.category]
          .filter(Boolean)
          .some((value) => value.toLowerCase().includes(term)) ||
        trend.related_trends?.some((value) => value.toLowerCase().includes(term));
      return matchesCategory && matchesSearch;
    });
  }, [selectedCategory, search, trends]);

  const activeTrends = trends.length;
  const categoriesCount = useMemo(
    () => new Set(trends.map((trend) => trend.category)).size,
    [trends]
  );
  const highMomentumCount = trends.filter((trend) => trend.momentumValue >= 80).length;

  const highMomentumTrends = useMemo(
    () =>
      [...trends]
        .sort((a, b) => {
          const pa = highlightPriority(a);
          const pb = highlightPriority(b);
          if (pa !== pb) return pa - pb;
          return b.momentumValue - a.momentumValue;
        })
        .filter((trend) => trend.momentumValue >= 80)
        .slice(0, 4),
    [trends]
  );

  const emergingTrends = useMemo(
    () =>
      trends
        .filter((trend) => trend.status === "Emerging")
        .sort((a, b) => b.momentumValue - a.momentumValue)
        .slice(0, 4),
    [trends]
  );

  return (
    <div className="dashboard-root">
      <section className="hero-panel">
        <div className="hero-copy">
          <p className="eyebrow">AI Radar</p>
          <h1>Discover what’s changing in AI.</h1>
          <p>
            Explore emerging protocols, agent architectures, model capabilities and
            infrastructure shaping the next generation of AI.
          </p>
        </div>
        <div className="hero-stats">
          <div className="stat-card">
            <span className="stat-number">{activeTrends}</span>
            <span className="stat-label">Active Trends</span>
          </div>
          <div className="stat-card">
            <span className="stat-number">{categoriesCount}</span>
            <span className="stat-label">Categories</span>
          </div>
          <div className="stat-card stat-highlight">
            <span className="stat-icon">🔥</span>
            <span className="stat-number">{highMomentumCount}</span>
            <span className="stat-label">High Momentum</span>
          </div>
        </div>
      </section>

      <section className="controls-panel">
        <div className="search-field">
          <label htmlFor="trend-search" className="sr-only">
            Search AI trends
          </label>
          <input
            id="trend-search"
            type="search"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="Search AI trends..."
          />
        </div>

        <div className="filter-strip" role="toolbar" aria-label="Trend categories">
          {categories.map((category) => (
            <button
              key={category}
              type="button"
              className={category === selectedCategory ? "filter-button active" : "filter-button"}
              onClick={() => setSelectedCategory(category)}
            >
              {category}
            </button>
          ))}
        </div>
      </section>

      <section className="trend-section">
        <div className="section-header">
          <h2>🔥 High Momentum</h2>
          <p>Flagship protocol and agent trends driving technical adoption.</p>
        </div>
        <div className="trend-grid">
          {highMomentumTrends.map((trend) => (
            <TrendCard key={trend.slug} trend={trend} />
          ))}
        </div>
      </section>

      <section className="trend-section">
        <div className="section-header">
          <h2>🌱 Emerging</h2>
          <p>New signal areas for context, reasoning, and agent infrastructure.</p>
        </div>
        <div className="trend-grid">
          {emergingTrends.map((trend) => (
            <TrendCard key={trend.slug} trend={trend} />
          ))}
        </div>
      </section>

      <section className="trend-section">
        <div className="section-header">
          <h2>Explore the ecosystem</h2>
          <p>Filter the full AI Radar by category and technical focus.</p>
        </div>
        <div className="trend-grid">
          {filteredTrends.length > 0 ? (
            filteredTrends.map((trend) => <TrendCard key={trend.slug} trend={trend} />)
          ) : (
            <div className="empty-state">
              <p>No trends match your search. Try a broader query or switch category.</p>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
