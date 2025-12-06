import { useNavigate } from "react-router-dom";
import Mascot3D from "@/components/Mascot3D";
import AuthForm from "@/components/AuthForm";
import FloatingElements from "@/components/FloatingElements";

const Auth = () => {
  const navigate = useNavigate();

  const handleAuthSuccess = () => {
    navigate("/dashboard");
  };

  return (
    <div className="min-h-screen bg-background relative overflow-hidden dark">
      <FloatingElements />
      
      <div className="relative z-10 min-h-screen flex">
        {/* Left side - Branding */}
        <div className="hidden lg:flex lg:w-1/2 flex-col items-center justify-center p-12 relative">
          {/* Large glowing orb behind mascot */}
          <div className="absolute w-[500px] h-[500px] bg-gradient-to-br from-primary/30 to-accent/20 rounded-full blur-3xl" />
          
          <div className="relative z-10 text-center">
            <Mascot3D size="xl" waving className="mx-auto mb-8" />
            
            <h1 className="font-display text-5xl font-bold mb-4 animate-fade-in">
              <span className="gradient-text">Learnora AI</span>
            </h1>
            
            <p className="text-xl text-muted-foreground max-w-md mx-auto animate-fade-in" style={{ animationDelay: '200ms' }}>
              Learn Better. Plan Better. Become Better.
            </p>
            
            <div className="mt-12 grid grid-cols-2 gap-4 max-w-sm mx-auto animate-fade-in" style={{ animationDelay: '400ms' }}>
              {[
                { label: "AI-Powered Learning", icon: "🤖" },
                { label: "Gamified Experience", icon: "🎮" },
                { label: "Career Readiness", icon: "🚀" },
                { label: "Personalized Paths", icon: "🗺️" },
              ].map((item, i) => (
                <div key={i} className="flex items-center gap-2 text-sm text-muted-foreground">
                  <span className="text-lg">{item.icon}</span>
                  <span>{item.label}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right side - Auth Form */}
        <div className="w-full lg:w-1/2 flex items-center justify-center p-6 lg:p-12">
          <div className="w-full max-w-md">
            {/* Mobile logo */}
            <div className="lg:hidden text-center mb-8">
              <Mascot3D size="lg" waving className="mx-auto mb-4" />
              <h1 className="font-display text-3xl font-bold gradient-text">Learnora AI</h1>
              <p className="text-sm text-muted-foreground mt-1">Learn Better. Plan Better. Become Better.</p>
            </div>
            
            <div className="glass-card p-8 animate-scale-in">
              <h2 className="font-display text-2xl font-semibold text-center mb-2">
                Welcome to Learnora
              </h2>
              <p className="text-muted-foreground text-center mb-8">
                Your AI-powered learning companion
              </p>
              
              <AuthForm onSuccess={handleAuthSuccess} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Auth;
