"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import TechStackMap from "./TechStackMap";

interface TrendSource {
  id: number;
  title: string;
  url: string;
  source_type: string | null;
}

export interface TechStackLayer {
  name: string;
  items: string[];
}

interface TrendDetail {
  id: number;
  name: string;
  slug: string;
  category: string | null;
  status: string | null;
  tldr: string | null;
  why_it_matters: string | null;
  momentum: string | null;
  tech_stack: string[] | { layers: TechStackLayer[] } | null;
  related_trends: string[] | null;
  sources: TrendSource[];
}

interface TrendDetailClientProps {
  slug: string;
}

const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

function formatSourceType(type: string | null) {
  if (!type) return "SOURCE";
  const raw = type.toLowerCase();
  switch (raw) {
    case "spec":
      return "OFFICIAL";
    case "docs":
      return "DOCUMENTATION";
    case "documentation":
      return "DOCUMENTATION";
    case "blog":
      return "BLOG";
    case "article":
      return "ARTICLE";
    case "tutorial":
      return "TUTORIAL";
    case "product":
      return "PRODUCT";
    case "github":
    case "repo":
      return "GITHUB";
    default:
      return type.toUpperCase();
  }
}

function normalizeMomentum(value: string | null): number {
  const parsed = Number(value ?? 0);
  return Number.isFinite(parsed) ? Math.max(0, Math.min(100, parsed)) : 0;
}

function priorityIndex(slug: string) {
  const priority = ["agent2agent", "agentic-ai", "ai-agent-skills", "context-engineering"];
  const index = priority.indexOf(slug);
  return index === -1 ? Number.MAX_SAFE_INTEGER : index;
}

function TrendSkeleton() {
  return (
    <div className="trend-detail-shell loading-shell">
      <div className="detail-header-skeleton skeleton-box" />
      <div className="detail-meta-skeleton">
        <div className="skeleton-pill" />
        <div className="skeleton-pill short" />
      </div>
      <div className="skeleton-line large" />
      <div className="skeleton-line medium" />
      <div className="skeleton-line medium" />
      <div className="section-skeleton">
        <div className="section-title-skeleton skeleton-box" />
        <div className="skeleton-line" />
        <div className="skeleton-line" />
      </div>
      <div className="section-skeleton">
        <div className="section-title-skeleton skeleton-box" />
        <div className="skeleton-line" />
        <div className="skeleton-line" />
        <div className="skeleton-line" />
      </div>
      <div className="section-skeleton">
        <div className="section-title-skeleton skeleton-box" />
        <div className="stack-placeholder" />
      </div>
      <div className="section-skeleton">
        <div className="section-title-skeleton skeleton-box" />
        <div className="skeleton-chip-row">
          <div className="skeleton-pill" />
          <div className="skeleton-pill" />
          <div className="skeleton-pill" />
        </div>
      </div>
      <div className="cta-skeleton" />
    </div>
  );
}

export default function TrendDetailClient({ slug }: TrendDetailClientProps) {
  const [trend, setTrend] = useState<TrendDetail | null>(null);
  const [related, setRelated] = useState<TrendDetail[]>([]);
  const [status, setStatus] = useState<"loading" | "ready" | "not-found" | "error">("loading");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    const controller = new AbortController();

    async function loadTrend() {
      try {
        setStatus("loading");
        setErrorMessage(null);

        const detailResponse = await fetch(`${apiUrl}/api/v1/trends/${slug}`, {
          signal: controller.signal,
          cache: "no-store",
        });

        if (!active) return;

        if (detailResponse.status === 404) {
          setStatus("not-found");
          return;
        }

        if (!detailResponse.ok) {
          throw new Error("Unable to load this trend.");
        }

        const trendData: TrendDetail = await detailResponse.json();
        setTrend(trendData);

        const listResponse = await fetch(`${apiUrl}/api/v1/trends`, {
          signal: controller.signal,
          cache: "no-store",
        });

        if (!active) return;

        const allTrends: TrendDetail[] = listResponse.ok ? await listResponse.json() : [];
        const relatedTrends = allTrends
          .filter((item) => trendData.related_trends?.includes(item.slug))
          .sort((a, b) => {
            const diff = priorityIndex(a.slug) - priorityIndex(b.slug);
            if (diff !== 0) return diff;
            return normalizeMomentum(b.momentum) - normalizeMomentum(a.momentum);
          });

        setRelated(relatedTrends);
        setStatus("ready");
      } catch (error) {
        if (!active) return;
        setStatus("error");
        setErrorMessage(error instanceof Error ? error.message : "Unable to load this trend.");
      }
    }

    loadTrend();

    return () => {
      active = false;
      controller.abort();
    };
  }, [slug]);

  const stackLayers = useMemo(() => {
    if (!trend?.tech_stack) return [];
    if (Array.isArray(trend.tech_stack)) {
      return [
        {
          name: "Technology",
          items: trend.tech_stack,
        },
      ];
    }
    return trend.tech_stack.layers ?? [];
  }, [trend]);

  if (status === "loading") {
    return <TrendSkeleton />;
  }

  if (status === "not-found") {
    return (
      <main className="trend-detail-page">
        <div className="trend-detail-shell error-shell">
          <p className="eyebrow">Trend not found</p>
          <h1>Trend not found</h1>
          <p className="error-copy">This trend may have been removed or is not available.</p>
          <Link href="/" className="back-link">
            ← Back to AI Radar
          </Link>
        </div>
      </main>
    );
  }

  if (status === "error") {
    return (
      <main className="trend-detail-page">
        <div className="trend-detail-shell error-shell">
          <p className="eyebrow">Unable to load trend</p>
          <h1>Unable to load this trend.</h1>
          <p className="error-copy">Please check your connection and try again.</p>
          <button className="retry-button" onClick={() => setStatus("loading")}>Try again</button>
          <Link href="/" className="back-link">
            ← Back to AI Radar
          </Link>
        </div>
      </main>
    );
  }

  if (!trend) {
    return null;
  }

  return (
    <main className="trend-detail-page">
      <div className="trend-detail-shell">
        <div className="detail-header-row">
          <div>
            <p className="eyebrow">{trend.category ?? "Trend"}</p>
            <h1>{trend.name}</h1>
            <p className="detail-subtitle">{trend.tldr}</p>
          </div>
          <div className="trend-status-card">
            <span className="trend-pill">{trend.status ?? "Status"}</span>
            <div className="momentum-block">
              <span className="momentum-label">Momentum</span>
              <span className="momentum-value">🔥 {normalizeMomentum(trend.momentum)}</span>
            </div>
          </div>
        </div>

        <div className="detail-actions">
          <Link href="/" className="secondary-link">
            ← Back to radar
          </Link>
        </div>

        <section className="detail-section">
          <div className="section-heading-row">
            <div>
              <p className="eyebrow">TL;DR</p>
              <h2>What this trend means</h2>
            </div>
          </div>
          <p className="detail-copy">{trend.tldr}</p>
        </section>

        <section className="detail-section">
          <div className="section-heading-row">
            <div>
              <p className="eyebrow">Why it matters</p>
              <h2>Why this trend is important</h2>
            </div>
          </div>
          <p className="detail-copy">{trend.why_it_matters}</p>
        </section>

        <section className="detail-section tech-section">
          <div className="section-heading-row">
            <div>
              <p className="eyebrow">Where it fits</p>
              <h2>Architecture and stack</h2>
            </div>
          </div>
          <TechStackMap layers={stackLayers} />
        </section>

        <section className="detail-section">
          <div className="section-heading-row">
            <div>
              <p className="eyebrow">Related technologies</p>
              <h2>Explore adjacent trends</h2>
            </div>
          </div>
          <div className="related-grid">
            {related.length > 0 ? (
              related.map((relatedTrend) => (
                <Link key={relatedTrend.slug} href={`/trends/${relatedTrend.slug}`} className="related-card">
                  <div>
                    <p className="related-category">{relatedTrend.category ?? "Trend"}</p>
                    <h3>{relatedTrend.name}</h3>
                  </div>
                  <div className="related-momentum">🔥 {normalizeMomentum(relatedTrend.momentum)}</div>
                </Link>
              ))
            ) : (
              <div className="empty-state">No related trends are available for this topic.</div>
            )}
          </div>
        </section>

        <section className="detail-section">
          <div className="section-heading-row">
            <div>
              <p className="eyebrow">Learn more</p>
              <h2>Trusted sources</h2>
            </div>
          </div>
          <div className="source-list">
            {trend.sources.map((source) => (
              <a
                key={source.id}
                href={source.url}
                target="_blank"
                rel="noopener noreferrer"
                className="source-card"
              >
                <span className="source-type">{formatSourceType(source.source_type)}</span>
                <span className="source-title">{source.title}</span>
                <span className="source-link">↗</span>
              </a>
            ))}
          </div>
        </section>

        <section className="detail-section cta-section">
          <div className="cta-card">
            <div>
              <p className="eyebrow">💬 Explore this trend with AI</p>
              <h2>Ask questions, compare technologies, or understand how this fits into the ecosystem.</h2>
            </div>
            <button type="button" className="primary-button" onClick={() => alert("Chat panel placeholder")}>Start exploring →</button>
          </div>
        </section>
      </div>
    </main>
  );
}
