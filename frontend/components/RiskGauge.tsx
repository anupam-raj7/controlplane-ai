interface RiskGaugeProps {
  score: number;
}

function colorForScore(score: number): string {
  if (score <= 30) return "#3FBF7F"; // allow
  if (score <= 60) return "#4AA8E0"; // verify
  if (score <= 85) return "#E0A73F"; // human review
  return "#E05B4A"; // block
}

export default function RiskGauge({ score }: RiskGaugeProps) {
  const color = colorForScore(score);
  return (
    <div className="w-full">
      <div className="mb-1 flex items-center justify-between text-xs text-base-400">
        <span>Risk score</span>
        <span style={{ color }}>{score}/100</span>
      </div>
      <div className="h-2 w-full overflow-hidden rounded-full bg-base-700">
        <div
          className="h-full rounded-full transition-all"
          style={{ width: `${score}%`, backgroundColor: color }}
        />
      </div>
    </div>
  );
}
