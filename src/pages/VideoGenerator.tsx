import { useState } from "react";
import { useNavigate } from "react-router-dom";
import DashboardNav from "@/components/DashboardNav";
import FloatingElements from "@/components/FloatingElements";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { ArrowLeft, Video, Sparkles, Play, Clock, Download, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

const sampleVideos = [
  { id: 1, title: "Introduction to Machine Learning", duration: "5:30", thumbnail: "🤖" },
  { id: 2, title: "Understanding Quantum Physics", duration: "8:45", thumbnail: "⚛️" },
  { id: 3, title: "Web Development Basics", duration: "6:15", thumbnail: "💻" },
];

const VideoGenerator = () => {
  const navigate = useNavigate();
  const [topic, setTopic] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);

  const handleLogout = () => navigate("/");

  const handleGenerate = () => {
    if (!topic.trim()) return;
    setIsGenerating(true);
    setTimeout(() => setIsGenerating(false), 3000);
  };

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
              <Video className="w-8 h-8" />
              AI Video Generator
            </h1>
            <p className="text-muted-foreground">Create educational videos from any topic</p>
          </div>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Generator */}
          <div>
            <div className="glass-card p-6 mb-6">
              <h2 className="font-display text-xl font-semibold mb-4">Create New Video</h2>
              <div className="space-y-4">
                <div>
                  <label className="text-sm text-muted-foreground mb-2 block">Topic</label>
                  <Input 
                    placeholder="e.g., How does photosynthesis work?"
                    value={topic}
                    onChange={(e) => setTopic(e.target.value)}
                    className="bg-secondary/30"
                  />
                </div>
                <div>
                  <label className="text-sm text-muted-foreground mb-2 block">Additional Details (Optional)</label>
                  <Textarea 
                    placeholder="Add specific points you want covered..."
                    className="bg-secondary/30 min-h-[100px]"
                  />
                </div>
                <div className="flex gap-4">
                  <select className="flex-1 px-4 py-2 rounded-lg bg-secondary/30 border border-border">
                    <option>5 minutes</option>
                    <option>10 minutes</option>
                    <option>15 minutes</option>
                  </select>
                  <select className="flex-1 px-4 py-2 rounded-lg bg-secondary/30 border border-border">
                    <option>Beginner</option>
                    <option>Intermediate</option>
                    <option>Advanced</option>
                  </select>
                </div>
                <Button 
                  className="w-full gap-2 bg-gradient-to-r from-primary to-accent"
                  onClick={handleGenerate}
                  disabled={isGenerating || !topic.trim()}
                >
                  {isGenerating ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      Generating...
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-5 h-5" />
                      Generate Video
                    </>
                  )}
                </Button>
              </div>
            </div>

            {/* Generation Progress */}
            {isGenerating && (
              <div className="glass-card p-6 animate-fade-in">
                <h3 className="font-semibold mb-4">Generating your video...</h3>
                <div className="space-y-3">
                  {["Analyzing topic", "Creating script", "Generating visuals", "Adding narration"].map((step, i) => (
                    <div key={step} className="flex items-center gap-3">
                      <div className={cn(
                        "w-6 h-6 rounded-full flex items-center justify-center text-sm",
                        i === 0 ? "bg-primary text-primary-foreground animate-pulse" : "bg-secondary text-muted-foreground"
                      )}>
                        {i + 1}
                      </div>
                      <span className={i === 0 ? "text-foreground" : "text-muted-foreground"}>{step}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Recent Videos */}
          <div>
            <h2 className="font-display text-xl font-semibold mb-4">Your Videos</h2>
            <div className="space-y-4">
              {sampleVideos.map((video, index) => (
                <div 
                  key={video.id}
                  className="glass-card p-4 flex gap-4 hover:border-primary/50 transition-all cursor-pointer animate-fade-in"
                  style={{ animationDelay: `${index * 100}ms` }}
                >
                  <div className="w-32 h-20 bg-gradient-to-br from-primary/20 to-accent/20 rounded-lg flex items-center justify-center text-4xl">
                    {video.thumbnail}
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold mb-1">{video.title}</h3>
                    <div className="flex items-center gap-4 text-sm text-muted-foreground">
                      <span className="flex items-center gap-1">
                        <Clock className="w-4 h-4" />
                        {video.duration}
                      </span>
                    </div>
                    <div className="flex gap-2 mt-3">
                      <Button size="sm" variant="outline" className="gap-1">
                        <Play className="w-4 h-4" /> Play
                      </Button>
                      <Button size="sm" variant="outline" className="gap-1">
                        <Download className="w-4 h-4" /> Download
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default VideoGenerator;
