import { useState } from "react";
import { useNavigate } from "react-router-dom";
import DashboardNav from "@/components/DashboardNav";
import FloatingElements from "@/components/FloatingElements";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { ArrowLeft, Map, Play, CheckCircle, Circle, Lock, Clock, Youtube, Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";

const roadmaps = [
  {
    id: 1,
    title: "Frontend Development",
    description: "Master React, TypeScript, and modern CSS",
    progress: 45,
    totalHours: 40,
    modules: 12,
    icon: "💻",
    color: "from-neon-blue to-neon-cyan",
  },
  {
    id: 2,
    title: "Data Science & ML",
    description: "Python, pandas, scikit-learn, and TensorFlow",
    progress: 20,
    totalHours: 60,
    modules: 18,
    icon: "🤖",
    color: "from-neon-purple to-neon-pink",
  },
  {
    id: 3,
    title: "Backend Development",
    description: "Node.js, databases, and API design",
    progress: 0,
    totalHours: 45,
    modules: 15,
    icon: "⚙️",
    color: "from-neon-green to-neon-cyan",
  },
  {
    id: 4,
    title: "DevOps Engineering",
    description: "Docker, Kubernetes, CI/CD, and cloud services",
    progress: 0,
    totalHours: 50,
    modules: 16,
    icon: "🚀",
    color: "from-neon-orange to-neon-pink",
  },
];

const sampleModules = [
  { title: "Introduction to React", duration: "2h 30m", completed: true, videoUrl: "#" },
  { title: "Components & Props", duration: "3h 15m", completed: true, videoUrl: "#" },
  { title: "State Management", duration: "4h 00m", completed: true, videoUrl: "#" },
  { title: "Hooks Deep Dive", duration: "3h 45m", completed: false, current: true, videoUrl: "#" },
  { title: "Context API", duration: "2h 00m", completed: false, videoUrl: "#" },
  { title: "Performance Optimization", duration: "3h 30m", completed: false, locked: true, videoUrl: "#" },
];

const Roadmaps = () => {
  const navigate = useNavigate();
  const [selectedRoadmap, setSelectedRoadmap] = useState<number | null>(null);

  const handleLogout = () => navigate("/");

  return (
    <div className="min-h-screen bg-background dark">
      <FloatingElements />
      <DashboardNav onLogout={handleLogout} />

      <main className="relative z-10 container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center gap-4 mb-8">
          <Button variant="ghost" size="icon" onClick={() => selectedRoadmap ? setSelectedRoadmap(null) : navigate("/dashboard")}>
            <ArrowLeft className="w-5 h-5" />
          </Button>
          <div>
            <h1 className="font-display text-3xl font-bold gradient-text flex items-center gap-3">
              <Map className="w-8 h-8" />
              AI Learning Roadmaps
            </h1>
            <p className="text-muted-foreground">Curated paths from free YouTube courses</p>
          </div>
        </div>

        {!selectedRoadmap ? (
          <>
            {/* AI Recommendation */}
            <div className="glass-card p-6 mb-8 animate-fade-in">
              <div className="flex items-center gap-4 mb-4">
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-primary to-accent flex items-center justify-center">
                  <Sparkles className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h2 className="font-display text-lg font-semibold">AI Recommendation</h2>
                  <p className="text-sm text-muted-foreground">Based on your career goals and current skills</p>
                </div>
              </div>
              <p className="text-muted-foreground mb-4">
                We recommend starting with <span className="text-foreground font-medium">Frontend Development</span> based on your quiz scores and career interests. This path will help you build a strong foundation for web development.
              </p>
              <Button className="gap-2 bg-gradient-to-r from-primary to-accent">
                Start Recommended Path
              </Button>
            </div>

            {/* Roadmap Grid */}
            <h2 className="font-display text-xl font-semibold mb-6">Available Roadmaps</h2>
            <div className="grid sm:grid-cols-2 gap-6">
              {roadmaps.map((roadmap, index) => (
                <div 
                  key={roadmap.id}
                  onClick={() => setSelectedRoadmap(roadmap.id)}
                  className="glass-card p-6 cursor-pointer hover:border-primary/50 transition-all duration-300 group animate-fade-in"
                  style={{ animationDelay: `${index * 100}ms` }}
                >
                  <div className="flex items-start gap-4 mb-4">
                    <div className={cn(
                      "w-14 h-14 rounded-xl bg-gradient-to-br flex items-center justify-center text-2xl group-hover:scale-110 transition-transform",
                      roadmap.color
                    )}>
                      {roadmap.icon}
                    </div>
                    <div className="flex-1">
                      <h3 className="font-display text-lg font-semibold group-hover:text-primary transition-colors">
                        {roadmap.title}
                      </h3>
                      <p className="text-sm text-muted-foreground">{roadmap.description}</p>
                    </div>
                  </div>

                  <div className="flex gap-4 text-sm text-muted-foreground mb-4">
                    <span className="flex items-center gap-1">
                      <Clock className="w-4 h-4" />
                      {roadmap.totalHours}h
                    </span>
                    <span>{roadmap.modules} modules</span>
                  </div>

                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Progress</span>
                      <span className="font-medium">{roadmap.progress}%</span>
                    </div>
                    <Progress value={roadmap.progress} className="h-2" />
                  </div>
                </div>
              ))}
            </div>
          </>
        ) : (
          /* Roadmap Detail View */
          <div className="animate-fade-in">
            <div className="glass-card p-6 mb-8">
              <div className="flex items-center gap-4 mb-4">
                <div className="w-16 h-16 rounded-xl bg-gradient-to-br from-neon-blue to-neon-cyan flex items-center justify-center text-3xl">
                  💻
                </div>
                <div>
                  <h2 className="font-display text-2xl font-bold">Frontend Development</h2>
                  <p className="text-muted-foreground">Master React, TypeScript, and modern CSS</p>
                </div>
              </div>
              <div className="flex gap-6 text-sm text-muted-foreground mb-4">
                <span className="flex items-center gap-1">
                  <Clock className="w-4 h-4" />
                  40 hours total
                </span>
                <span>12 modules</span>
                <span>Free YouTube courses</span>
              </div>
              <div className="flex gap-3">
                <Progress value={45} className="flex-1 h-3" />
                <span className="font-semibold">45%</span>
              </div>
            </div>

            <h3 className="font-display text-lg font-semibold mb-4">Course Modules</h3>
            <div className="space-y-3">
              {sampleModules.map((module, index) => (
                <div 
                  key={index}
                  className={cn(
                    "glass-card p-4 flex items-center gap-4 transition-all",
                    module.current && "border-primary",
                    module.locked && "opacity-60"
                  )}
                >
                  <div className={cn(
                    "w-10 h-10 rounded-full flex items-center justify-center",
                    module.completed ? "bg-neon-green text-white" :
                    module.current ? "bg-primary text-primary-foreground" :
                    "bg-secondary text-muted-foreground"
                  )}>
                    {module.completed ? <CheckCircle className="w-5 h-5" /> :
                     module.locked ? <Lock className="w-5 h-5" /> :
                     <Circle className="w-5 h-5" />}
                  </div>
                  
                  <div className="flex-1">
                    <h4 className="font-medium">{module.title}</h4>
                    <div className="flex items-center gap-3 text-sm text-muted-foreground">
                      <span className="flex items-center gap-1">
                        <Youtube className="w-4 h-4" />
                        YouTube
                      </span>
                      <span>{module.duration}</span>
                    </div>
                  </div>
                  
                  <Button 
                    variant={module.current ? "default" : "outline"}
                    size="sm"
                    disabled={module.locked}
                    className={module.current ? "gap-2 bg-gradient-to-r from-primary to-accent" : ""}
                  >
                    {module.completed ? "Review" : module.current ? <><Play className="w-4 h-4" /> Continue</> : "Start"}
                  </Button>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default Roadmaps;
