import React, { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import DashboardHeader from "@/components/DashboardHeader";
import EnhancedExplainabilityDashboard from "@/components/EnhancedExplainabilityDashboard";
import ExplainabilityReportViewer from "@/components/ExplainabilityReportViewer";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import dashboardBg from "@/assets/dashboard-bg.jpg";
import { useProcessedDocuments } from "@/hooks/useProcessedDocuments";
import { 
  BarChart3, FileText, Zap, Brain, BookOpen, TrendingUp, 
  ArrowRight, Lightbulb, Shield, Download, Settings 
} from "lucide-react";

const Explainability = () => {
  const [searchParams] = useSearchParams();
  const [activeTab, setActiveTab] = useState(() => searchParams.get("tab") || "dashboard");
  const [currentExplanationData, setCurrentExplanationData] = useState<any>(null);
  const [selectedDocumentId, setSelectedDocumentId] = useState<string>("");
  const [predictionDataForAnalysis, setPredictionDataForAnalysis] = useState<any>(null);
  
  const { documents, loading: docsLoading } = useProcessedDocuments();

  const handleAnalyzeDocument = (documentId: string): boolean => {
    if (!documentId) {
      alert('Please select a processed document first');
      return false;
    }

    const selectedDoc = documents.find((d) => d.id === documentId);
    if (selectedDoc) {
      // Prepare data for analysis
      const analysisData = {
        content: selectedDoc.filename || 'Unknown document',
        document_type: selectedDoc.type || 'unknown',
        classification: selectedDoc.classification,
        confidence: selectedDoc.confidence,
        entities: selectedDoc.entities,
        prediction: selectedDoc.classification,
      };
      setPredictionDataForAnalysis(analysisData);
      return true;
    }
    return false;
  };

  const handleTabChange = (tabName: string, documentId?: string) => {
    if (documentId) {
      const success = handleAnalyzeDocument(documentId);
      if (!success) return;
    }
    setActiveTab(tabName);
    // Scroll to tabs section smoothly - wait for state update
    setTimeout(() => {
      const tabsSection = document.querySelector('[role="tablist"]');
      if (tabsSection) {
        tabsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }, 300); // Increased delay to ensure state update completes
  };

  useEffect(() => {
    const tabParam = searchParams.get("tab");
    if (tabParam === "reports" || tabParam === "dashboard") {
      setActiveTab(tabParam);
    }
  }, [searchParams]);

  const generateReport = (data?: any) => {
    if (!data && !currentExplanationData) {
      alert('No explanation data available. Please generate explanations first.');
      return;
    }

    const reportData = data || currentExplanationData;
    const report = {
      filename: `explainability-report-${Date.now()}.json`,
      format: 'JSON',
      size: JSON.stringify(reportData).length,
      created: new Date().toISOString(),
      url: '', // Not used for local storage
      data: reportData
    };

    // Save to localStorage
    const existingReports = JSON.parse(localStorage.getItem('explainability-reports') || '[]');
    existingReports.push(report);
    localStorage.setItem('explainability-reports', JSON.stringify(existingReports));

    // Switch to reports tab
    setActiveTab('reports');
  };

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
            <h1 className="text-5xl font-bold text-foreground mb-4 bg-gradient-primary bg-clip-text text-transparent">
              🔬 Model Explainability
            </h1>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              Unlock the black box of AI with SHAP analysis, interactive dashboards, and comprehensive explainability reports
            </p>
          </div>

          {/* Main Features Section */}
          <div className="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-950 dark:to-indigo-950 rounded-lg border border-blue-200 dark:border-blue-800 p-8">
            <div className="max-w-6xl mx-auto">
              <div className="text-center mb-10">
                <h2 className="text-3xl font-bold text-foreground mb-3">
                  ✨ Advanced AI Interpretation
                </h2>
                <p className="text-lg text-muted-foreground">
                  Understand exactly how our models make decisions
                </p>
              </div>

              {/* Document Selector */}
              <div className="mb-8 p-4 bg-white dark:bg-slate-900 rounded-lg border border-blue-200 dark:border-blue-700">
                <label className="block text-sm font-medium text-foreground mb-2">
                  Select a processed document to analyze:
                </label>
                <Select value={selectedDocumentId} onValueChange={setSelectedDocumentId} disabled={docsLoading}>
                  <SelectTrigger className="w-full">
                    <SelectValue placeholder={docsLoading ? "Loading documents..." : "Choose a document..."} />
                  </SelectTrigger>
                  <SelectContent>
                    {documents.length === 0 && !docsLoading && (
                      <SelectItem value="none" disabled>No processed documents found</SelectItem>
                    )}
                    {documents.map((doc) => (
                      <SelectItem key={doc.id} value={doc.id}>
                        {doc.filename} - {doc.type} ({doc.classification})
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                {selectedDocumentId && documents.find(d => d.id === selectedDocumentId) && (
                  <p className="text-xs text-green-600 dark:text-green-400 mt-2">
                    ✓ Document selected and ready for analysis
                  </p>
                )}
              </div>

              {/* Feature Cards Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                {/* SHAP Card */}
                <div className="bg-white dark:bg-slate-900 rounded-lg p-6 border border-blue-200 dark:border-blue-800 hover:shadow-lg transition-shadow">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <Zap className="w-5 h-5 text-blue-600" />
                        <h3 className="text-xl font-semibold text-foreground">
                          SHAP Analysis
                        </h3>
                      </div>
                      <p className="text-sm text-muted-foreground">
                        SHapley Additive exPlanations for game-theory based feature importance analysis
                      </p>
                    </div>
                  </div>
                  <ul className="space-y-2 text-sm mb-4">
                    <li className="flex gap-2 text-muted-foreground"><span className="text-blue-600">✓</span> Feature importance rankings</li>
                    <li className="flex gap-2 text-muted-foreground"><span className="text-blue-600">✓</span> SHAP value decomposition</li>
                    <li className="flex gap-2 text-muted-foreground"><span className="text-blue-600">✓</span> Prediction force plots</li>
                  </ul>
                  <Button 
                    onClick={() => handleTabChange("dashboard", selectedDocumentId)}
                    disabled={!selectedDocumentId || docsLoading}
                    className="w-full bg-blue-600 hover:bg-blue-700 text-white disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Explore SHAP
                    <ArrowRight className="ml-2 w-4 h-4" />
                  </Button>
                </div>

                {/* LIME Card */}
                <div className="bg-white dark:bg-slate-900 rounded-lg p-6 border border-purple-200 dark:border-purple-800 hover:shadow-lg transition-shadow">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <Brain className="w-5 h-5 text-purple-600" />
                        <h3 className="text-xl font-semibold text-foreground">
                          LIME Interpretation
                        </h3>
                      </div>
                      <p className="text-sm text-muted-foreground">
                        Local Interpretable Model-agnostic Explanations for localized insights
                      </p>
                    </div>
                  </div>
                  <ul className="space-y-2 text-sm mb-4">
                    <li className="flex gap-2 text-muted-foreground"><span className="text-purple-600">✓</span> Local feature weights</li>
                    <li className="flex gap-2 text-muted-foreground"><span className="text-purple-600">✓</span> Model behavior interpretation</li>
                    <li className="flex gap-2 text-muted-foreground"><span className="text-purple-600">✓</span> Decision path analysis</li>
                  </ul>
                  <Button 
                    onClick={() => handleTabChange("dashboard", selectedDocumentId)}
                    disabled={!selectedDocumentId || docsLoading}
                    className="w-full bg-purple-600 hover:bg-purple-700 text-white disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Compare Methods
                    <ArrowRight className="ml-2 w-4 h-4" />
                  </Button>
                </div>
              </div>

              {/* Info Box */}
              <div className="mt-6 p-4 bg-blue-100 dark:bg-blue-900 rounded border border-blue-300 dark:border-blue-700">
                <p className="text-sm text-blue-900 dark:text-blue-100">
                  💡 <strong>Tip:</strong> Make a prediction from Documents or VAT Predictor first, then return here to see detailed explanations
                </p>
              </div>
            </div>
          </div>

          {/* Tabs Section */}
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <div className="flex justify-center mb-6">
              <TabsList className="grid w-full max-w-md grid-cols-2 h-12">
                <TabsTrigger value="dashboard" className="flex items-center justify-center gap-2 px-4 py-3 text-sm font-medium data-[state=active]:bg-white data-[state=active]:text-slate-900">
                  <BarChart3 className="w-4 h-4" />
                  <span>Dashboard</span>
                </TabsTrigger>
                <TabsTrigger value="reports" className="flex items-center justify-center gap-2 px-4 py-3 text-sm font-medium data-[state=active]:bg-white data-[state=active]:text-slate-900">
                  <FileText className="w-4 h-4" />
                  <span>Reports</span>
                </TabsTrigger>
              </TabsList>
            </div>

            {/* Dashboard Tab */}
            <TabsContent value="dashboard" className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                {/* Real-time Analysis Card */}
                <div className="group relative overflow-hidden rounded-xl border border-cyan-200 dark:border-cyan-700 bg-gradient-to-br from-cyan-50 via-blue-50 to-indigo-50 dark:from-cyan-950 dark:via-blue-950 dark:to-indigo-950 p-6 hover:shadow-xl transition-all duration-300 hover:border-cyan-400 dark:hover:border-cyan-600">
                  {/* Gradient overlay on hover */}
                  <div className="absolute inset-0 bg-gradient-to-br from-cyan-400/0 to-blue-500/0 group-hover:from-cyan-400/5 group-hover:to-blue-500/10 transition-all duration-300" />
                  <div className="relative z-10">
                    <div className="flex items-start justify-between mb-4">
                      <div className="p-3 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-xl shadow-lg group-hover:shadow-xl transition-shadow">
                        <Lightbulb className="w-6 h-6 text-white" />
                      </div>
                      <div className="text-xs px-3 py-1 bg-cyan-200 dark:bg-cyan-800 text-cyan-900 dark:text-cyan-100 rounded-full font-semibold">
                        Real-time
                      </div>
                    </div>
                    <h3 className="text-lg font-bold text-foreground mb-2">Real-time Analysis</h3>
                    <p className="text-sm text-muted-foreground leading-relaxed mb-4">
                      Get instant explanations for each prediction with interactive visualizations
                    </p>
                    <div className="space-y-2 text-xs text-muted-foreground">
                      <div className="flex items-center gap-2"><span className="text-cyan-600 font-bold">◆</span> Interactive charts & graphs</div>
                      <div className="flex items-center gap-2"><span className="text-cyan-600 font-bold">◆</span> Live SHAP value computation</div>
                      <div className="flex items-center gap-2"><span className="text-cyan-600 font-bold">◆</span> Instant model insights</div>
                    </div>
                  </div>
                </div>

                {/* Risk Assessment Card */}
                <div className="group relative overflow-hidden rounded-xl border border-red-200 dark:border-red-700 bg-gradient-to-br from-red-50 via-orange-50 to-yellow-50 dark:from-red-950 dark:via-orange-950 dark:to-yellow-950 p-6 hover:shadow-xl transition-all duration-300 hover:border-red-400 dark:hover:border-red-600">
                  {/* Gradient overlay on hover */}
                  <div className="absolute inset-0 bg-gradient-to-br from-red-400/0 to-orange-500/0 group-hover:from-red-400/5 group-hover:to-orange-500/10 transition-all duration-300" />
                  <div className="relative z-10">
                    <div className="flex items-start justify-between mb-4">
                      <div className="p-3 bg-gradient-to-br from-red-500 to-orange-600 rounded-xl shadow-lg group-hover:shadow-xl transition-shadow">
                        <Shield className="w-6 h-6 text-white" />
                      </div>
                      <div className="text-xs px-3 py-1 bg-red-200 dark:bg-red-800 text-red-900 dark:text-red-100 rounded-full font-semibold">
                        Alert
                      </div>
                    </div>
                    <h3 className="text-lg font-bold text-foreground mb-2">Risk Assessment</h3>
                    <p className="text-sm text-muted-foreground leading-relaxed mb-4">
                      Automated risk scoring and anomaly detection for each analysis
                    </p>
                    <div className="space-y-2 text-xs text-muted-foreground">
                      <div className="flex items-center gap-2"><span className="text-red-600 font-bold">◆</span> Anomaly detection system</div>
                      <div className="flex items-center gap-2"><span className="text-red-600 font-bold">◆</span> Risk score calculation</div>
                      <div className="flex items-center gap-2"><span className="text-red-600 font-bold">◆</span> Outlier identification</div>
                    </div>
                  </div>
                </div>

                {/* SHAP vs LIME Comparison Card */}
                <div className="group relative overflow-hidden rounded-xl border border-purple-200 dark:border-purple-700 bg-gradient-to-br from-purple-50 via-pink-50 to-rose-50 dark:from-purple-950 dark:via-pink-950 dark:to-rose-950 p-6 hover:shadow-xl transition-all duration-300 hover:border-purple-400 dark:hover:border-purple-600">
                  {/* Gradient overlay on hover */}
                  <div className="absolute inset-0 bg-gradient-to-br from-purple-400/0 to-pink-500/0 group-hover:from-purple-400/5 group-hover:to-pink-500/10 transition-all duration-300" />
                  <div className="relative z-10">
                    <div className="flex items-start justify-between mb-4">
                      <div className="p-3 bg-gradient-to-br from-purple-500 to-pink-600 rounded-xl shadow-lg group-hover:shadow-xl transition-shadow">
                        <BarChart3 className="w-6 h-6 text-white" />
                      </div>
                      <div className="text-xs px-3 py-1 bg-purple-200 dark:bg-purple-800 text-purple-900 dark:text-purple-100 rounded-full font-semibold">
                        Compare
                      </div>
                    </div>
                    <h3 className="text-lg font-bold text-foreground mb-2">SHAP vs LIME</h3>
                    <p className="text-sm text-muted-foreground leading-relaxed mb-4">
                      Compare multiple interpretation methods side-by-side
                    </p>
                    <div className="space-y-2 text-xs text-muted-foreground">
                      <div className="flex items-center gap-2"><span className="text-purple-600 font-bold">◆</span> Method comparison view</div>
                      <div className="flex items-center gap-2"><span className="text-purple-600 font-bold">◆</span> Accuracy metrics display</div>
                      <div className="flex items-center gap-2"><span className="text-purple-600 font-bold">◆</span> Feature importance ranking</div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Main Dashboard Component */}
              <EnhancedExplainabilityDashboard 
                predictionData={predictionDataForAnalysis}
                modelName="document_classifier"
                modelType="document"
                onGenerateReport={generateReport} 
              />
            </TabsContent>

            {/* Reports Tab */}
            <TabsContent value="reports" className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                {/* Export Card */}
                <div className="bg-gradient-to-br from-amber-50 to-orange-50 dark:from-amber-950 dark:to-orange-950 rounded-lg p-6 border border-amber-200 dark:border-amber-800">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="p-3 bg-amber-600 rounded-lg">
                      <Download className="w-5 h-5 text-white" />
                    </div>
                    <h3 className="font-semibold text-foreground">Multi-Format Export</h3>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    Download reports as JSON, HTML, or PDF for sharing and documentation
                  </p>
                </div>

                {/* Management Card */}
                <div className="bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-950 dark:to-pink-950 rounded-lg p-6 border border-purple-200 dark:border-purple-800">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="p-3 bg-purple-600 rounded-lg">
                      <BookOpen className="w-5 h-5 text-white" />
                    </div>
                    <h3 className="font-semibold text-foreground">Report History</h3>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    Track and manage all generated reports with timestamp and version control
                  </p>
                </div>

                {/* Insights Card */}
                <div className="bg-gradient-to-br from-green-50 to-teal-50 dark:from-green-950 dark:to-teal-950 rounded-lg p-6 border border-green-200 dark:border-green-800">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="p-3 bg-green-600 rounded-lg">
                      <TrendingUp className="w-5 h-5 text-white" />
                    </div>
                    <h3 className="font-semibold text-foreground">Key Insights</h3>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    Extract actionable insights and recommendations from analysis
                  </p>
                </div>
              </div>

              {/* Main Reports Component */}
              <ExplainabilityReportViewer
                apiEndpoint={import.meta.env.VITE_BACKEND_URL || "http://localhost:3001"}
              />
            </TabsContent>
          </Tabs>

          {/* Footer */}
          <div className="text-center pt-8 border-t border-border/50">
            <p className="text-sm text-muted-foreground">
              Advanced Explainability • Real-time Analysis • Model Transparency
            </p>
          </div>
        </main>
      </div>
    </div>
  );
};

export default Explainability;