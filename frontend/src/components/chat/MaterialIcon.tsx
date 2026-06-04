interface MaterialIconProps {
  name: string;
  filled?: boolean;
  size?: number;
  className?: string;
  "aria-hidden"?: boolean;
}

export function MaterialIcon({
  name,
  filled = false,
  size = 24,
  className,
  "aria-hidden": ariaHidden = true,
}: MaterialIconProps) {
  return (
    <span
      className={`material-symbols-outlined ${className ?? ""}`}
      aria-hidden={ariaHidden}
      style={{
        fontSize: size,
        ...(filled ? { fontVariationSettings: "'FILL' 1" } : {}),
      }}
    >
      {name}
    </span>
  );
}
