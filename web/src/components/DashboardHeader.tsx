import { Bell, Search, Settings, User, Sun, Moon, LogOut, UserCircle, Mail, HelpCircle, Shield, FileText, BarChart3 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useTheme } from "next-themes";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/hooks/useAuth";
import { useProfile } from "@/hooks/useProfile";
import { useState } from "react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { useToast } from "@/hooks/use-toast";

const DashboardHeader = () => {
  const { theme, setTheme } = useTheme();
  const navigate = useNavigate();
  const { toast } = useToast();
  const { user, signOut } = useAuth();
  const { profile } = useProfile();
  const [searchQuery, setSearchQuery] = useState("");

  const handleSignOut = async () => {
    await signOut();
    toast({ title: "Logged out", description: "You have been signed out." });
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    const query = searchQuery.toLowerCase().trim();

    if (!query) return;

    // Define search mappings for navigation
    const searchMappings: Record<string, string> = {
      'document': '/documents',
      'documents': '/documents',
      'upload': '/documents',
      'file': '/documents',
      'files': '/documents',
      'explainability': '/explainability',
      'explain': '/explainability',
      'shap': '/explainability',
      'lime': '/explainability',
      'model': '/explainability',
      'analysis': '/explainability',
      'reports': '/explainability?tab=reports',
      'dashboard': '/',
      'home': '/',
      'vat': '/vat-predictor',
      'predictor': '/vat-predictor',
      'prediction': '/vat-predictor',
      'refund': '/vat-predictor',
      'compliance': '/',
      'risk': '/',
      'assessment': '/',
      'profile': '/profile',
      'settings': '/profile',
      'notification': '/notifications',
      'notifications': '/notifications',
      'help': '/profile', // Could be a dedicated help page
      'support': '/profile'
    };

    // Check for exact matches first
    if (searchMappings[query]) {
      navigate(searchMappings[query]);
      setSearchQuery("");
      return;
    }

    // Check for partial matches
    for (const [key, path] of Object.entries(searchMappings)) {
      if (query.includes(key) || key.includes(query)) {
        navigate(path);
        setSearchQuery("");
        return;
      }
    }

    // If no match found, show toast
    toast({
      title: "Search not found",
      description: `No page found for "${query}". Try searching for: documents, explainability, dashboard, vat predictor, profile`,
      variant: "destructive"
    });
  };

  return (
    <header className="bg-card/60 backdrop-blur-xl border-b border-border/50 px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2 cursor-pointer" onClick={() => navigate("/")}>
            <div className="h-8 w-8 bg-gradient-primary rounded-lg flex items-center justify-center">
              <span className="text-primary-foreground font-bold text-sm">AI</span>
            </div>
            <div>
              <h1 className="text-xl font-bold text-foreground leading-relaxed hover:text-primary transition-smooth">Tax Intelligence</h1>
              <p className="text-xs text-muted-foreground">Predictive Analytics & Automation</p>
            </div>
          </div>
        </div>
        
        <div className="flex items-center space-x-4">
          <form onSubmit={handleSearch} className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
            <Input
              placeholder="Search insights, documents..."
              className="pl-10 w-64 bg-background/50"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </form>
          
          <Button variant="ghost" size="icon" onClick={() => navigate("/notifications")}>
            <Bell className="h-4 w-4" />
          </Button>
          
          <Button 
            variant="ghost" 
            size="icon"
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          >
            {theme === "dark" ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
          </Button>
          
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon" className="h-8 w-8 rounded-full">
                <Avatar className="h-8 w-8">
                  <AvatarImage src={profile?.avatar_url || "/placeholder.svg"} alt="User" />
                  <AvatarFallback>
                    {profile?.full_name 
                      ? profile.full_name.split(' ').map(n => n[0]).join('').toUpperCase()
                      : user?.email?.charAt(0).toUpperCase() || 'U'}
                  </AvatarFallback>
                </Avatar>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-56">
              <DropdownMenuLabel className="font-normal">
                <div className="flex flex-col space-y-1">
                  <p className="text-sm font-medium leading-none">
                    {profile?.full_name || user?.email || 'User'}
                  </p>
                  <p className="text-xs leading-none text-muted-foreground">
                    {profile?.position || user?.email}
                  </p>
                </div>
              </DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => navigate("/documents")}>
                <FileText className="mr-2 h-4 w-4" />
                <span>My Documents</span>
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => navigate("/explainability")}>
                <BarChart3 className="mr-2 h-4 w-4" />
                <span>Model Explainability</span>
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => navigate("/profile")}>
                <UserCircle className="mr-2 h-4 w-4" />
                <span>Profile & Settings</span>
              </DropdownMenuItem>
              <DropdownMenuItem>
                <HelpCircle className="mr-2 h-4 w-4" />
                <span>Help & Support</span>
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem onSelect={handleSignOut}>
                <LogOut className="mr-2 h-4 w-4" />
                <span>Log out</span>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </header>
  );
};

export default DashboardHeader;