import { useState } from "react";
import { useNavigate } from "react-router-dom";
import DashboardNav from "@/components/DashboardNav";
import FloatingElements from "@/components/FloatingElements";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { Gamepad2, Trophy, Flame, Star, Zap, ArrowLeft, Check, X } from "lucide-react";

const categories = [
  { name: "Mathematics", icon: "📐", color: "from-neon-blue to-neon-cyan" },
  { name: "Science", icon: "🔬", color: "from-neon-green to-neon-cyan" },
  { name: "Programming", icon: "💻", color: "from-neon-purple to-neon-pink" },
  { name: "History", icon: "📜", color: "from-neon-orange to-neon-pink" },
  { name: "Languages", icon: "🌍", color: "from-neon-blue to-neon-purple" },
  { name: "General Knowledge", icon: "🧠", color: "from-neon-pink to-neon-orange" },
];

const sampleQuestions = [
  {
    question: "What is the output of: console.log(typeof null)?",
    options: ["null", "undefined", "object", "string"],
    correct: 2,
  },
  {
    question: "Which data structure uses LIFO?",
    options: ["Queue", "Stack", "Array", "Linked List"],
    correct: 1,
  },
  {
    question: "What does CSS stand for?",
    options: ["Computer Style Sheets", "Cascading Style Sheets", "Creative Style Sheets", "Colorful Style Sheets"],
    correct: 1,
  },
];

const Quiz = () => {
  const navigate = useNavigate();
  const [gameState, setGameState] = useState<"menu" | "playing" | "results">("menu");
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [score, setScore] = useState(0);
  const [answers, setAnswers] = useState<boolean[]>([]);

  const handleLogout = () => navigate("/");

  const startQuiz = () => {
    setGameState("playing");
    setCurrentQuestion(0);
    setSelectedAnswer(null);
    setScore(0);
    setAnswers([]);
  };

  const handleAnswer = (index: number) => {
    if (selectedAnswer !== null) return;
    
    setSelectedAnswer(index);
    const isCorrect = index === sampleQuestions[currentQuestion].correct;
    
    if (isCorrect) {
      setScore(score + 100);
    }
    setAnswers([...answers, isCorrect]);

    setTimeout(() => {
      if (currentQuestion < sampleQuestions.length - 1) {
        setCurrentQuestion(currentQuestion + 1);
        setSelectedAnswer(null);
      } else {
        setGameState("results");
      }
    }, 1500);
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
              <Gamepad2 className="w-8 h-8" />
              Gamified Quiz
            </h1>
            <p className="text-muted-foreground">Test your knowledge and earn XP!</p>
          </div>
        </div>

        {/* Game Stats Bar */}
        <div className="flex flex-wrap gap-4 mb-8">
          <div className="glass-card px-4 py-2 flex items-center gap-2">
            <Flame className="w-5 h-5 text-neon-orange" />
            <span className="font-bold">7 Day Streak</span>
          </div>
          <div className="glass-card px-4 py-2 flex items-center gap-2">
            <Trophy className="w-5 h-5 text-neon-purple" />
            <span className="font-bold">1,250 XP</span>
          </div>
          <div className="glass-card px-4 py-2 flex items-center gap-2">
            <Star className="w-5 h-5 text-neon-cyan" />
            <span className="font-bold">12 Badges</span>
          </div>
        </div>

        {/* Menu State */}
        {gameState === "menu" && (
          <div className="animate-fade-in">
            <h2 className="font-display text-xl font-semibold mb-6">Choose a Category</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
              {categories.map((cat) => (
                <button
                  key={cat.name}
                  onClick={startQuiz}
                  className={cn(
                    "glass-card p-6 text-left group hover:scale-105 transition-all duration-300",
                    "hover:shadow-lg hover:shadow-primary/20"
                  )}
                >
                  <div className={cn("w-12 h-12 rounded-xl bg-gradient-to-br flex items-center justify-center text-2xl mb-3", cat.color)}>
                    {cat.icon}
                  </div>
                  <h3 className="font-semibold text-lg group-hover:text-primary transition-colors">{cat.name}</h3>
                  <p className="text-sm text-muted-foreground mt-1">10 questions • 5 min</p>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Playing State */}
        {gameState === "playing" && (
          <div className="max-w-2xl mx-auto animate-fade-in">
            {/* Progress */}
            <div className="mb-8">
              <div className="flex justify-between text-sm text-muted-foreground mb-2">
                <span>Question {currentQuestion + 1} of {sampleQuestions.length}</span>
                <span className="flex items-center gap-1">
                  <Zap className="w-4 h-4 text-neon-purple" />
                  {score} XP
                </span>
              </div>
              <div className="h-2 bg-secondary rounded-full overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-primary to-accent transition-all duration-500"
                  style={{ width: `${((currentQuestion + 1) / sampleQuestions.length) * 100}%` }}
                />
              </div>
            </div>

            {/* Question Card */}
            <div className="glass-card p-8 mb-6">
              <h2 className="text-xl font-semibold mb-6">{sampleQuestions[currentQuestion].question}</h2>
              
              <div className="space-y-3">
                {sampleQuestions[currentQuestion].options.map((option, index) => {
                  const isSelected = selectedAnswer === index;
                  const isCorrect = index === sampleQuestions[currentQuestion].correct;
                  const showResult = selectedAnswer !== null;
                  
                  return (
                    <button
                      key={index}
                      onClick={() => handleAnswer(index)}
                      disabled={selectedAnswer !== null}
                      className={cn(
                        "w-full p-4 rounded-xl text-left transition-all duration-300",
                        "border-2",
                        showResult && isCorrect && "border-neon-green bg-neon-green/10",
                        showResult && isSelected && !isCorrect && "border-destructive bg-destructive/10",
                        !showResult && "border-border hover:border-primary hover:bg-primary/5",
                        !showResult && "hover:scale-[1.02]"
                      )}
                    >
                      <div className="flex items-center justify-between">
                        <span>{option}</span>
                        {showResult && isCorrect && <Check className="w-5 h-5 text-neon-green" />}
                        {showResult && isSelected && !isCorrect && <X className="w-5 h-5 text-destructive" />}
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>
          </div>
        )}

        {/* Results State */}
        {gameState === "results" && (
          <div className="max-w-md mx-auto text-center animate-fade-in">
            <div className="glass-card p-8">
              <div className="w-20 h-20 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center mx-auto mb-6">
                <Trophy className="w-10 h-10 text-white" />
              </div>
              
              <h2 className="font-display text-3xl font-bold mb-2">Quiz Complete!</h2>
              <p className="text-muted-foreground mb-6">Great job on completing the quiz!</p>
              
              <div className="grid grid-cols-2 gap-4 mb-8">
                <div className="bg-secondary/50 rounded-xl p-4">
                  <p className="text-3xl font-bold text-primary">{score}</p>
                  <p className="text-sm text-muted-foreground">XP Earned</p>
                </div>
                <div className="bg-secondary/50 rounded-xl p-4">
                  <p className="text-3xl font-bold text-neon-green">
                    {answers.filter(a => a).length}/{sampleQuestions.length}
                  </p>
                  <p className="text-sm text-muted-foreground">Correct</p>
                </div>
              </div>
              
              <div className="flex gap-4">
                <Button variant="outline" className="flex-1" onClick={() => setGameState("menu")}>
                  Back to Menu
                </Button>
                <Button className="flex-1" onClick={startQuiz}>
                  Play Again
                </Button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default Quiz;
