import TrendDetailClient from "../../components/TrendDetailClient";

interface TrendPageProps {
  params: {
    slug: string;
  };
}

export default function TrendDetail({ params }: TrendPageProps) {
  return <TrendDetailClient slug={params.slug} />;
}
