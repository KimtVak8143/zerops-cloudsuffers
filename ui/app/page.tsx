import React from "react";

const sections = [
  { title: "Trending", copy: "Track the most active ideas in AI today." },
  { title: "Emerging", copy: "Spot early signals and rising AI themes." },
  { title: "Categories", copy: "Browse by architecture, agents, data, and security." },
];

export default function Home() {
  return (
    <main className="page-shell">
      <div className="page-content">
        <section className="hero">
          <p className="eyebrow">AI Radar</p>
          <h1>Discover what's changing in AI.</h1>
          <p className="description">
            A clean hackathon MVP for finding and exploring emerging AI trends.
          </p>
        </section>

        <section className="grid">
          {sections.map((section) => (
            <article key={section.title} className="card">
              <h2>{section.title}</h2>
              <p>{section.copy}</p>
            </article>
          ))}
        </section>
      </div>
    </main>
  );
}
