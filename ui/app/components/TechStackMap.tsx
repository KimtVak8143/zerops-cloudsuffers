interface TechStackLayer {
  name: string;
  items: string[];
}

interface TechStackMapProps {
  layers: TechStackLayer[];
}

function clampText(value: string, maxLength: number) {
  return value.length > maxLength ? `${value.slice(0, maxLength - 1)}…` : value;
}

export default function TechStackMap({ layers }: TechStackMapProps) {
  if (!layers?.length) {
    return (
      <div className="tech-stack-map empty">
        <div className="stack-empty">No architecture layers available.</div>
      </div>
    );
  }

  return (
    <div className="tech-stack-map">
      {layers.map((layer, index) => (
        <div key={layer.name} className="stack-column">
          <div className="stack-header">
            <span className="stack-label">{layer.name}</span>
          </div>
          <div className="stack-box">
            {layer.items.map((item) => (
              <div key={item} className="stack-item" title={item}>
                {clampText(item, 30)}
              </div>
            ))}
          </div>
          {index < layers.length - 1 ? (
            <div className="stack-connector" aria-hidden="true">
              <span />
            </div>
          ) : null}
        </div>
      ))}
    </div>
  );
}
