import DashboardHeader from "@/components/DashboardHeader";
import MetricsCards from "@/components/MetricsCards";
import PredictiveChart from "@/components/PredictiveChart";
import ComplianceRisk from "@/components/ComplianceRisk";
import DocumentProcessor from "@/components/DocumentProcessor";
import VATRefundPredictor from "@/components/VATRefundPredictor";
import dashboardBg from "@/assets/dashboard-bg.jpg";

const Index = () => {
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
