import { TrendingUp, TrendingDown, AlertTriangle, CheckCircle, FileText } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useProcessedDocuments } from "@/hooks/useProcessedDocuments";
import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";

interface Metric {
  title: string;
  value: string;
  change: string;
  trend: string;
  icon: any;
  gradient: string;
  clickable?: boolean;
  onClick?: () => void;
}

const MetricsCards = () => {
  const { documents, loading } = useProcessedDocuments();
  const navigate = useNavigate();
  const [showAnomalyDialog, setShowAnomalyDialog] = useState(false);

  // Get anomaly documents
  const anomalyDocs = useMemo(() => {
    return documents.filter(doc => 
      doc.classification === 'Missing Key Information' || 
      doc.classification === 'Processing Failed'
    );
  }, [documents]);

  // Calculate metrics from real data
  const metrics = useMemo(() => {
    const totalDocs = documents.length;
    const compliantDocs = documents.filter(doc => 
      doc.classification === 'Compliant'
    ).length;
    const complianceScore = totalDocs > 0 
      ? ((compliantDocs / totalDocs) * 100).toFixed(1)
      : "0.0";
    
    const avgConfidence = totalDocs > 0
      ? (documents.reduce((sum, doc) => sum + doc.confidence, 0) / totalDocs * 100).toFixed(1)
      : "0.0";

    const alertDocs = anomalyDocs.length;

    return [
      {
        title: "Tax Compliance Score",
        value: `${complianceScore}%`,
        change: totalDocs > 0 ? `${compliantDocs}/${totalDocs} compliant` : "No data",
        trend: "up",
        icon: CheckCircle,
        gradient: "gradient-success"
      },
      {
        title: "Documents Processed",
        value: totalDocs.toString(),
        change: totalDocs > 0 ? "Total processed" : "Upload documents",
        trend: "up",
        icon: FileText,
        gradient: "gradient-primary",
        clickable: true,
        onClick: () => navigate('/documents')
      },
      {
        title: "Anomaly Detection",
        value: `${alertDocs} alerts`,
        change: alertDocs > 0 ? "Needs attention" : "All clear",
        trend: alertDocs > 0 ? "up" : "down",
        icon: AlertTriangle,
        gradient: "gradient-warning",
        clickable: alertDocs > 0,
        onClick: () => setShowAnomalyDialog(true)
      },
      {
        title: "Processing Confidence",
        value: `${avgConfidence}%`,
        change: totalDocs > 0 ? "Average confidence" : "No data",
        trend: "up",
        icon: TrendingUp,
        gradient: "gradient-success"
      }
    ];
  }, [documents, anomalyDocs, navigate]);

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {[1, 2, 3, 4].map((i) => (
          <Card key={i} className="shadow-card border-border/50 bg-card/60 backdrop-blur-sm">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <div className="h-4 w-32 bg-muted animate-pulse rounded" />
              <div className="h-8 w-8 bg-muted animate-pulse rounded-lg" />
            </CardHeader>
            <CardContent>
              <div className="h-8 w-20 bg-muted animate-pulse rounded mb-1" />
              <div className="h-3 w-24 bg-muted animate-pulse rounded" />
            </CardContent>
          </Card>
        ))}
      </div>
    );
  }

  return (
    <>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {metrics.map((metric, index) => {
          const Icon = metric.icon;
          const isClickable = metric.clickable;
          
          return (
            <Card 
              key={index} 
              className={`shadow-card hover:shadow-elegant transition-smooth border-border/50 bg-card/60 backdrop-blur-sm ${
                isClickable ? 'cursor-pointer hover:scale-105 hover:border-intelligence-blue/50' : ''
              }`}
              onClick={isClickable && metric.onClick ? metric.onClick : undefined}
            >
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">
                  {metric.title}
                </CardTitle>
                <div className={`p-2 rounded-lg bg-${metric.gradient}`}>
                  <Icon className="h-4 w-4 text-white" />
                </div>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-foreground mb-1">
                  {metric.value}
                </div>
                <p className={`text-xs flex items-center ${
                  metric.trend === 'up' ? 'text-success' : 'text-intelligence-amber'
                }`}>
                  {metric.trend === 'up' ? (
                    <TrendingUp className="h-3 w-3 mr-1" />
                  ) : (
                    <TrendingDown className="h-3 w-3 mr-1" />
                  )}
                  {metric.change}
                </p>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Anomaly Details Dialog */}
      <Dialog open={showAnomalyDialog} onOpenChange={setShowAnomalyDialog}>
        <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="flex items-center text-xl">
              <AlertTriangle className="h-6 w-6 mr-2 text-intelligence-amber" />
              Anomaly Detection Details
            </DialogTitle>
            <DialogDescription>
              Documents that require your attention
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-4 mt-4">
            {anomalyDocs.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground">
                <CheckCircle className="h-12 w-12 mx-auto mb-4 text-success" />
                <p>No anomalies detected. All documents are compliant!</p>
              </div>
            ) : (
              anomalyDocs.map((doc, index) => (
                <Card key={index} className="border-intelligence-amber/30">
                  <CardContent className="p-4">
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex items-center space-x-2">
                        <FileText className="h-5 w-5 text-intelligence-amber" />
                        <div>
                          <p className="font-medium text-foreground">{doc.filename}</p>
                          <p className="text-xs text-muted-foreground">
                            Processed: {new Date(doc.processed_at).toLocaleDateString()}
                          </p>
                        </div>
                      </div>
                      <span className={`px-2 py-1 rounded text-xs font-medium ${
                        doc.classification === 'Processing Failed' 
                          ? 'bg-destructive/10 text-destructive' 
                          : 'bg-intelligence-amber/10 text-intelligence-amber'
                      }`}>
                        {doc.classification}
                      </span>
                    </div>
                    
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Document Type:</span>
                        <span className="font-medium">{doc.type}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Confidence:</span>
                        <span className="font-medium">{(doc.confidence * 100).toFixed(1)}%</span>
                      </div>
                      
                      {doc.classification === 'Missing Key Information' && (
                        <div className="mt-3 p-3 bg-intelligence-amber/5 rounded-lg border border-intelligence-amber/20">
                          <p className="text-xs font-medium text-intelligence-amber mb-1">⚠️ Issues Found:</p>
                          <ul className="text-xs text-muted-foreground space-y-1">
                            <li>• Missing required tax identification numbers</li>
                            <li>• Incomplete date information</li>
                            <li>• Missing monetary values</li>
                          </ul>
                        </div>
                      )}
                      
                      {doc.classification === 'Processing Failed' && (
                        <div className="mt-3 p-3 bg-destructive/5 rounded-lg border border-destructive/20">
                          <p className="text-xs font-medium text-destructive mb-1">❌ Processing Error:</p>
                          <p className="text-xs text-muted-foreground">
                            The document could not be processed. Please check the file format and try uploading again.
                          </p>
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              ))
            )}
          </div>
        </DialogContent>
      </Dialog>
    </>
  );
};

export default MetricsCards;