import { AlertTriangle, Shield, FileX, Clock } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
import { supabase } from "@/integrations/supabase/client";
import { useState, useEffect } from "react";

interface RiskFactor {
  title: string;
  score: number;
  status: "low" | "medium" | "high";
  reasons: string[];
  icon?: any;
  description?: string;
}

interface ComplianceData {
  riskFactors: RiskFactor[];
  overallScore: number;
  overallStatus: "low" | "medium" | "high";
}

const ComplianceRisk = () => {
  const [data, setData] = useState<ComplianceData | null>(null);
  const [loading, setLoading] = useState(true);
  const [showDetails, setShowDetails] = useState<Record<string, boolean>>({});

  const generateReport = async () => {
    try {
      const { data: pdfBlob, error } = await supabase.functions.invoke('compliance-report', {
        responseType: 'blob'
      });
      if (error) throw error;

      // Create download link
      const url = URL.createObjectURL(new Blob([pdfBlob]));
      const link = document.createElement('a');
      link.href = url;
      link.download = 'compliance-report.pdf';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error generating report:', error);
      alert('Error generating report. Please try again.');
    }
  };

  const toggleDetails = (title: string) => {
    setShowDetails(prev => ({
      ...prev,
      [title]: !prev[title]
    }));
  };

  useEffect(() => {
    fetchComplianceData();
  }, []);

  const fetchComplianceData = async () => {
    try {
      // Try to fetch from ML API first
      const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:3001';
      const response = await fetch(`${backendUrl}/api/compliance-risk-assessment`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const mlData = await response.json();
        setData(mlData);
      } else {
        throw new Error('ML API not available');
      }
    } catch (error) {
      console.error('Error fetching compliance data from ML API:', error);

      // Try Supabase edge function as backup
      try {
        const { data: response, error } = await supabase.functions.invoke('compliance-risk');
        if (error) throw error;
        setData(response);
      } catch (supabaseError) {
        console.error('Error fetching compliance data from Supabase:', supabaseError);

        // Final fallback to default data
        setData({
          riskFactors: [
            {
              title: "Late Filing Risk",
              score: 15,
              status: "low",
              reasons: ["No late filings detected"]
            },
            {
              title: "Documentation Gap",
              score: 45,
              status: "medium",
              reasons: ["Some documents missing"]
            },
            {
              title: "Audit Probability",
              score: 25,
              status: "low",
              reasons: ["Low risk based on compliance"]
            },
            {
              title: "Penalty Risk",
              score: 65,
              status: "high",
              reasons: ["Multiple non-compliance indicators"]
            }
          ],
          overallScore: 37,
          overallStatus: "medium"
        });
      }
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Card className="shadow-card border-border/50 bg-card/60 backdrop-blur-sm">
        <CardContent className="p-6">
          <div className="text-center">Loading compliance data...</div>
        </CardContent>
      </Card>
    );
  }

  const riskFactors = data?.riskFactors || [];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'low': return 'text-success';
      case 'medium': return 'text-intelligence-amber';
      case 'high': return 'text-destructive';
      default: return 'text-muted-foreground';
    }
  };

  const getProgressColor = (status: string) => {
    switch (status) {
      case 'low': return 'bg-success';
      case 'medium': return 'bg-intelligence-amber';
      case 'high': return 'bg-destructive';
      default: return 'bg-muted';
    }
  };

  return (
    <Card className="shadow-card border-border/50 bg-card/60 backdrop-blur-sm">
      <CardHeader>
        <CardTitle className="text-lg font-semibold text-foreground flex items-center">
          <AlertTriangle className="h-5 w-5 mr-2 text-intelligence-amber" />
          Compliance Risk Assessment
        </CardTitle>
        <p className="text-sm text-muted-foreground">
          AI-powered risk scoring and recommendations
        </p>
      </CardHeader>
      <CardContent className="space-y-6">
        {riskFactors.map((factor, index) => {
          const Icon = factor.icon || AlertTriangle;
          return (
            <div key={index} className="space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <Icon className={`h-4 w-4 ${getStatusColor(factor.status)}`} />
                  <div>
                    <p className="font-medium text-foreground">{factor.title}</p>
                    <p className="text-xs text-muted-foreground">{factor.description}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className={`text-sm font-semibold ${getStatusColor(factor.status)}`}>
                    {factor.score}%
                  </p>
                  <p className="text-xs text-muted-foreground capitalize">
                    {factor.status} risk
                  </p>
                </div>
              </div>
              <Progress 
                value={factor.score} 
                className="h-2"
                // Note: Progress component would need custom styling for colors
              />
              
              {showDetails[factor.title] && (
                <div className="mt-2 p-3 bg-muted/50 rounded-lg">
                  <h4 className="font-medium mb-2 text-sm">Detailed Reasons:</h4>
                  <ul className="space-y-1 text-sm">
                    {factor.reasons.map((reason, idx) => (
                      <li key={idx} className="text-muted-foreground">• {reason}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          );
        })}
        
        <div className="pt-4 border-t border-border/50">
          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium text-foreground">Overall Risk Score</p>
              <p className="text-xs text-muted-foreground">Weighted average assessment</p>
            </div>
            <div className="text-right">
              <p className={`text-lg font-bold ${getStatusColor(data?.overallStatus || 'medium')}`}>
                {data?.overallScore || 0}%
              </p>
              <p className="text-xs text-muted-foreground capitalize">
                {data?.overallStatus || 'medium'} Risk
              </p>
            </div>
          </div>
          <div className="mt-4 flex space-x-2">
            <Button
              variant="intelligence"
              size="sm"
              className="flex-1"
              onClick={generateReport}
            >
              Generate Report
            </Button>
            <Button
              variant="outline"
              size="sm"
              className="flex-1"
              onClick={() => setShowDetails(prev => {
                const allShown = Object.values(prev).every(v => v);
                const newState: Record<string, boolean> = {};
                riskFactors.forEach(f => newState[f.title] = !allShown);
                return newState;
              })}
            >
              {Object.values(showDetails).some(v => v) ? 'Hide Details' : 'View Details'}
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default ComplianceRisk;