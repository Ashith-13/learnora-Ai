import { useNavigate } from "react-router-dom";
import DashboardNav from "@/components/DashboardNav";
import FloatingElements from "@/components/FloatingElements";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, Microscope, Box, Play, Lock } from "lucide-react";
import { cn } from "@/lib/utils";

const labs = [
  {
    id: 1,
    title: "Human Heart 3D Model",
    subject: "Biology",
    description: "Explore the human heart in 3D. Learn about chambers, valves, and blood flow.",
    icon: "❤️",
    locked: false,
  },
  {
    id: 2,
    title: "Solar System Explorer",
    subject: "Astronomy",
    description: "Navigate through our solar system. Examine planets, moons, and orbital mechanics.",
    icon: "🌍",
    locked: false,
  },
  {
    id: 3,
    title: "Molecular Chemistry Lab",
    subject: "Chemistry",
    description: "Build and manipulate molecules. Understand chemical bonds and structures.",
    icon: "⚗️",
    locked: false,
  },
  {
    id: 4,
    title: "Circuit Builder",
    subject: "Physics",
    description: "Build virtual circuits and understand electricity flow.",
    icon: "⚡",
    locked: true,
  },
  {
    id: 5,
    title: "DNA Structure",
    subject: "Biology",
    description: "Explore the double helix structure of DNA in 3D.",
    icon: "🧬",
    locked: true,
  },
  {
    id: 6,
    title: "Volcano Simulation",
    subject: "Geology",
    description: "Witness volcanic eruptions and understand plate tectonics.",
    icon: "🌋",
    locked: true,
  },
];

const ARLabs = () => {
  const navigate = useNavigate();
  const handleLogout = () => navigate("/");

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
              <Microscope className="w-8 h-8" />
              AR Labs
            </h1>
            <p className="text-muted-foreground">Interactive 3D models and virtual experiments</p>
          </div>
        </div>

        {/* Featured Lab */}
        <div className="glass-card p-8 mb-8 relative overflow-hidden animate-fade-in">
          <div className="absolute inset-0 bg-gradient-to-br from-primary/10 to-accent/10" />
          <div className="relative z-10 flex flex-col md:flex-row gap-8 items-center">
            <div className="w-48 h-48 bg-gradient-to-br from-primary/20 to-accent/20 rounded-2xl flex items-center justify-center text-8xl animate-float">
              🔬
            </div>
            <div className="flex-1 text-center md:text-left">
              <Badge className="mb-3 bg-neon-green/20 text-neon-green">Featured Lab</Badge>
              <h2 className="font-display text-2xl font-bold mb-2">Chemistry Virtual Lab</h2>
              <p className="text-muted-foreground mb-4 max-w-lg">
                Conduct virtual chemistry experiments safely. Mix chemicals, observe reactions, and learn fundamental concepts through hands-on experience.
              </p>
              <Button className="gap-2 bg-gradient-to-r from-primary to-accent">
                <Play className="w-4 h-4" />
                Launch Lab
              </Button>
            </div>
          </div>
        </div>

        {/* Lab Grid */}
        <h2 className="font-display text-xl font-semibold mb-6">All Labs</h2>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {labs.map((lab, index) => (
            <div 
              key={lab.id}
              className={cn(
                "glass-card p-6 group hover:border-primary/50 transition-all duration-300 animate-fade-in",
                lab.locked && "opacity-60"
              )}
              style={{ animationDelay: `${index * 100}ms` }}
            >
              <div className="flex items-start justify-between mb-4">
                <div className="w-16 h-16 bg-gradient-to-br from-primary/20 to-accent/20 rounded-xl flex items-center justify-center text-3xl group-hover:scale-110 transition-transform">
                  {lab.icon}
                </div>
                {lab.locked && (
                  <div className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center">
                    <Lock className="w-4 h-4 text-muted-foreground" />
                  </div>
                )}
              </div>
              
              <Badge variant="secondary" className="mb-2">{lab.subject}</Badge>
              <h3 className="font-display text-lg font-semibold mb-2">{lab.title}</h3>
              <p className="text-sm text-muted-foreground mb-4">{lab.description}</p>
              
              <Button 
                variant={lab.locked ? "outline" : "default"} 
                className={cn("w-full gap-2", !lab.locked && "bg-gradient-to-r from-primary to-accent")}
                disabled={lab.locked}
              >
                {lab.locked ? (
                  <>
                    <Lock className="w-4 h-4" />
                    Unlock with Premium
                  </>
                ) : (
                  <>
                    <Box className="w-4 h-4" />
                    Open Lab
                  </>
                )}
              </Button>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
};

export default ARLabs;
