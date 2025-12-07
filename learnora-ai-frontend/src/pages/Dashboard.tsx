import { useNavigate } from "react-router-dom";
import DashboardNav from "@/components/DashboardNav";
import FloatingElements from "@/components/FloatingElements";
import FeatureCard from "@/components/FeatureCard";
import Mascot3D from "@/components/Mascot3D";
import {
  Gamepad2,
  MessageCircle,
  BarChart3,
  FileText,
  Briefcase,
  Video,
  Microscope,
  Map,
  Flame,
  Trophy,
  Target,
} from "lucide-react";

const features = [
  {
    title: "Gamified Quiz",
    description: "Test your knowledge with interactive quizzes, earn XP, climb leaderboards, and unlock achievements.",
    icon: Gamepad2,
    href: "/quiz",
    gradient: "bg-gradient-to-br from-neon-purple to-neon-pink",
  },
  {
    title: "AI Doubt Solver",
    description: "Get instant AI-powered answers to your academic questions. Supports text, images, and equations.",
    icon: MessageCircle,
    href: "/doubt-solver",
    gradient: "bg-gradient-to-br from-neon-blue to-neon-cyan",
  },
  {
    title: "Career Readiness Score",
    description: "Assess your career readiness, identify skill gaps, and get personalized improvement recommendations.",
    icon: BarChart3,
    href: "/career-score",
    gradient: "bg-gradient-to-br from-neon-green to-neon-cyan",
  },
  {
    title: "AI Resume Builder",
    description: "Create professional resumes with AI assistance. Multiple templates and instant PDF download.",
    icon: FileText,
    href: "/resume-builder",
    gradient: "bg-gradient-to-br from-neon-orange to-neon-pink",
  },
  {
    title: "Job Recommendations",
    description: "Discover personalized job matches based on your skills, experience, and career goals.",
    icon: Briefcase,
    href: "/jobs",
    gradient: "bg-gradient-to-br from-neon-purple to-neon-blue",
  },
  {
    title: "AI Video Generator",
    description: "Transform topics into engaging educational videos. Perfect for visual learning.",
    icon: Video,
    href: "/video-generator",
    gradient: "bg-gradient-to-br from-neon-pink to-neon-orange",
  },
  {
    title: "AR Labs",
    description: "Experience interactive 3D models and virtual experiments for immersive learning.",
    icon: Microscope,
    href: "/ar-labs",
    gradient: "bg-gradient-to-br from-neon-cyan to-neon-green",
  },
  {
    title: "AI Learning Roadmaps",
    description: "Get curated learning paths from free YouTube courses with progress tracking and milestones.",
    icon: Map,
    href: "/roadmaps",
    gradient: "bg-gradient-to-br from-neon-blue to-neon-purple",
  },
];

const Dashboard = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    navigate("/");
  };

  return (
    <div className="min-h-screen bg-background dark">
      <FloatingElements />
      <DashboardNav onLogout={handleLogout} />

      <main className="relative z-10 container mx-auto px-4 py-8">
        {/* Hero Section */}
        <section className="mb-12">
          <div className="flex flex-col lg:flex-row items-center gap-8 lg:gap-12">
            {/* Welcome text */}
            <div className="flex-1 text-center lg:text-left">
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-primary/10 rounded-full text-primary text-sm font-medium mb-4 animate-fade-in">
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
                </span>
                AI-Powered Learning Platform
              </div>
              
              <h1 className="font-display text-4xl lg:text-5xl font-bold mb-4 animate-fade-in" style={{ animationDelay: '100ms' }}>
                Welcome back, <span className="gradient-text">Learner!</span>
              </h1>
              
              <p className="text-lg text-muted-foreground max-w-xl animate-fade-in" style={{ animationDelay: '200ms' }}>
                Continue your learning journey with AI-powered tools designed to help you learn better, plan better, and become better.
              </p>

              {/* Quick stats */}
              <div className="flex flex-wrap justify-center lg:justify-start gap-6 mt-8 animate-fade-in" style={{ animationDelay: '300ms' }}>
                <div className="flex items-center gap-3 glass-card px-4 py-3">
                  <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-neon-orange to-neon-pink flex items-center justify-center">
                    <Flame className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-foreground">7</p>
                    <p className="text-xs text-muted-foreground">Day Streak</p>
                  </div>
                </div>
                
                <div className="flex items-center gap-3 glass-card px-4 py-3">
                  <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-neon-purple to-neon-blue flex items-center justify-center">
                    <Trophy className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-foreground">1,250</p>
                    <p className="text-xs text-muted-foreground">Total XP</p>
                  </div>
                </div>
                
                <div className="flex items-center gap-3 glass-card px-4 py-3">
                  <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-neon-green to-neon-cyan flex items-center justify-center">
                    <Target className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-foreground">72%</p>
                    <p className="text-xs text-muted-foreground">Career Score</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Mascot */}
            <div className="lg:flex-shrink-0 animate-fade-in" style={{ animationDelay: '400ms' }}>
              <Mascot3D size="xl" waving />
            </div>
          </div>
        </section>

        {/* Features Grid */}
        <section>
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="font-display text-2xl font-bold text-foreground">Explore Features</h2>
              <p className="text-muted-foreground mt-1">Unlock your potential with our AI-powered tools</p>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <FeatureCard
                key={feature.title}
                {...feature}
                delay={index * 100}
              />
            ))}
          </div>
        </section>
      </main>
    </div>
  );
};

export default Dashboard;
