import { useState } from "react";
import { useNavigate } from "react-router-dom";
import DashboardNav from "@/components/DashboardNav";
import FloatingElements from "@/components/FloatingElements";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, Briefcase, MapPin, Clock, DollarSign, Search, Building, Sparkles, Heart, ExternalLink } from "lucide-react";
import { cn } from "@/lib/utils";

const jobs = [
  {
    id: 1,
    title: "Frontend Developer",
    company: "TechCorp Inc.",
    location: "San Francisco, CA",
    type: "Full-time",
    salary: "$80k - $120k",
    match: 95,
    skills: ["React", "TypeScript", "Tailwind"],
    posted: "2 days ago",
  },
  {
    id: 2,
    title: "Full Stack Engineer",
    company: "StartupXYZ",
    location: "Remote",
    type: "Full-time",
    salary: "$90k - $140k",
    match: 88,
    skills: ["Node.js", "React", "PostgreSQL"],
    posted: "1 week ago",
  },
  {
    id: 3,
    title: "Junior Developer",
    company: "InnovateTech",
    location: "New York, NY",
    type: "Full-time",
    salary: "$60k - $80k",
    match: 82,
    skills: ["JavaScript", "HTML/CSS", "Git"],
    posted: "3 days ago",
  },
  {
    id: 4,
    title: "React Native Developer",
    company: "MobileFirst Co.",
    location: "Austin, TX",
    type: "Contract",
    salary: "$70k - $100k",
    match: 78,
    skills: ["React Native", "TypeScript", "Mobile"],
    posted: "5 days ago",
  },
];

const Jobs = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState("");
  const [savedJobs, setSavedJobs] = useState<number[]>([]);

  const handleLogout = () => navigate("/");

  const toggleSave = (id: number) => {
    setSavedJobs(prev => 
      prev.includes(id) ? prev.filter(j => j !== id) : [...prev, id]
    );
  };

  const filteredJobs = jobs.filter(job => 
    job.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    job.company.toLowerCase().includes(searchQuery.toLowerCase())
  );

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
              <Briefcase className="w-8 h-8" />
              Job Recommendations
            </h1>
            <p className="text-muted-foreground">AI-matched jobs based on your skills and preferences</p>
          </div>
        </div>

        {/* Search */}
        <div className="glass-card p-4 mb-8">
          <div className="flex gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
              <Input 
                placeholder="Search jobs, companies..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 bg-secondary/30"
              />
            </div>
            <Button variant="outline">Filters</Button>
            <Button className="gap-2 bg-gradient-to-r from-primary to-accent">
              <Sparkles className="w-4 h-4" />
              AI Match
            </Button>
          </div>
        </div>

        {/* Job Listings */}
        <div className="space-y-4">
          {filteredJobs.map((job, index) => (
            <div 
              key={job.id}
              className="glass-card p-6 hover:border-primary/50 transition-all duration-300 animate-fade-in"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="font-display text-xl font-semibold hover:text-primary transition-colors cursor-pointer">
                        {job.title}
                      </h3>
                      <div className="flex items-center gap-2 text-muted-foreground mt-1">
                        <Building className="w-4 h-4" />
                        <span>{job.company}</span>
                      </div>
                    </div>
                    <Badge 
                      className={cn(
                        "font-semibold",
                        job.match >= 90 ? "bg-neon-green/20 text-neon-green" :
                        job.match >= 80 ? "bg-primary/20 text-primary" :
                        "bg-neon-orange/20 text-neon-orange"
                      )}
                    >
                      {job.match}% Match
                    </Badge>
                  </div>

                  <div className="flex flex-wrap gap-4 mt-4 text-sm text-muted-foreground">
                    <span className="flex items-center gap-1">
                      <MapPin className="w-4 h-4" />
                      {job.location}
                    </span>
                    <span className="flex items-center gap-1">
                      <Clock className="w-4 h-4" />
                      {job.type}
                    </span>
                    <span className="flex items-center gap-1">
                      <DollarSign className="w-4 h-4" />
                      {job.salary}
                    </span>
                  </div>

                  <div className="flex flex-wrap gap-2 mt-4">
                    {job.skills.map(skill => (
                      <Badge key={skill} variant="secondary">{skill}</Badge>
                    ))}
                  </div>
                </div>

                <div className="flex md:flex-col gap-2">
                  <Button className="flex-1 md:flex-none gap-2">
                    Apply <ExternalLink className="w-4 h-4" />
                  </Button>
                  <Button 
                    variant="outline" 
                    size="icon"
                    onClick={() => toggleSave(job.id)}
                    className={savedJobs.includes(job.id) ? "text-neon-pink border-neon-pink" : ""}
                  >
                    <Heart className={cn("w-5 h-5", savedJobs.includes(job.id) && "fill-current")} />
                  </Button>
                </div>
              </div>

              <p className="text-sm text-muted-foreground mt-4">Posted {job.posted}</p>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
};

export default Jobs;
