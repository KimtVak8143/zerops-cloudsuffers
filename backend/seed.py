import asyncio

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.session import AsyncSessionLocal
from app.models.source import Source
from app.models.trend import Trend


TREND_SEED_DATA = [
    {
        "name": "Model Context Protocol",
        "slug": "model-context-protocol",
        "category": "Protocols",
        "status": "Growing",
        "tldr": "A standardized protocol for agent-to-tool and service invocation that normalizes tool metadata, authorization, and response structure.",
        "why_it_matters": "MCP makes agent ecosystems composable by treating tool calls as first-class protocol objects, reducing custom SDKs and enabling safer interoperability.",
        "momentum": "94",
        "tech_stack": ["MCP", "HTTP", "JSON", "API schemas"],
        "related_trends": ["agent2agent", "agentic-ai", "context-engineering"],
        "sources": [
            {
                "title": "The 2026-07-28 MCP Specification",
                "url": "https://blog.modelcontextprotocol.io/posts/2026-07-28",
                "source_type": "spec",
            },
            {
                "title": "MCP Specification Release Candidate",
                "url": "https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate",
                "source_type": "blog",
            },
        ],
    },
    {
        "name": "Agent2Agent (A2A)",
        "slug": "agent2agent",
        "category": "Protocols",
        "status": "Growing",
        "tldr": "A communication protocol for independent AI agents to exchange tasks, capabilities, and responses without relying on shared tool contexts.",
        "why_it_matters": "A2A enables agent-to-agent workflows where Agent A coordinates with Agent B, while MCP remains focused on agent-to-tool and service integration.",
        "momentum": "92",
        "tech_stack": ["A2A", "agent cards", "OpenID Connect", "task lifecycle"],
        "related_trends": ["model-context-protocol", "agentic-ai", "agent-security"],
        "sources": [
            {
                "title": "Announcing the Agent2Agent Protocol (A2A)",
                "url": "https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability",
                "source_type": "blog",
            },
            {
                "title": "A2A Protocol Technical Documentation",
                "url": "https://agent2agent.info/docs",
                "source_type": "docs",
            },
        ],
    },
    {
        "name": "Agentic AI",
        "slug": "agentic-ai",
        "category": "Agents",
        "status": "Growing",
        "tldr": "Agents are being designed as autonomous decision-makers that plan, act, and adapt across complex workflows.",
        "why_it_matters": "Agentic systems bring higher-level automation to AI products, but they also demand new runtime governance and observability.",
        "momentum": "88",
        "tech_stack": ["orchestration", "planning", "tool selection", "service meshes"],
        "related_trends": ["model-context-protocol", "agent2agent", "reasoning-models"],
        "sources": [
            {
                "title": "Announcing the Agent2Agent Protocol (A2A)",
                "url": "https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability",
                "source_type": "blog",
            },
            {
                "title": "A2A Protocol Technical Documentation",
                "url": "https://agent2agent.info/docs",
                "source_type": "docs",
            },
        ],
    },
    {
        "name": "Context Engineering",
        "slug": "context-engineering",
        "category": "Context",
        "status": "Adoption",
        "tldr": "Teams are engineering prompt context, state, and metadata to make agent decisions reproducible, auditable, and efficient.",
        "why_it_matters": "Clear context engineering helps bridge model intent with tool calls, reducing hallucinations and improving agent trustworthiness.",
        "momentum": "81",
        "tech_stack": ["prompt design", "state management", "metadata", "session-less APIs"],
        "related_trends": ["model-context-protocol", "agentic-ai", "reasoning-models"],
        "sources": [
            {
                "title": "The 2026-07-28 MCP Specification",
                "url": "https://blog.modelcontextprotocol.io/posts/2026-07-28",
                "source_type": "spec",
            },
            {
                "title": "MCP Specification Release Candidate",
                "url": "https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate",
                "source_type": "blog",
            },
        ],
    },
    {
        "name": "AI Agent Skills",
        "slug": "ai-agent-skills",
        "category": "Developer AI",
        "status": "Emerging",
        "tldr": "Agent skills describe capabilities, schemas, and security posture so agents can negotiate work across protocols and runtimes.",
        "why_it_matters": "Standardized skill descriptions make agent interoperability and discovery much easier for multi-agent ecosystems.",
        "momentum": "76",
        "tech_stack": ["skill manifests", "capability schemas", "agent cards", "metadata"],
        "related_trends": ["agent2agent", "agentic-ai", "agent-memory"],
        "sources": [
            {
                "title": "Getting Started with Agent2Agent (A2A)",
                "url": "https://codelabs.developers.google.com/intro-a2a-purchasing-concierge",
                "source_type": "tutorial",
            },
            {
                "title": "A2A Protocol Technical Documentation",
                "url": "https://agent2agent.info/docs",
                "source_type": "docs",
            },
        ],
    },
    {
        "name": "Agent Memory",
        "slug": "agent-memory",
        "category": "Agent Infrastructure",
        "status": "Growing",
        "tldr": "Persistent agent memory stores state, user preferences, and task context so agents can continue conversations and workflows safely.",
        "why_it_matters": "Memory is essential for agent continuity, enabling more natural long-running interactions while keeping data boundaries explicit.",
        "momentum": "78",
        "tech_stack": ["vector stores", "secure storage", "session records", "cache invalidation"],
        "related_trends": ["context-engineering", "agentic-ai", "agent-security"],
        "sources": [
            {
                "title": "A2A Protocol Technical Documentation",
                "url": "https://agent2agent.info/docs",
                "source_type": "docs",
            },
            {
                "title": "The 2026-07-28 MCP Specification",
                "url": "https://blog.modelcontextprotocol.io/posts/2026-07-28",
                "source_type": "spec",
            },
        ],
    },
    {
        "name": "AI Coding Agents",
        "slug": "ai-coding-agents",
        "category": "Developer AI",
        "status": "Adoption",
        "tldr": "Tools and agents are being built to write, review, and evolve software with model-driven workflows and tool integrations.",
        "why_it_matters": "Coding agents are shifting developer tooling from manual editing to AI-assisted development and secure deployment automation.",
        "momentum": "82",
        "tech_stack": ["IDE integrations", "LLMs", "code analysis", "tool calling"],
        "related_trends": ["agentic-ai", "reasoning-models", "ai-agent-skills"],
        "sources": [
            {
                "title": "GitHub Copilot expands to more developers",
                "url": "https://github.com/features/copilot",
                "source_type": "product",
            },
            {
                "title": "OpenAI releases code generation capabilities",
                "url": "https://openai.com/research/codex",
                "source_type": "article",
            },
        ],
    },
    {
        "name": "Reasoning Models",
        "slug": "reasoning-models",
        "category": "Models",
        "status": "Adoption",
        "tldr": "Models are being evaluated for structured reasoning, multi-step planning, and explainable outputs that support agent decision-making.",
        "why_it_matters": "Reasoning models define the boundaries between raw generation and reliable, composable agent workflows.",
        "momentum": "85",
        "tech_stack": ["tool-aware models", "chain-of-thought", "plan execution", "evaluation"],
        "related_trends": ["agentic-ai", "context-engineering", "model-context-protocol"],
        "sources": [
            {
                "title": "The 2026-07-28 MCP Specification",
                "url": "https://blog.modelcontextprotocol.io/posts/2026-07-28",
                "source_type": "spec",
            },
            {
                "title": "OpenAI introduces GPT-4 with image understanding",
                "url": "https://openai.com/research/gpt-4",
                "source_type": "article",
            },
        ],
    },
    {
        "name": "Multimodal AI",
        "slug": "multimodal-ai",
        "category": "Models",
        "status": "Growing",
        "tldr": "AI systems are combining text, image, audio, and logic to support richer agent interfaces and multi-domain workflows.",
        "why_it_matters": "Multimodal understanding expands how agents perceive and interact with real-world signals beyond text.",
        "momentum": "80",
        "tech_stack": ["vision", "speech", "LLMs", "sensor fusion"],
        "related_trends": ["reasoning-models", "ai-coding-agents", "agentic-ai"],
        "sources": [
            {
                "title": "OpenAI introduces GPT-4 with image understanding",
                "url": "https://openai.com/research/gpt-4",
                "source_type": "article",
            },
            {
                "title": "Google’s Gemini multimodal AI",
                "url": "https://blog.google/technology/ai/gemini/",
                "source_type": "article",
            },
        ],
    },
    {
        "name": "Agent Security",
        "slug": "agent-security",
        "category": "Security",
        "status": "Growing",
        "tldr": "Security capabilities are being integrated into agent protocols and runtimes so agent trust boundaries are explicit and enforceable.",
        "why_it_matters": "Agent security is critical for safe multi-agent collaboration, identity, and authorization in production systems.",
        "momentum": "79",
        "tech_stack": ["auth", "authorization", "audit logs", "policy enforcement"],
        "related_trends": ["agent2agent", "model-context-protocol", "agent-memory"],
        "sources": [
            {
                "title": "Announcing the Agent2Agent Protocol (A2A)",
                "url": "https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability",
                "source_type": "blog",
            },
            {
                "title": "A2A Protocol Technical Documentation",
                "url": "https://agent2agent.info/docs",
                "source_type": "docs",
            },
        ],
    },
    {
        "name": "AI Inference Infrastructure",
        "slug": "ai-inference-infrastructure",
        "category": "AI Infrastructure",
        "status": "Adoption",
        "tldr": "Infrastructure is being optimized for efficient model execution, latency, and cost across cloud, edge, and hybrid deployments.",
        "why_it_matters": "Inference infrastructure determines whether next-generation AI systems can scale from research prototypes to production services.",
        "momentum": "83",
        "tech_stack": ["GPU clusters", "model serving", "accelerators", "autoscaling"],
        "related_trends": ["agentic-ai", "edge-ai", "model-context-protocol"],
        "sources": [
            {
                "title": "NVIDIA Inference for AI infrastructure",
                "url": "https://www.nvidia.com/en-us/data-center/inference/",
                "source_type": "article",
            },
            {
                "title": "AWS inference infrastructure",
                "url": "https://aws.amazon.com/machine-learning/inference/",
                "source_type": "article",
            },
        ],
    },
]


async def seed_trends() -> None:
    async with AsyncSessionLocal() as session:
        for trend_data in TREND_SEED_DATA:
            slug = trend_data["slug"]
            result = await session.execute(select(Trend).options(selectinload(Trend.sources)).filter_by(slug=slug))
            trend = result.scalars().first()
            sources = trend_data.pop("sources")

            if trend:
                trend.name = trend_data["name"]
                trend.category = trend_data["category"]
                trend.status = trend_data["status"]
                trend.tldr = trend_data["tldr"]
                trend.why_it_matters = trend_data["why_it_matters"]
                trend.momentum = trend_data["momentum"]
                trend.tech_stack = trend_data["tech_stack"]
                trend.related_trends = trend_data["related_trends"]
                trend.sources = []
            else:
                trend = Trend(**trend_data)
                session.add(trend)

            for source_data in sources:
                trend.sources.append(Source(**source_data))

        await session.commit()
        print("Seed data complete.")


def main() -> None:
    asyncio.run(seed_trends())


if __name__ == "__main__":
    main()
