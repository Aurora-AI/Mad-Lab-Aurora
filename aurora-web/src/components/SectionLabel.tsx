import React from 'react';

interface SectionLabelProps {
  children: React.ReactNode;
  className?: string;
}

export default function SectionLabel({ children, className = '' }: SectionLabelProps) {
  return (
    <span
      className={`t-mono ${className}`}
      style={{
        fontSize: '0.65rem',
        letterSpacing: '0.35em',
        color: `color-mix(in srgb, var(--page-text) 40%, transparent)`,
        display: 'block',
        marginBottom: '2rem',
      }}
    >
      [ {children} ]
    </span>
  );
}
