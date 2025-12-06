import { cn } from "@/lib/utils";

interface Mascot3DProps {
  size?: "sm" | "md" | "lg" | "xl";
  className?: string;
  animated?: boolean;
  waving?: boolean;
}

const Mascot3D = ({ size = "md", className, animated = true, waving = false }: Mascot3DProps) => {
  const sizeClasses = {
    sm: "w-16 h-16",
    md: "w-24 h-24",
    lg: "w-32 h-32",
    xl: "w-48 h-48",
  };

  return (
    <div className={cn("relative", sizeClasses[size], className)}>
      {/* Glow effect behind mascot */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary/40 to-accent/40 rounded-full blur-xl animate-glow-pulse" />
      
      {/* Main mascot body */}
      <div className={cn(
        "relative w-full h-full",
        animated && "animate-float"
      )}>
        {/* Robot Head */}
        <svg viewBox="0 0 100 100" className="w-full h-full drop-shadow-2xl">
          <defs>
            <linearGradient id="bodyGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="hsl(263 90% 60%)" />
              <stop offset="100%" stopColor="hsl(200 100% 60%)" />
            </linearGradient>
            <linearGradient id="faceGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="hsl(222 47% 15%)" />
              <stop offset="100%" stopColor="hsl(222 47% 9%)" />
            </linearGradient>
            <linearGradient id="eyeGlow" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="hsl(180 100% 50%)" />
              <stop offset="100%" stopColor="hsl(150 100% 50%)" />
            </linearGradient>
            <filter id="glow">
              <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
              <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
          </defs>
          
          {/* Antenna */}
          <circle cx="50" cy="8" r="4" fill="url(#eyeGlow)" filter="url(#glow)">
            <animate attributeName="opacity" values="0.5;1;0.5" dur="2s" repeatCount="indefinite"/>
          </circle>
          <rect x="48" y="8" width="4" height="10" fill="url(#bodyGradient)" rx="2"/>
          
          {/* Head outline with gradient border */}
          <rect x="20" y="18" width="60" height="55" rx="12" fill="url(#bodyGradient)" opacity="0.3"/>
          <rect x="22" y="20" width="56" height="51" rx="10" fill="url(#faceGradient)"/>
          
          {/* Face screen */}
          <rect x="28" y="28" width="44" height="35" rx="6" fill="hsl(222 47% 6%)" stroke="url(#bodyGradient)" strokeWidth="1"/>
          
          {/* Eyes */}
          <ellipse cx="38" cy="42" rx="6" ry="8" fill="url(#eyeGlow)" filter="url(#glow)">
            <animate attributeName="ry" values="8;2;8" dur="3s" repeatCount="indefinite"/>
          </ellipse>
          <ellipse cx="62" cy="42" rx="6" ry="8" fill="url(#eyeGlow)" filter="url(#glow)">
            <animate attributeName="ry" values="8;2;8" dur="3s" repeatCount="indefinite"/>
          </ellipse>
          
          {/* Mouth - happy smile */}
          <path d="M 40 54 Q 50 62 60 54" stroke="url(#eyeGlow)" strokeWidth="2" fill="none" strokeLinecap="round" filter="url(#glow)"/>
          
          {/* Ear pieces */}
          <rect x="12" y="35" width="8" height="20" rx="4" fill="url(#bodyGradient)"/>
          <rect x="80" y="35" width="8" height="20" rx="4" fill="url(#bodyGradient)"/>
          
          {/* Body */}
          <rect x="30" y="73" width="40" height="20" rx="8" fill="url(#bodyGradient)" opacity="0.8"/>
          
          {/* Arms */}
          <g className={waving ? "origin-[25px_80px] animate-wave" : ""}>
            <rect x="15" y="75" width="15" height="6" rx="3" fill="url(#bodyGradient)" opacity="0.7"/>
            <circle cx="15" cy="78" r="4" fill="url(#eyeGlow)" opacity="0.6"/>
          </g>
          <rect x="70" y="75" width="15" height="6" rx="3" fill="url(#bodyGradient)" opacity="0.7"/>
          <circle cx="85" cy="78" r="4" fill="url(#eyeGlow)" opacity="0.6"/>
          
          {/* Chest light */}
          <circle cx="50" cy="83" r="4" fill="url(#eyeGlow)" filter="url(#glow)">
            <animate attributeName="opacity" values="0.6;1;0.6" dur="1.5s" repeatCount="indefinite"/>
          </circle>
        </svg>
      </div>
      
      {/* Floating particles around mascot */}
      <div className="absolute -top-2 -right-2 w-2 h-2 bg-accent rounded-full animate-bounce-slow opacity-60" />
      <div className="absolute -bottom-1 -left-3 w-3 h-3 bg-primary rounded-full animate-bounce-slow opacity-40" style={{ animationDelay: '-1s' }} />
      <div className="absolute top-1/2 -right-4 w-1.5 h-1.5 bg-neon-pink rounded-full animate-bounce-slow opacity-50" style={{ animationDelay: '-0.5s' }} />
    </div>
  );
};

export default Mascot3D;
