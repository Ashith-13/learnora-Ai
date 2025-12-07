import { useNavigate } from "react-router-dom";
import DashboardNav from "@/components/DashboardNav";
import FloatingElements from "@/components/FloatingElements";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { ArrowLeft, BarChart3, TrendingUp, Target, Award, BookOpen, Code, Users, Briefcase } from "lucide-react";
import { cn } from "@/lib/utils";

const skills = [
  { name: "Technical Skills", score: 78, icon: Code, color: "from-neon-blue to-neon-cyan" },
  { name: "Communication", score: 65, icon: Users, color: "from-neon-purple to-neon-pink" },
  { name: "Problem Solving", score: 82, icon: Target, color: "from-neon-green to-neon-cyan" },
  { name: "Leadership", score: 55, icon: Award, color: "from-neon-orange to-neon-pink" },
  { name: "Domain Knowledge", score: 70, icon: BookOpen, color: "from-neon-pink to-neon-purple" },
  { name: "Industry Readiness", score: 60, icon: Briefcase, color: "from-neon-cyan to-neon-blue" },
];

const CareerScore = () => {
  const navigate = useNavigate();
  const handleLogout = () => navigate("/");

  const overallScore = Math.round(skills.reduce((acc, s) => acc + s.score, 0) / skills.length);

  return (
    <div className="min-h-screen bg-background dark">
      <FloatingElements />
      <DashboardNav onLogout={handleLogout} />

      <main className="relative z-10 container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center gap-4 mb-8">
          <Button variant="ghost" size="icon" onClick={() => navigate("/dashboard")}>
            <ArrowLeft className="w-5 h-5" />
          </Button>
          <div>
            <h1 className="font-display text-3xl font-bold gradient-text flex items-center gap-3">
              <BarChart3 className="w-8 h-8" />
              Career Readiness Score
            </h1>
            <p className="text-muted-foreground">Assess your career readiness and identify areas for improvement</p>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Overall Score */}
          <div className="lg:col-span-1">
            <div className="glass-card p-8 text-center sticky top-24">
              <h2 className="font-display text-xl font-semibold mb-6">Your Career Score</h2>
              
              <div className="relative w-48 h-48 mx-auto mb-6">
                <svg className="w-full h-full -rotate-90" viewBox="0 0 100 100">
                  <circle
                    cx="50"
                    cy="50"
                    r="45"
                    fill="none"
                    stroke="hsl(var(--secondary))"
                    strokeWidth="8"
                  />
                  <circle
                    cx="50"
                    cy="50"
                    r="45"
                    fill="none"
                    stroke="url(#scoreGradient)"
                    strokeWidth="8"
                    strokeLinecap="round"
                    strokeDasharray={`${overallScore * 2.83} 283`}
                    className="transition-all duration-1000"
                  />
                  <defs>
                    <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                      <stop offset="0%" stopColor="hsl(var(--primary))" />
                      <stop offset="100%" stopColor="hsl(var(--accent))" />
                    </linearGradient>
                  </defs>
                </svg>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                  <span className="text-5xl font-bold gradient-text">{overallScore}</span>
                  <span className="text-sm text-muted-foreground">out of 100</span>
                </div>
              </div>

              <div className="flex items-center justify-center gap-2 text-neon-green mb-4">
                <TrendingUp className="w-5 h-5" />
                <span className="font-medium">+5 from last month</span>
              </div>

              <Button className="w-full bg-gradient-to-r from-primary to-accent">
                Take Assessment
              </Button>
            </div>
          </div>

          {/* Skills Breakdown */}
          <div className="lg:col-span-2 space-y-6">
            <h2 className="font-display text-xl font-semibold">Skills Breakdown</h2>
            
            <div className="grid gap-4">
              {skills.map((skill, index) => (
                <div 
                  key={skill.name} 
                  className="glass-card p-6 animate-fade-in"
                  style={{ animationDelay: `${index * 100}ms` }}
                >
                  <div className="flex items-center gap-4 mb-4">
                    <div className={cn(
                      "w-12 h-12 rounded-xl bg-gradient-to-br flex items-center justify-center",
                      skill.color
                    )}>
                      <skill.icon className="w-6 h-6 text-white" />
                    </div>
                    <div className="flex-1">
                      <div className="flex justify-between items-center mb-2">
                        <h3 className="font-semibold">{skill.name}</h3>
                        <span className="text-lg font-bold">{skill.score}%</span>
                      </div>
                      <Progress value={skill.score} className="h-2" />
                    </div>
                  </div>
                  
                  <p className="text-sm text-muted-foreground">
                    {skill.score >= 75 
                      ? "Excellent! Keep maintaining this skill level."
                      : skill.score >= 50 
                        ? "Good progress. Consider taking advanced courses to improve."
                        : "Needs improvement. Check out our recommended learning paths."}
                  </p>
                </div>
              ))}
            </div>

            {/* Recommendations */}
            <div className="glass-card p-6">
              <h3 className="font-display text-lg font-semibold mb-4">Recommendations</h3>
              <ul className="space-y-3">
                <li className="flex items-start gap-3">
                  <div className="w-2 h-2 rounded-full bg-primary mt-2" />
                  <p className="text-muted-foreground">Complete the Leadership Development course to boost your score</p>
                </li>
                <li className="flex items-start gap-3">
                  <div className="w-2 h-2 rounded-full bg-accent mt-2" />
                  <p className="text-muted-foreground">Practice mock interviews to improve communication skills</p>
                </li>
                <li className="flex items-start gap-3">
                  <div className="w-2 h-2 rounded-full bg-neon-green mt-2" />
                  <p className="text-muted-foreground">Take the Industry Readiness assessment for a detailed analysis</p>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default CareerScore;
