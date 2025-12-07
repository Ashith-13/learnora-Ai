import { cn } from "@/lib/utils";
import { LucideIcon } from "lucide-react";
import { Link } from "react-router-dom";

interface FeatureCardProps {
  title: string;
  description: string;
  icon: LucideIcon;
  href: string;
  gradient: string;
  delay?: number;
}

const FeatureCard = ({ title, description, icon: Icon, href, gradient, delay = 0 }: FeatureCardProps) => {
  return (
    <Link
      to={href}
      className={cn(
        "group relative overflow-hidden rounded-2xl p-6 transition-all duration-500",
        "bg-card/50 backdrop-blur-sm border border-border/50",
        "hover:border-primary/50 hover:shadow-2xl hover:shadow-primary/20",
        "hover:-translate-y-2 hover:scale-[1.02]",
        "animate-fade-in-up"
      )}
      style={{ animationDelay: `${delay}ms` }}
    >
      {/* Gradient overlay on hover */}
      <div className={cn(
        "absolute inset-0 opacity-0 group-hover:opacity-10 transition-opacity duration-500",
        gradient
      )} />
      
      {/* Glow effect */}
      <div className="absolute -inset-px rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 bg-gradient-to-r from-primary/20 via-transparent to-accent/20 blur-sm" />
      
      {/* Content */}
      <div className="relative z-10">
        {/* Icon container */}
        <div className={cn(
          "w-14 h-14 rounded-xl flex items-center justify-center mb-4",
          "bg-gradient-to-br transition-all duration-500",
          "group-hover:scale-110 group-hover:shadow-lg",
          gradient
        )}>
          <Icon className="w-7 h-7 text-white" />
        </div>
        
        {/* Title */}
        <h3 className="text-lg font-display font-semibold text-foreground mb-2 group-hover:text-primary transition-colors">
          {title}
        </h3>
        
        {/* Description */}
        <p className="text-sm text-muted-foreground leading-relaxed">
          {description}
        </p>
        
        {/* Arrow indicator */}
        <div className="mt-4 flex items-center text-primary opacity-0 group-hover:opacity-100 transition-all duration-300 transform translate-x-0 group-hover:translate-x-2">
          <span className="text-sm font-medium">Explore</span>
          <svg className="w-4 h-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
          </svg>
        </div>
      </div>
      
      {/* Shimmer effect */}
      <div className="absolute inset-0 -translate-x-full group-hover:translate-x-full transition-transform duration-1000 bg-gradient-to-r from-transparent via-white/5 to-transparent" />
    </Link>
  );
};

export default FeatureCard;
