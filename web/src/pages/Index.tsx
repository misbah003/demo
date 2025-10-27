import DashboardHeader from "@/components/DashboardHeader";
import MetricsCards from "@/components/MetricsCards";
import PredictiveChart from "@/components/PredictiveChart";
import ComplianceRisk from "@/components/ComplianceRisk";
import DocumentProcessor from "@/components/DocumentProcessor";
import VATRefundPredictor from "@/components/VATRefundPredictor";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import { BarChart3, FileText, ArrowRight } from "lucide-react";
import dashboardBg from "@/assets/dashboard-bg.jpg";

const Index = () => {
  const navigate = useNavigate();
  return (
    <div className="min-h-screen bg-background relative">
      {/* Background */}
      <div 
        className="absolute inset-0 opacity-5 bg-cover bg-center bg-no-repeat"
        style={{ backgroundImage: `url(${dashboardBg})` }}
      />
      
      {/* Content */}
      <div className="relative z-10">
        <DashboardHeader />
        
        <main className="px-6 py-8 space-y-8">
          {/* Hero Section */}
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-foreground mb-4 bg-gradient-primary bg-clip-text text-transparent">
              AI-Powered Tax Intelligence
            </h1>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              Transform tax compliance with predictive analytics, automated workflows, and intelligent document processing
            </p>
          </div>

          {/* Key Metrics */}
          <MetricsCards />

          {/* Main Dashboard Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Primary Chart - Spans 2 columns */}
            <div className="lg:col-span-2">
              <PredictiveChart />
            </div>
            
            {/* Compliance Risk */}
            <div className="lg:col-span-1">
              <ComplianceRisk />
            </div>
          </div>

          {/* AI Tools Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <DocumentProcessor />
            <VATRefundPredictor />
          </div>

          {/* Explainability Features Section */}
          <div className="bg-gradient-to-br from-blue-50 to-purple-50 dark:from-blue-950 dark:to-purple-950 rounded-lg border border-blue-200 dark:border-blue-800 p-8 mt-8">
            <div className="max-w-4xl mx-auto">
              <div className="text-center mb-8">
                <h2 className="text-3xl font-bold text-foreground mb-3">
                  🔍 Understand Your AI
                </h2>
                <p className="text-lg text-muted-foreground">
                  Deep dive into model decisions with explainability analysis and comprehensive reports
                </p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Dashboard Card */}
                <div className="bg-white dark:bg-slate-900 rounded-lg p-6 border border-blue-200 dark:border-blue-800 hover:shadow-lg transition-shadow">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="text-xl font-semibold text-foreground mb-2">
                        Advanced AI Interpretation
                      </h3>
                      <p className="text-sm text-muted-foreground">
                        Visualize feature contributions and understand model predictions with interactive SHAP analysis
                      </p>
                    </div>
                    <BarChart3 className="w-6 h-6 text-blue-500 flex-shrink-0" />
                  </div>
                  <Button 
                    onClick={() => navigate("/explainability?tab=dashboard")}
                    className="w-full bg-blue-600 hover:bg-blue-700 text-white"
                  >
                    View Dashboard
                    <ArrowRight className="ml-2 w-4 h-4" />
                  </Button>
                </div>

                {/* Reports Card */}
                <div className="bg-white dark:bg-slate-900 rounded-lg p-6 border border-purple-200 dark:border-purple-800 hover:shadow-lg transition-shadow">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="text-xl font-semibold text-foreground mb-2">
                        Explainability Reports
                      </h3>
                      <p className="text-sm text-muted-foreground">
                        Generate professional reports in JSON, HTML, and PDF formats for predictions and analysis
                      </p>
                    </div>
                    <FileText className="w-6 h-6 text-purple-500 flex-shrink-0" />
                  </div>
                  <Button 
                    onClick={() => navigate("/explainability?tab=reports")}
                    className="w-full bg-purple-600 hover:bg-purple-700 text-white"
                  >
                    Manage Reports
                    <ArrowRight className="ml-2 w-4 h-4" />
                  </Button>
                </div>
              </div>

              <div className="mt-6 p-4 bg-blue-100 dark:bg-blue-900 rounded border border-blue-300 dark:border-blue-700">
                <p className="text-sm text-blue-900 dark:text-blue-100">
                  ✨ <strong>New Features:</strong> Generate comprehensive explainability reports, manage report history, and download in multiple formats
                </p>
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="text-center pt-8 border-t border-border/50">
            <p className="text-sm text-muted-foreground">
              Powered by Machine Learning • Real-time Analytics • Explainable AI
            </p>
          </div>
        </main>
      </div>
    </div>
  );
};

export default Index;
