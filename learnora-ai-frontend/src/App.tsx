import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Index from "./pages/Index";
import Auth from "./pages/Auth";
import Dashboard from "./pages/Dashboard";
import Quiz from "./pages/Quiz";
import DoubtSolver from "./pages/DoubtSolver";
import CareerScore from "./pages/CareerScore";
import ResumeBuilder from "./pages/ResumeBuilder";
import Jobs from "./pages/Jobs";
import VideoGenerator from "./pages/VideoGenerator";
import ARLabs from "./pages/ARLabs";
import Roadmaps from "./pages/Roadmaps";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Index />} />
          <Route path="/auth" element={<Auth />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/quiz" element={<Quiz />} />
          <Route path="/doubt-solver" element={<DoubtSolver />} />
          <Route path="/career-score" element={<CareerScore />} />
          <Route path="/resume-builder" element={<ResumeBuilder />} />
          <Route path="/jobs" element={<Jobs />} />
          <Route path="/video-generator" element={<VideoGenerator />} />
          <Route path="/ar-labs" element={<ARLabs />} />
          <Route path="/roadmaps" element={<Roadmaps />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
