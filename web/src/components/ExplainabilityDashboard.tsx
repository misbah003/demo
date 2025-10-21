/**
 * 🔍 EXPLAINABILITY DASHBOARD COMPONENT
 * =====================================
 * 
 * Displays SHAP/LIME explanations and model interpretability
 * - Feature importance visualization
 * - Prediction breakdown
 * - Risk assessment
 * - PDF report generation
 */

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from 'recharts';
import { FileDown, RefreshCw, Loader2 } from 'lucide-react';

interface FeatureContribution {
  feature: string;
  shap_value: number;
  importance: number;
  value: number | null;
  direction: 'positive' | 'negative';
}

interface ExplanationData {
  method: string;
  status: string;
  base_value?: number;
  prediction: number;
  feature_contributions: FeatureContribution[];
  timestamp: string;
  confidence?: number;
  anomaly_score?: number;
  is_anomaly?: boolean;
}

interface ExplainabilityDashboardProps {
  predictionData?: any;
  modelName: string;
  onGenerateReport?: () => void;
}

const ExplainabilityDashboard: React.FC<ExplainabilityDashboardProps> = ({
  predictionData,
  modelName = 'vat_predictor',
  onGenerateReport
}) => {
  const [explanation, setExplanation] = useState<ExplanationData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedMethod, setSelectedMethod] = useState<'shap' | 'lime'>('shap');

  // Fetch explanation on mount or when predictionData changes
  useEffect(() => {
    if (predictionData) {
      fetchExplanation();
    }
  }, [predictionData]);

  const fetchExplanation = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const endpoint = getExplanationEndpoint();
      const response = await fetch(`http://localhost:8000${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...predictionData,
          method: selectedMethod
        })
      });

      if (!response.ok) {
        throw new Error('Failed to fetch explanation');
      }

      const data = await response.json();
      setExplanation(data.data || data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
      console.error('Explanation fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getExplanationEndpoint = (): string => {
    switch (modelName.toLowerCase()) {
      case 'vat_predictor':
        return '/api/explain-vat';
      case 'document_classifier':
        return '/api/explain-document';
      case 'anomaly_detector':
        return '/api/explain-anomaly';
      default:
        return '/api/explain';
    }
  };

  const handleGenerateReport = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/explain-report', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prediction_data: predictionData,
          model_name: modelName,
          input_summary: explanation
        })
      });

      if (!response.ok) throw new Error('Failed to generate report');

      const data = await response.json();
      
      // Download report
      const reportResponse = await fetch(data.download_url);
      const blob = await reportResponse.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `explanation_${modelName}_${new Date().getTime()}.json`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      console.error('Report generation error:', err);
    }
  };

  const chartData = explanation?.feature_contributions?.map(f => ({
    name: f.feature.substring(0, 20),
    importance: Math.abs(f.importance),
    value: f.shap_value,
    fullName: f.feature
  })) || [];

  const topFeatures = chartData.slice(0, 5);

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Model Explainability</h2>
          <p className="text-muted-foreground mt-2">
            Understand how {modelName} makes predictions
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={fetchExplanation}
            disabled={loading}
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
          <Button
            size="sm"
            onClick={handleGenerateReport}
            disabled={!explanation}
          >
            <FileDown className="w-4 h-4 mr-2" />
            Download Report
          </Button>
        </div>
      </div>

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Method Selection */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Explanation Method</CardTitle>
          <CardDescription>Choose how to explain the prediction</CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs value={selectedMethod} onValueChange={(v) => setSelectedMethod(v as 'shap' | 'lime')}>
            <TabsList>
              <TabsTrigger value="shap">SHAP Values</TabsTrigger>
              <TabsTrigger value="lime">LIME</TabsTrigger>
            </TabsList>
            <TabsContent value="shap" className="text-sm text-muted-foreground mt-4">
              🎯 SHAP (SHapley Additive exPlanations): Shows how each feature contributes to pushing the prediction from the base value to the actual prediction. Global and local interpretability.
            </TabsContent>
            <TabsContent value="lime" className="text-sm text-muted-foreground mt-4">
              🔍 LIME (Local Interpretable Model-agnostic Explanations): Creates local interpretable models around the prediction. Fast and model-agnostic approach.
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>

      {/* Prediction Summary */}
      {explanation && (
        <>
          <Card>
            <CardHeader>
              <CardTitle>Prediction Summary</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {/* Prediction Value */}
                <div className="space-y-2">
                  <p className="text-sm font-medium text-muted-foreground">Predicted Value</p>
                  <p className="text-2xl font-bold">
                    {typeof explanation.prediction === 'number'
                      ? `€${explanation.prediction.toLocaleString('en-US', {
                          minimumFractionDigits: 2,
                          maximumFractionDigits: 2
                        })}`
                      : explanation.prediction}
                  </p>
                </div>

                {/* Confidence */}
                {explanation.confidence !== undefined && (
                  <div className="space-y-2">
                    <p className="text-sm font-medium text-muted-foreground">Confidence</p>
                    <div className="flex items-center gap-2">
                      <div className="flex-1 bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-blue-500 h-2 rounded-full transition-all"
                          style={{ width: `${(explanation.confidence ?? 0) * 100}%` }}
                        />
                      </div>
                      <span className="text-xl font-bold">
                        {((explanation.confidence ?? 0) * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>
                )}

                {/* Status */}
                <div className="space-y-2">
                  <p className="text-sm font-medium text-muted-foreground">Status</p>
                  <Badge variant={explanation.status === 'success' ? 'default' : 'destructive'}>
                    {explanation.status === 'success' ? '✅ Success' : '❌ Failed'}
                  </Badge>
                </div>
              </div>

              {/* Base Value */}
              {explanation.base_value !== undefined && (
                <div>
                  <p className="text-sm text-muted-foreground">
                    Base Value (Model Expectation): €{explanation.base_value.toLocaleString()}
                  </p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Feature Importance */}
          <Card>
            <CardHeader>
              <CardTitle>Feature Importance</CardTitle>
              <CardDescription>
                Top factors influencing the prediction
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Tabs defaultValue="chart" className="space-y-4">
                <TabsList>
                  <TabsTrigger value="chart">Chart</TabsTrigger>
                  <TabsTrigger value="table">Details</TabsTrigger>
                </TabsList>

                {/* Chart View */}
                <TabsContent value="chart">
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={topFeatures}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis />
                      <Tooltip content={({ active, payload }) => {
                        if (active && payload && payload.length) {
                          const data = payload[0].payload;
                          return (
                            <div className="bg-white p-2 border rounded shadow">
                              <p className="font-semibold">{data.fullName}</p>
                              <p>Importance: {data.importance.toFixed(4)}</p>
                              <p>SHAP: {data.value.toFixed(4)}</p>
                            </div>
                          );
                        }
                        return null;
                      }} />
                      <Bar dataKey="importance" fill="#3b82f6" />
                    </BarChart>
                  </ResponsiveContainer>
                </TabsContent>

                {/* Table View */}
                <TabsContent value="table">
                  <div className="space-y-2">
                    {explanation.feature_contributions?.map((feat, idx) => (
                      <div key={idx} className="flex items-center justify-between p-3 border rounded">
                        <div className="flex-1">
                          <p className="font-semibold text-sm">{feat.feature}</p>
                          <p className="text-xs text-muted-foreground">
                            Value: {feat.value?.toFixed(2) ?? 'N/A'} | 
                            Direction: {feat.direction}
                          </p>
                        </div>
                        <div className="text-right">
                          <p className="text-sm font-bold">
                            {feat.direction === 'positive' ? '📈' : '📉'} {feat.shap_value.toFixed(4)}
                          </p>
                          <p className="text-xs text-muted-foreground">
                            Importance: {feat.importance.toFixed(4)}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>

          {/* Anomaly Information */}
          {explanation.is_anomaly !== undefined && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  {explanation.is_anomaly ? '⚠️' : '✅'} Anomaly Detection
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">Anomaly Score:</span>
                    <Badge variant={explanation.is_anomaly ? 'destructive' : 'default'}>
                      {explanation.anomaly_score?.toFixed(3)} 
                      {explanation.is_anomaly ? ' (HIGH RISK)' : ' (LOW RISK)'}
                    </Badge>
                  </div>
                  {explanation.is_anomaly && (
                    <Alert>
                      <AlertDescription>
                        This transaction shows unusual patterns. Recommend manual review.
                      </AlertDescription>
                    </Alert>
                  )}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Metadata */}
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">Metadata</CardTitle>
            </CardHeader>
            <CardContent className="text-xs text-muted-foreground space-y-1">
              <p>Method: {explanation.method}</p>
              <p>Generated: {new Date(explanation.timestamp).toLocaleString()}</p>
            </CardContent>
          </Card>
        </>
      )}

      {/* Loading State */}
      {loading && !explanation && (
        <Card>
          <CardContent className="py-12 flex items-center justify-center">
            <div className="text-center space-y-4">
              <Loader2 className="w-8 h-8 animate-spin mx-auto" />
              <p className="text-muted-foreground">Generating explanation...</p>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default ExplainabilityDashboard;