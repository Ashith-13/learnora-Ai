import { useState } from "react";
import { useNavigate } from "react-router-dom";
import DashboardNav from "@/components/DashboardNav";
import FloatingElements from "@/components/FloatingElements";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { ArrowLeft, FileText, Download, Sparkles, Plus, Trash2 } from "lucide-react";
import { cn } from "@/lib/utils";

const ResumeBuilder = () => {
  const navigate = useNavigate();
  const handleLogout = () => navigate("/");

  const [resume, setResume] = useState({
    name: "",
    email: "",
    phone: "",
    summary: "",
    experience: [{ title: "", company: "", duration: "", description: "" }],
    education: [{ degree: "", institution: "", year: "" }],
    skills: "",
  });

  const addExperience = () => {
    setResume({
      ...resume,
      experience: [...resume.experience, { title: "", company: "", duration: "", description: "" }],
    });
  };

  const addEducation = () => {
    setResume({
      ...resume,
      education: [...resume.education, { degree: "", institution: "", year: "" }],
    });
  };

  return (
    <div className="min-h-screen bg-background dark">
      <FloatingElements />
      <DashboardNav onLogout={handleLogout} />

      <main className="relative z-10 container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="icon" onClick={() => navigate("/dashboard")}>
              <ArrowLeft className="w-5 h-5" />
            </Button>
            <div>
              <h1 className="font-display text-3xl font-bold gradient-text flex items-center gap-3">
                <FileText className="w-8 h-8" />
                AI Resume Builder
              </h1>
              <p className="text-muted-foreground">Create professional resumes with AI assistance</p>
            </div>
          </div>
          <div className="flex gap-3">
            <Button variant="outline" className="gap-2">
              <Sparkles className="w-4 h-4" />
              AI Enhance
            </Button>
            <Button className="gap-2 bg-gradient-to-r from-primary to-accent">
              <Download className="w-4 h-4" />
              Download PDF
            </Button>
          </div>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Form */}
          <div className="space-y-6">
            {/* Personal Info */}
            <div className="glass-card p-6">
              <h2 className="font-display text-lg font-semibold mb-4">Personal Information</h2>
              <div className="grid gap-4">
                <div>
                  <Label>Full Name</Label>
                  <Input 
                    value={resume.name}
                    onChange={(e) => setResume({ ...resume, name: e.target.value })}
                    placeholder="John Doe"
                    className="bg-secondary/30"
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label>Email</Label>
                    <Input 
                      value={resume.email}
                      onChange={(e) => setResume({ ...resume, email: e.target.value })}
                      placeholder="john@example.com"
                      className="bg-secondary/30"
                    />
                  </div>
                  <div>
                    <Label>Phone</Label>
                    <Input 
                      value={resume.phone}
                      onChange={(e) => setResume({ ...resume, phone: e.target.value })}
                      placeholder="+1 234 567 890"
                      className="bg-secondary/30"
                    />
                  </div>
                </div>
                <div>
                  <Label>Professional Summary</Label>
                  <Textarea 
                    value={resume.summary}
                    onChange={(e) => setResume({ ...resume, summary: e.target.value })}
                    placeholder="Brief summary of your professional background..."
                    className="bg-secondary/30 min-h-[100px]"
                  />
                </div>
              </div>
            </div>

            {/* Experience */}
            <div className="glass-card p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="font-display text-lg font-semibold">Experience</h2>
                <Button variant="outline" size="sm" onClick={addExperience} className="gap-1">
                  <Plus className="w-4 h-4" /> Add
                </Button>
              </div>
              <div className="space-y-4">
                {resume.experience.map((exp, i) => (
                  <div key={i} className="p-4 bg-secondary/30 rounded-xl space-y-3">
                    <div className="grid grid-cols-2 gap-3">
                      <Input 
                        placeholder="Job Title"
                        value={exp.title}
                        onChange={(e) => {
                          const updated = [...resume.experience];
                          updated[i].title = e.target.value;
                          setResume({ ...resume, experience: updated });
                        }}
                      />
                      <Input 
                        placeholder="Company"
                        value={exp.company}
                        onChange={(e) => {
                          const updated = [...resume.experience];
                          updated[i].company = e.target.value;
                          setResume({ ...resume, experience: updated });
                        }}
                      />
                    </div>
                    <Input 
                      placeholder="Duration (e.g., 2020 - Present)"
                      value={exp.duration}
                      onChange={(e) => {
                        const updated = [...resume.experience];
                        updated[i].duration = e.target.value;
                        setResume({ ...resume, experience: updated });
                      }}
                    />
                    <Textarea 
                      placeholder="Description of your role..."
                      value={exp.description}
                      onChange={(e) => {
                        const updated = [...resume.experience];
                        updated[i].description = e.target.value;
                        setResume({ ...resume, experience: updated });
                      }}
                    />
                  </div>
                ))}
              </div>
            </div>

            {/* Skills */}
            <div className="glass-card p-6">
              <h2 className="font-display text-lg font-semibold mb-4">Skills</h2>
              <Textarea 
                value={resume.skills}
                onChange={(e) => setResume({ ...resume, skills: e.target.value })}
                placeholder="React, TypeScript, Node.js, Python..."
                className="bg-secondary/30"
              />
            </div>
          </div>

          {/* Preview */}
          <div className="glass-card p-8 sticky top-24 h-fit">
            <h2 className="font-display text-lg font-semibold mb-6">Preview</h2>
            <div className="bg-white text-gray-900 p-8 rounded-xl shadow-xl min-h-[600px]">
              <div className="border-b-2 border-gray-200 pb-4 mb-4">
                <h1 className="text-2xl font-bold text-gray-900">{resume.name || "Your Name"}</h1>
                <p className="text-gray-600 text-sm">
                  {resume.email || "email@example.com"} • {resume.phone || "+1 234 567 890"}
                </p>
              </div>
              
              {resume.summary && (
                <div className="mb-4">
                  <h2 className="text-sm font-bold text-gray-700 uppercase mb-2">Summary</h2>
                  <p className="text-sm text-gray-600">{resume.summary}</p>
                </div>
              )}
              
              {resume.experience.some(e => e.title) && (
                <div className="mb-4">
                  <h2 className="text-sm font-bold text-gray-700 uppercase mb-2">Experience</h2>
                  {resume.experience.filter(e => e.title).map((exp, i) => (
                    <div key={i} className="mb-3">
                      <div className="flex justify-between">
                        <p className="font-semibold text-sm">{exp.title}</p>
                        <p className="text-xs text-gray-500">{exp.duration}</p>
                      </div>
                      <p className="text-sm text-gray-600">{exp.company}</p>
                      <p className="text-xs text-gray-500 mt-1">{exp.description}</p>
                    </div>
                  ))}
                </div>
              )}
              
              {resume.skills && (
                <div>
                  <h2 className="text-sm font-bold text-gray-700 uppercase mb-2">Skills</h2>
                  <p className="text-sm text-gray-600">{resume.skills}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default ResumeBuilder;
