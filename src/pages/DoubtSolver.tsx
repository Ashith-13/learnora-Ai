import { useState } from "react";
import { useNavigate } from "react-router-dom";
import DashboardNav from "@/components/DashboardNav";
import FloatingElements from "@/components/FloatingElements";
import Mascot3D from "@/components/Mascot3D";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { ArrowLeft, Send, Loader2, Image, Sparkles, MessageCircleQuestion } from "lucide-react";
import { cn } from "@/lib/utils";

interface Message {
  role: "user" | "assistant";
  content: string;
}

const DoubtSolver = () => {
  const navigate = useNavigate();
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleLogout = () => navigate("/");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput("");
    setMessages(prev => [...prev, { role: "user", content: userMessage }]);
    setIsLoading(true);

    // Simulate AI response
    setTimeout(() => {
      const response = `I understand you're asking about "${userMessage}". Let me help you with that!\n\nThis is a simulated response. When connected to Lovable AI, I'll provide detailed explanations, solve equations, and help you understand complex concepts step by step.`;
      setMessages(prev => [...prev, { role: "assistant", content: response }]);
      setIsLoading(false);
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-background dark flex flex-col">
      <FloatingElements />
      <DashboardNav onLogout={handleLogout} />

      <main className="relative z-10 container mx-auto px-4 py-8 flex-1 flex flex-col">
        {/* Header */}
        <div className="flex items-center gap-4 mb-6">
          <Button variant="ghost" size="icon" onClick={() => navigate("/dashboard")}>
            <ArrowLeft className="w-5 h-5" />
          </Button>
          <div>
            <h1 className="font-display text-3xl font-bold gradient-text flex items-center gap-3">
              <MessageCircleQuestion className="w-8 h-8" />
              AI Doubt Solver
            </h1>
            <p className="text-muted-foreground">Get instant answers to your academic questions</p>
          </div>
        </div>

        {/* Chat Area */}
        <div className="flex-1 glass-card rounded-2xl flex flex-col overflow-hidden">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-6 space-y-6">
            {messages.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center">
                <Mascot3D size="lg" waving className="mb-6" />
                <h2 className="font-display text-2xl font-semibold mb-2">Hi! I'm your AI tutor</h2>
                <p className="text-muted-foreground max-w-md mb-8">
                  Ask me any academic question - math problems, science concepts, programming help, or anything else you're curious about!
                </p>
                <div className="flex flex-wrap justify-center gap-2">
                  {["Explain photosynthesis", "Solve x² + 5x + 6 = 0", "What is recursion?", "History of AI"].map((q) => (
                    <button
                      key={q}
                      onClick={() => setInput(q)}
                      className="px-4 py-2 bg-secondary/50 hover:bg-secondary rounded-full text-sm transition-colors"
                    >
                      {q}
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              messages.map((msg, i) => (
                <div
                  key={i}
                  className={cn(
                    "flex gap-4 animate-fade-in",
                    msg.role === "user" && "flex-row-reverse"
                  )}
                >
                  <div className={cn(
                    "w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0",
                    msg.role === "user" 
                      ? "bg-primary text-primary-foreground" 
                      : "bg-gradient-to-br from-primary to-accent"
                  )}>
                    {msg.role === "user" ? "U" : <Sparkles className="w-5 h-5 text-white" />}
                  </div>
                  <div className={cn(
                    "max-w-[80%] rounded-2xl p-4",
                    msg.role === "user" 
                      ? "bg-primary text-primary-foreground" 
                      : "bg-secondary/50"
                  )}>
                    <p className="whitespace-pre-wrap">{msg.content}</p>
                  </div>
                </div>
              ))
            )}
            
            {isLoading && (
              <div className="flex gap-4 animate-fade-in">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center flex-shrink-0">
                  <Sparkles className="w-5 h-5 text-white" />
                </div>
                <div className="bg-secondary/50 rounded-2xl p-4">
                  <Loader2 className="w-5 h-5 animate-spin" />
                </div>
              </div>
            )}
          </div>

          {/* Input Area */}
          <form onSubmit={handleSubmit} className="p-4 border-t border-border/50">
            <div className="flex gap-3">
              <Button type="button" variant="outline" size="icon" className="flex-shrink-0">
                <Image className="w-5 h-5" />
              </Button>
              <Textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type your question here..."
                className="min-h-[52px] max-h-32 resize-none bg-secondary/30"
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    handleSubmit(e);
                  }
                }}
              />
              <Button 
                type="submit" 
                size="icon" 
                disabled={!input.trim() || isLoading}
                className="flex-shrink-0 bg-gradient-to-r from-primary to-accent hover:opacity-90"
              >
                <Send className="w-5 h-5" />
              </Button>
            </div>
          </form>
        </div>
      </main>
    </div>
  );
};

export default DoubtSolver;
