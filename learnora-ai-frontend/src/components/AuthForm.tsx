import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { cn } from "@/lib/utils";
import { Eye, EyeOff, Mail, Lock, User, Loader2 } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { authService } from "@/api/services/authService";

interface AuthFormProps {
  onSuccess: () => void;
}

const AuthForm = ({ onSuccess }: AuthFormProps) => {
  const [isLogin, setIsLogin] = useState(true);
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();
  
  const [formData, setFormData] = useState({
    full_name: "",
    username: "",
    email: "",
    password: "",
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      if (isLogin) {
        // Backend Login
        await authService.login({
          email: formData.email,
          password: formData.password,
        });
        
        toast({
          title: "Welcome back!",
          description: "You've successfully logged in to Learnora AI",
        });
      } else {
        // Backend Register
        await authService.register({
          email: formData.email,
          username: formData.username,
          password: formData.password,
          full_name: formData.full_name,
        });
        
        toast({
          title: "Account created!",
          description: "Your account has been created. Welcome to Learnora AI!",
        });
      }
      
      onSuccess();
    } catch (error: any) {
      console.error("Auth error:", error);
      console.error("Error details:", JSON.stringify(error, null, 2));
      
      // Extract the actual error message from nested structure
      let errorMessage = "Something went wrong. Please try again.";
      
      if (error?.error?.message) {
        errorMessage = error.error.message;
      } else if (error?.detail) {
        errorMessage = error.detail;
      } else if (error?.message) {
        errorMessage = error.message;
      }
      
      toast({
        title: "Error",
        description: errorMessage,
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto">
      {/* Tab switcher */}
      <div className="flex mb-8 p-1 bg-secondary/50 rounded-xl backdrop-blur-sm">
        <button
          type="button"
          onClick={() => setIsLogin(true)}
          className={cn(
            "flex-1 py-3 px-4 rounded-lg font-medium transition-all duration-300",
            isLogin 
              ? "bg-primary text-primary-foreground shadow-lg shadow-primary/25" 
              : "text-muted-foreground hover:text-foreground"
          )}
        >
          Sign In
        </button>
        <button
          type="button"
          onClick={() => setIsLogin(false)}
          className={cn(
            "flex-1 py-3 px-4 rounded-lg font-medium transition-all duration-300",
            !isLogin 
              ? "bg-primary text-primary-foreground shadow-lg shadow-primary/25" 
              : "text-muted-foreground hover:text-foreground"
          )}
        >
          Sign Up
        </button>
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-5">
        {/* Full Name field (only for signup) */}
        {!isLogin && (
          <div className="space-y-2 animate-fade-in">
            <Label htmlFor="full_name" className="text-foreground">Full Name</Label>
            <div className="relative">
              <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
              <Input
                id="full_name"
                type="text"
                placeholder="Enter your full name"
                value={formData.full_name}
                onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                className="pl-11 h-12 bg-secondary/50 border-border/50 focus:border-primary focus:ring-primary/20"
                required={!isLogin}
              />
            </div>
          </div>
        )}

        {/* Username field (only for signup) */}
        {!isLogin && (
          <div className="space-y-2 animate-fade-in">
            <Label htmlFor="username" className="text-foreground">Username</Label>
            <div className="relative">
              <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
              <Input
                id="username"
                type="text"
                placeholder="Choose a username"
                value={formData.username}
                onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                className="pl-11 h-12 bg-secondary/50 border-border/50 focus:border-primary focus:ring-primary/20"
                required={!isLogin}
              />
            </div>
          </div>
        )}

        {/* Email field */}
        <div className="space-y-2">
          <Label htmlFor="email" className="text-foreground">Email</Label>
          <div className="relative">
            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
            <Input
              id="email"
              type="email"
              placeholder="you@example.com"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              className="pl-11 h-12 bg-secondary/50 border-border/50 focus:border-primary focus:ring-primary/20"
              required
            />
          </div>
        </div>

        {/* Password field */}
        <div className="space-y-2">
          <Label htmlFor="password" className="text-foreground">Password</Label>
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
            <Input
              id="password"
              type={showPassword ? "text" : "password"}
              placeholder="••••••••"
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              className="pl-11 pr-11 h-12 bg-secondary/50 border-border/50 focus:border-primary focus:ring-primary/20"
              required
              minLength={8}
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
            >
              {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {/* Forgot password link */}
        {isLogin && (
          <div className="text-right">
            <button type="button" className="text-sm text-primary hover:text-primary/80 transition-colors">
              Forgot password?
            </button>
          </div>
        )}

        {/* Submit button */}
        <Button
          type="submit"
          disabled={isLoading}
          className={cn(
            "w-full h-12 text-base font-semibold",
            "bg-gradient-to-r from-primary to-primary/80",
            "hover:from-primary/90 hover:to-primary/70",
            "shadow-lg shadow-primary/25 hover:shadow-xl hover:shadow-primary/30",
            "transition-all duration-300"
          )}
        >
          {isLoading ? (
            <>
              <Loader2 className="w-5 h-5 mr-2 animate-spin" />
              {isLogin ? "Signing in..." : "Creating account..."}
            </>
          ) : (
            isLogin ? "Sign In" : "Create Account"
          )}
        </Button>

        {/* Divider */}
        <div className="relative my-6">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-border/50" />
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-4 bg-background text-muted-foreground">or continue with</span>
          </div>
        </div>

        {/* Social login buttons */}
        <div className="grid grid-cols-2 gap-4">
          <Button
            type="button"
            variant="outline"
            className="h-12 bg-secondary/30 border-border/50 hover:bg-secondary/50 hover:border-primary/50"
            disabled
          >
            <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24">
              <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            Google
          </Button>
          <Button
            type="button"
            variant="outline"
            className="h-12 bg-secondary/30 border-border/50 hover:bg-secondary/50 hover:border-primary/50"
            disabled
          >
            <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>
            GitHub
          </Button>
        </div>
      </form>

      {/* Terms */}
      <p className="mt-6 text-center text-sm text-muted-foreground">
        By continuing, you agree to our{" "}
        <a href="#" className="text-primary hover:underline">Terms of Service</a>
        {" "}and{" "}
        <a href="#" className="text-primary hover:underline">Privacy Policy</a>
      </p>
    </div>
  );
};

export default AuthForm;