/**
 * 📋 EXPLAINABILITY REPORT VIEWER COMPONENT
 * ==========================================
 * 
 * Advanced component for displaying, managing, and downloading explainability reports
 * - Report list management
 * - Multi-format download (JSON, HTML, PDF)
 * - Report detail view
 * - Report deletion
 * - Batch operations
 */

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { 
  FileDown, 
  FileJson, 
  FileText, 
  FileX, 
  RefreshCw, 
  Loader2,
  Trash2,
  Eye,
  Download,
  Clock,
  HardDrive,
  File
} from 'lucide-react';

interface Report {
  filename: string;
  format: string;
  size: number;
  created: string;
  url: string;
}

interface ReportSummary {
  prediction?: {
    value?: number;
    confidence?: number;
  };
  risk_level?: string;
  top_features?: Array<{
    feature: string;
    importance: number;
  }>;
}

interface ExplainabilityReportViewerProps {
  apiEndpoint?: string;
  autoRefresh?: boolean;
  refreshInterval?: number;
}

const ExplainabilityReportViewer: React.FC<ExplainabilityReportViewerProps> = ({
  apiEndpoint = import.meta.env.VITE_BACKEND_URL || 'http://localhost:3001',
  autoRefresh = true,
  refreshInterval = 30000
}) => {
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedReport, setSelectedReport] = useState<Report | null>(null);
  const [reportDetail, setReportDetail] = useState<any>(null);
  const [detailLoading, setDetailLoading] = useState(false);

  // Auto-refresh reports
  useEffect(() => {
    fetchReports();
    
    if (autoRefresh) {
      const interval = setInterval(fetchReports, refreshInterval);
      return () => clearInterval(interval);
    }
  }, []);

  const fetchReports = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${apiEndpoint}/api/reports`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch reports');
      }
      
      const data = await response.json();
      setReports(data.reports || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
      console.error('Reports fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchReportDetail = async (report: Report) => {
    if (report.format !== 'JSON') {
      return; // Can't display detail view for non-JSON reports
    }
    
    setDetailLoading(true);
    
    try {
      const response = await fetch(`${apiEndpoint}${report.url}`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch report details');
      }
      
      const data = await response.json();
      setReportDetail(data);
      setSelectedReport(report);
    } catch (err) {
      console.error('Report detail fetch error:', err);
    } finally {
      setDetailLoading(false);
    }
  };

  const downloadReport = async (report: Report) => {
    try {
      const response = await fetch(`${apiEndpoint}${report.url}`);
      
      if (!response.ok) {
        throw new Error('Failed to download report');
      }
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = report.filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      console.error('Download error:', err);
      setError(err instanceof Error ? err.message : 'Download failed');
    }
  };

  const deleteReport = async (filename: string) => {
    if (!confirm(`Are you sure you want to delete ${filename}?`)) {
      return;
    }
    
    try {
      const response = await fetch(`${apiEndpoint}/api/reports/${filename}`, {
        method: 'DELETE'
      });
      
      if (!response.ok) {
        throw new Error('Failed to delete report');
      }
      
      setReports(reports.filter(r => r.filename !== filename));
      if (selectedReport?.filename === filename) {
        setSelectedReport(null);
        setReportDetail(null);
      }
    } catch (err) {
      console.error('Delete error:', err);
      setError(err instanceof Error ? err.message : 'Delete failed');
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  const getRiskColor = (riskLevel?: string): string => {
    switch (riskLevel?.toUpperCase()) {
      case 'HIGH':
        return 'bg-red-100 text-red-800';
      case 'MEDIUM':
        return 'bg-yellow-100 text-yellow-800';
      case 'LOW':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getFormatIcon = (format: string) => {
    switch (format.toUpperCase()) {
      case 'JSON':
        return <FileJson className="w-4 h-4" />;
      case 'HTML':
        return <FileText className="w-4 h-4" />;
      case 'PDF':
        return <FileDown className="w-4 h-4" />;
      default:
        return <FileX className="w-4 h-4" />;
    }
  };

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Explainability Reports</h2>
          <p className="text-muted-foreground mt-2">
            View, download, and manage model explanation reports
          </p>
        </div>
        <Button
          onClick={fetchReports}
          disabled={loading}
          variant="outline"
          size="sm"
        >
          {loading ? (
            <>
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              Loading...
            </>
          ) : (
            <>
              <RefreshCw className="w-4 h-4 mr-2" />
              Refresh
            </>
          )}
        </Button>
      </div>

      {/* Loading State */}
      {loading && reports.length === 0 && (
        <Alert className="bg-blue-50 border-blue-200">
          <Loader2 className="h-4 w-4 animate-spin" />
          <AlertDescription className="text-blue-900">
            Loading reports from server...
          </AlertDescription>
        </Alert>
      )}

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive">
          <AlertDescription>
            <div className="space-y-2">
              <p><strong>Error loading reports:</strong> {error}</p>
              <p className="text-sm">Make sure the ML API server is running on http://localhost:8000</p>
              <Button 
                onClick={fetchReports} 
                size="sm" 
                variant="outline"
                className="mt-2"
              >
                <RefreshCw className="w-4 h-4 mr-2" />
                Retry
              </Button>
            </div>
          </AlertDescription>
        </Alert>
      )}

      {/* Reports Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardContent className="pt-6">
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">Total Reports</p>
              <p className="text-3xl font-bold">{reports.length}</p>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="pt-6">
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">Total Size</p>
              <p className="text-3xl font-bold">
                {formatFileSize(reports.reduce((sum, r) => sum + r.size, 0))}
              </p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">Formats</p>
              <div className="flex gap-2">
                {Array.from(new Set(reports.map(r => r.format))).map(fmt => (
                  <Badge key={fmt} variant="outline">
                    {fmt}
                  </Badge>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Reports List */}
      <Card>
        <CardHeader>
          <CardTitle>Reports List</CardTitle>
          <CardDescription>
            {reports.length === 0 ? 'No reports available' : `${reports.length} reports found`}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {reports.length === 0 ? (
            <div className="text-center py-8 space-y-4">
              <FileX className="w-12 h-12 mx-auto mb-3 opacity-50 text-muted-foreground" />
              <div className="space-y-2">
                <p className="font-semibold text-foreground">No reports available yet</p>
                <p className="text-sm text-muted-foreground">Generate your first explainability report to get started.</p>
              </div>
              <div className="bg-blue-50 dark:bg-blue-950 border border-blue-200 dark:border-blue-800 rounded-lg p-4 text-left text-sm">
                <p className="font-semibold text-blue-900 dark:text-blue-100 mb-2">How to generate reports:</p>
                <ol className="list-decimal list-inside space-y-1 text-blue-800 dark:text-blue-200 text-xs">
                  <li>Go to the <strong>Documents</strong> section</li>
                  <li>Upload or process a document</li>
                  <li>View the prediction results</li>
                  <li>Click "Generate Report" to save an explainability report</li>
                </ol>
              </div>
            </div>
          ) : (
            <div className="space-y-2">
              {reports.map((report) => (
                <div
                  key={report.filename}
                  className="flex items-center justify-between p-4 border rounded-lg hover:bg-slate-50 transition-colors"
                >
                  {/* Report Info */}
                  <div className="flex-1">
                    <div className="flex items-center gap-3">
                      {getFormatIcon(report.format)}
                      <div>
                        <p className="font-medium text-sm">{report.filename}</p>
                        <div className="flex gap-2 mt-1 text-xs text-muted-foreground">
                          <span className="flex items-center gap-1">
                            <Clock className="w-3 h-3" />
                            {formatDate(report.created)}
                          </span>
                          <span className="flex items-center gap-1">
                            <HardDrive className="w-3 h-3" />
                            {formatFileSize(report.size)}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Format Badge */}
                  <Badge variant="outline" className="mx-3">
                    {report.format}
                  </Badge>

                  {/* Actions */}
                  <div className="flex gap-2">
                    {report.format === 'JSON' && (
                      <Dialog>
                        <DialogTrigger asChild>
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => fetchReportDetail(report)}
                          >
                            <Eye className="w-4 h-4" />
                          </Button>
                        </DialogTrigger>
                        <DialogContent className="max-w-2xl">
                          <DialogHeader>
                            <DialogTitle>Report Details</DialogTitle>
                            <DialogDescription>
                              {report.filename}
                            </DialogDescription>
                          </DialogHeader>
                          {detailLoading ? (
                            <div className="flex justify-center py-8">
                              <Loader2 className="w-6 h-6 animate-spin" />
                            </div>
                          ) : reportDetail ? (
                            <div className="space-y-4 max-h-96 overflow-y-auto">
                              {/* Prediction Summary */}
                              {reportDetail.prediction && (
                                <div>
                                  <h4 className="font-semibold text-sm mb-2">Prediction</h4>
                                  <div className="bg-slate-50 p-3 rounded text-sm space-y-1">
                                    {reportDetail.prediction.value && (
                                      <p><strong>Value:</strong> €{reportDetail.prediction.value.toLocaleString()}</p>
                                    )}
                                    {reportDetail.prediction.confidence && (
                                      <p><strong>Confidence:</strong> {(reportDetail.prediction.confidence * 100).toFixed(1)}%</p>
                                    )}
                                  </div>
                                </div>
                              )}

                              {/* Risk Assessment */}
                              {reportDetail.risk_assessment && (
                                <div>
                                  <h4 className="font-semibold text-sm mb-2">Risk Assessment</h4>
                                  <div className="bg-slate-50 p-3 rounded text-sm space-y-1">
                                    <p>
                                      <strong>Level:</strong> {' '}
                                      <Badge className={getRiskColor(reportDetail.risk_assessment.level)}>
                                        {reportDetail.risk_assessment.level}
                                      </Badge>
                                    </p>
                                    <p><strong>Score:</strong> {reportDetail.risk_assessment.score.toFixed(2)}/100</p>
                                    <p><strong>Assessment:</strong> {reportDetail.risk_assessment.assessment}</p>
                                  </div>
                                </div>
                              )}

                              {/* Top Features */}
                              {reportDetail.feature_importance?.top_features && (
                                <div>
                                  <h4 className="font-semibold text-sm mb-2">Top Features</h4>
                                  <div className="bg-slate-50 p-3 rounded text-sm space-y-2">
                                    {reportDetail.feature_importance.top_features.slice(0, 5).map((feat: any, idx: number) => (
                                      <div key={idx} className="flex justify-between">
                                        <span>{feat.feature}</span>
                                        <span className="font-medium">{feat.importance.toFixed(4)}</span>
                                      </div>
                                    ))}
                                  </div>
                                </div>
                              )}
                            </div>
                          ) : (
                            <p className="text-sm text-muted-foreground">No details available</p>
                          )}
                        </DialogContent>
                      </Dialog>
                    )}

                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => downloadReport(report)}
                    >
                      <Download className="w-4 h-4" />
                    </Button>

                    <Button
                      size="sm"
                      variant="outline"
                      className="text-red-600 hover:text-red-700"
                      onClick={() => deleteReport(report.filename)}
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Report Info Card */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">About Explainability Reports</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3 text-sm">
          <div>
            <p className="font-semibold mb-1">📊 JSON Format</p>
            <p className="text-muted-foreground">Complete report data with all metrics and feature contributions. Ideal for programmatic processing.</p>
          </div>
          <div>
            <p className="font-semibold mb-1">📄 HTML Format</p>
            <p className="text-muted-foreground">Professional, printable report with visual formatting. Open directly in your browser.</p>
          </div>
          <div>
            <p className="font-semibold mb-1">📋 PDF Format</p>
            <p className="text-muted-foreground">Portable document format suitable for sharing and archiving. Requires reportlab library.</p>
          </div>
          <div>
            <p className="font-semibold mb-1">🔍 What's Included</p>
            <ul className="list-disc list-inside text-muted-foreground space-y-1">
              <li>Prediction values and confidence scores</li>
              <li>Feature importance analysis</li>
              <li>Risk assessment and classification</li>
              <li>SHAP/LIME explanation breakdown</li>
              <li>Model interpretation and insights</li>
            </ul>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default ExplainabilityReportViewer;