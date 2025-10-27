/**
 * 🎨 ENHANCED EXPLAINABILITY DASHBOARD WITH LIME VISUALIZATION
 * =============================================================
 * 
 * Advanced component showing:
 * - SHAP vs LIME comparison
 * - Feature/Token importance visualization
 * - Risk assessment with color coding
 * - Interactive method selection
 * - Performance metrics
 */

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { 
  BarChart, Bar, 
  LineChart, Line, 
  ScatterChart, Scatter,
  XAxis, YAxis, 
  CartesianGrid, Tooltip, 
  Legend, ResponsiveContainer, 
  Cell, PieChart, Pie 
} from 'recharts';
import { 
  FileDown, RefreshCw, Loader2, 
  TrendingUp, AlertTriangle, CheckCircle,
  Zap, Brain, Layers
} from 'lucide-react';

interface FeatureContribution {
  feature?: string;
  token?: string;
  shap_value?: number;
  lime_weight?: number;
  importance: number;
  value?: number | null;
  direction: 'positive' | 'negative';
  position?: number;
}

interface ExplanationData {
  method: string;
  status: string;
  base_value?: number;
  prediction?: number | string;
  confidence?: number;
  anomaly_score?: number;
  is_anomaly?: boolean;
  sentiment?: string;
  feature_contributions: FeatureContribution[];
  top_positive_features?: FeatureContribution[];
  top_negative_features?: FeatureContribution[];
  positive_words?: FeatureContribution[];
  negative_words?: FeatureContribution[];
  timestamp: string;
  elapsed_time?: number;
}

interface ComparisonData {
  shap: ExplanationData | null;
  lime: ExplanationData | null;
  selectedMethod: 'shap' | 'lime';
  loading: boolean;
  error: string | null;
}

interface EnhancedExplainabilityDashboardProps {
  predictionData?: any;
  modelName: string;
  modelType: 'document' | 'anomaly' | 'sentiment' | 'vat';
  onGenerateReport?: (data: any) => void;
  apiEndpoint?: string;
}

const EnhancedExplainabilityDashboard: React.FC<EnhancedExplainabilityDashboardProps> = ({
  predictionData,
  modelName = 'tax_model',
  modelType = 'document',
  onGenerateReport,
  apiEndpoint = import.meta.env.VITE_BACKEND_URL || 'http://localhost:3001'
}) => {
  const [comparison, setComparison] = useState<ComparisonData>({
    shap: null,
    lime: null,
    selectedMethod: 'shap',
    loading: false,
    error: null
  });

  // Fetch explanations on mount or when predictionData changes
  useEffect(() => {
    if (predictionData) {
      fetchComparativeExplanations();
    }
  }, [predictionData]);

  const getEndpoint = (): string => {
    // The ML API uses /explain endpoint for all explanation types
    return '/explain';
  };

  const fetchComparativeExplanations = async () => {
    setComparison(prev => ({ ...prev, loading: true, error: null }));

    try {
      const endpoint = getEndpoint();

      // Fetch explanations from ML API (single call returns both SHAP and LIME)
      const start = performance.now();
      const response = await fetch(`${apiEndpoint}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(predictionData)
      });

      if (!response.ok) throw new Error('Explanation fetch failed');
      const result = await response.json();
      const elapsed = performance.now() - start;

      // Assume API returns { shap: ExplanationData, lime: ExplanationData }
      const shapData: ExplanationData = result.shap || result;
      const limeData: ExplanationData = result.lime || result;

      if (shapData) {
        shapData.elapsed_time = elapsed / 2; // Split time
        shapData.method = 'shap';
      }
      if (limeData) {
        limeData.elapsed_time = elapsed / 2;
        limeData.method = 'lime';
      }

      setComparison(prev => ({
        ...prev,
        shap: shapData,
        lime: limeData,
        loading: false,
        selectedMethod: 'shap'
      }));
    } catch (error) {
      setComparison(prev => ({
        ...prev,
        loading: false,
        error: error instanceof Error ? error.message : 'Failed to fetch explanations. Make sure you have prediction data.'
      }));
    }
  };

  const getRiskColor = (score: number): string => {
    if (score < 0.3) return 'bg-green-100 text-green-900';
    if (score < 0.7) return 'bg-yellow-100 text-yellow-900';
    return 'bg-red-100 text-red-900';
  };

  const getRiskLevel = (score: number): string => {
    if (score < 0.3) return 'LOW RISK';
    if (score < 0.7) return 'MEDIUM RISK';
    return 'HIGH RISK';
  };

  const getSentimentColor = (sentiment: string): string => {
    switch (sentiment?.toLowerCase()) {
      case 'positive':
        return 'bg-green-100 text-green-900';
      case 'negative':
        return 'bg-red-100 text-red-900';
      default:
        return 'bg-gray-100 text-gray-900';
    }
  };

  const currentData = comparison.selectedMethod === 'shap' ? comparison.shap : comparison.lime;

  if (comparison.loading) {
    return (
      <Card className="w-full">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Loader2 className="h-4 w-4 animate-spin" />
            Generating Explanations...
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col gap-4">
            <div className="flex items-center gap-2">
              <Loader2 className="h-4 w-4 animate-spin" />
              <p>Fetching SHAP explanation...</p>
            </div>
            <div className="flex items-center gap-2">
              <Loader2 className="h-4 w-4 animate-spin" />
              <p>Fetching LIME explanation...</p>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (comparison.error) {
    return (
      <Card className="w-full">
        <CardHeader>
          <CardTitle>Error</CardTitle>
        </CardHeader>
        <CardContent>
          <Alert className="bg-red-50">
            <AlertTriangle className="h-4 w-4" />
            <AlertDescription>{comparison.error}</AlertDescription>
          </Alert>
          <Button onClick={fetchComparativeExplanations} className="mt-4">
            <RefreshCw className="mr-2 h-4 w-4" />
            Retry
          </Button>
        </CardContent>
      </Card>
    );
  }

  if (!predictionData && !currentData) {
    return (
      <Card className="w-full border border-slate-200 dark:border-slate-700">
        <CardHeader className="pb-8">
          <CardTitle className="text-2xl font-light tracking-tight">
            SHAP Analysis Dashboard
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-10">
          {/* Main CTA Section */}
          <div className="flex flex-col gap-6">
            <div className="space-y-2">
              <p className="text-sm font-medium text-slate-600 dark:text-slate-400">To get started</p>
              <p className="text-base text-foreground">Make a prediction from Documents or VAT Predictor</p>
            </div>
            
            <div className="border-l-2 border-slate-300 dark:border-slate-600 pl-6 space-y-4">
              <div className="space-y-1">
                <p className="text-sm font-medium text-foreground">Feature Contributions</p>
                <p className="text-sm text-muted-foreground">View SHAP values and feature impact analysis</p>
              </div>
              <div className="space-y-1">
                <p className="text-sm font-medium text-foreground">Interpretation Methods</p>
                <p className="text-sm text-muted-foreground">Compare SHAP, LIME and other models</p>
              </div>
              <div className="space-y-1">
                <p className="text-sm font-medium text-foreground">Risk & Performance</p>
                <p className="text-sm text-muted-foreground">Anomaly detection and model metrics</p>
              </div>
            </div>
          </div>

          {/* Divider */}
          <div className="h-px bg-slate-200 dark:bg-slate-700"></div>

          {/* Info Section */}
          <div className="space-y-2">
            <p className="text-xs font-semibold text-slate-700 dark:text-slate-400 uppercase tracking-wider">What you'll see</p>
            <p className="text-sm text-muted-foreground leading-relaxed">
              Interactive visualizations, detailed explanations, and comprehensive metrics that help you understand exactly why the model made each prediction.
            </p>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!currentData) {
    return null;
  }

  return (
    <div className="w-full space-y-4">
      {/* Header with Method Selection */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <Brain className="h-5 w-5" />
                Model Explainability Analysis
              </CardTitle>
              <CardDescription>
                {modelType.charAt(0).toUpperCase() + modelType.slice(1)} Classification - {modelName}
              </CardDescription>
            </div>
            <Button onClick={fetchComparativeExplanations} variant="outline" size="sm">
              <RefreshCw className="mr-2 h-4 w-4" />
              Refresh
            </Button>
          </div>
        </CardHeader>
      </Card>

      {/* Method Selection Tabs */}
      <Tabs value={comparison.selectedMethod} onValueChange={(v) => 
        setComparison(prev => ({ ...prev, selectedMethod: v as 'shap' | 'lime' }))
      }>
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="shap" className="flex items-center gap-2">
            <Zap className="h-4 w-4" />
            SHAP
            {comparison.shap?.elapsed_time && (
              <span className="text-xs ml-1">({(comparison.shap.elapsed_time / 1000).toFixed(1)}s)</span>
            )}
          </TabsTrigger>
          <TabsTrigger value="lime" className="flex items-center gap-2">
            <Layers className="h-4 w-4" />
            LIME
            {comparison.lime?.elapsed_time && (
              <span className="text-xs ml-1">({(comparison.lime.elapsed_time / 1000).toFixed(1)}s)</span>
            )}
          </TabsTrigger>
          <TabsTrigger value="comparison">Comparison</TabsTrigger>
          <TabsTrigger value="insights">Insights</TabsTrigger>
        </TabsList>

        {/* SHAP Tab */}
        <TabsContent value="shap" className="space-y-4">
          <ShapExplanationView data={comparison.shap} modelType={modelType} />
        </TabsContent>

        {/* LIME Tab */}
        <TabsContent value="lime" className="space-y-4">
          <LimeExplanationView data={comparison.lime} modelType={modelType} />
        </TabsContent>

        {/* Comparison Tab */}
        <TabsContent value="comparison" className="space-y-4">
          <ComparisonView shap={comparison.shap} lime={comparison.lime} modelType={modelType} />
        </TabsContent>

        {/* Insights Tab */}
        <TabsContent value="insights" className="space-y-4">
          <InsightsView 
            shap={comparison.shap} 
            lime={comparison.lime} 
            modelType={modelType}
            onGenerateReport={onGenerateReport}
          />
        </TabsContent>
      </Tabs>
    </div>
  );
};

// ==================== SHAP VIEW ====================

const ShapExplanationView: React.FC<{ data: ExplanationData | null; modelType: string }> = ({ data, modelType }) => {
  if (!data) return null;

  const getPredictionDisplay = () => {
    switch (modelType) {
      case 'anomaly':
        return (
          <div className="grid grid-cols-3 gap-4 mb-4">
            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <p className="text-sm text-gray-600">Anomaly Detection</p>
                  <p className={`text-2xl font-bold ${data.is_anomaly ? 'text-red-600' : 'text-green-600'}`}>
                    {data.is_anomaly ? '⚠️ ANOMALY' : '✓ NORMAL'}
                  </p>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <p className="text-sm text-gray-600">Anomaly Score</p>
                  <p className="text-2xl font-bold">{(data.anomaly_score || 0).toFixed(2)}%</p>
                  <Progress value={(data.anomaly_score || 0) * 100} className="mt-2" />
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <p className="text-sm text-gray-600">Risk Level</p>
                  <Badge className={getRiskColor(data.anomaly_score || 0)}>
                    {getRiskLevel(data.anomaly_score || 0)}
                  </Badge>
                </div>
              </CardContent>
            </Card>
          </div>
        );
      case 'sentiment':
        return (
          <div className="grid grid-cols-3 gap-4 mb-4">
            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <p className="text-sm text-gray-600">Sentiment</p>
                  <Badge className={getSentimentColor(data.sentiment || '')}>
                    {data.sentiment?.toUpperCase()}
                  </Badge>
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <p className="text-sm text-gray-600">Confidence</p>
                  <p className="text-2xl font-bold">{(data.confidence || 0).toFixed(0)}%</p>
                  <Progress value={data.confidence || 0} className="mt-2" />
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <p className="text-sm text-gray-600">Intensity</p>
                  <p className="font-semibold">
                    {(data.confidence || 0) > 0.8 ? 'STRONG' : (data.confidence || 0) > 0.6 ? 'MODERATE' : 'WEAK'}
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="space-y-4">
      {getPredictionDisplay()}

      <Card>
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Zap className="h-4 w-4" />
            Top Contributing Features
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data.feature_contributions?.slice(0, 10) || []}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey={data.token ? 'token' : 'feature'} 
                angle={-45}
                textAnchor="end"
                height={100}
              />
              <YAxis label={{ value: 'SHAP Value', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Bar dataKey="shap_value" fill="#8b5cf6">
                {data.feature_contributions?.slice(0, 10).map((item, index) => (
                  <Cell key={`cell-${index}`} fill={item.direction === 'positive' ? '#10b981' : '#ef4444'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {data.top_positive_features && data.top_positive_features.length > 0 && (
        <FeatureList 
          features={data.top_positive_features} 
          title="Positive Contributors" 
          color="green"
        />
      )}

      {data.top_negative_features && data.top_negative_features.length > 0 && (
        <FeatureList 
          features={data.top_negative_features} 
          title="Negative Contributors" 
          color="red"
        />
      )}
    </div>
  );
};

// ==================== LIME VIEW ====================

const LimeExplanationView: React.FC<{ data: ExplanationData | null; modelType: string }> = ({ data, modelType }) => {
  if (!data) return null;

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Layers className="h-4 w-4" />
            Local Explanation (LIME)
          </CardTitle>
          <CardDescription>
            Shows how individual features influence the prediction locally
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data.feature_contributions?.slice(0, 10) || []}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey={data.token ? 'token' : 'feature'} 
                angle={-45}
                textAnchor="end"
                height={100}
              />
              <YAxis label={{ value: 'LIME Weight', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Bar dataKey="lime_weight" fill="#06b6d4">
                {data.feature_contributions?.slice(0, 10).map((item, index) => (
                  <Cell key={`cell-${index}`} fill={item.direction === 'positive' ? '#06b6d4' : '#f97316'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {data.positive_words && data.positive_words.length > 0 && (
        <FeatureList 
          features={data.positive_words} 
          title="Supporting Words (LIME)" 
          color="cyan"
        />
      )}

      {data.negative_words && data.negative_words.length > 0 && (
        <FeatureList 
          features={data.negative_words} 
          title="Opposing Words (LIME)" 
          color="orange"
        />
      )}
    </div>
  );
};

// ==================== COMPARISON VIEW ====================

const ComparisonView: React.FC<{ shap: ExplanationData | null; lime: ExplanationData | null; modelType: string }> = ({ shap, lime, modelType }) => {
  if (!shap || !lime) return null;

  const shap_features = shap.feature_contributions?.slice(0, 5).map(f => f.feature || f.token) || [];
  const lime_features = lime.feature_contributions?.slice(0, 5).map(f => f.feature || f.token) || [];
  
  const overlap = shap_features.filter(f => lime_features.includes(f)).length;
  const agreement = (overlap / Math.max(shap_features.length, lime_features.length)) * 100;

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle>Method Comparison</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="font-semibold mb-2">⚡ SHAP Method</p>
              <ul className="space-y-1 text-sm">
                <li>✓ Theoretically sound (Shapley values)</li>
                <li>✓ Works with any model</li>
                <li>✗ Slower (~40s per prediction)</li>
                <li>✓ More accurate</li>
              </ul>
            </div>
            <div>
              <p className="font-semibold mb-2">🎨 LIME Method</p>
              <ul className="space-y-1 text-sm">
                <li>✓ Local interpretability</li>
                <li>✓ Fast (~5-10s)</li>
                <li>✓ Intuitive visualization</li>
                <li>~ Model-specific accuracy</li>
              </ul>
            </div>
          </div>

          <div className="mt-4">
            <p className="font-semibold mb-2">Feature Agreement</p>
            <Progress value={agreement} className="mb-2" />
            <p className="text-sm text-gray-600">
              {overlap}/{Math.max(shap_features.length, lime_features.length)} top features match ({agreement.toFixed(0)}%)
            </p>
          </div>

          <div className="mt-4 p-4 bg-blue-50 rounded">
            <p className="font-semibold mb-1 text-blue-900">Recommendation</p>
            <p className="text-sm text-blue-800">
              {shap?.elapsed_time! < lime?.elapsed_time! 
                ? 'SHAP is faster in this case - use for production' 
                : 'LIME is faster - ideal for real-time dashboards'}
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

// ==================== INSIGHTS VIEW ====================

const InsightsView: React.FC<{ shap: ExplanationData | null; lime: ExplanationData | null; modelType: string; onGenerateReport?: (data: any) => void }> = ({
  shap, lime, modelType, onGenerateReport
}) => {
  if (!shap || !lime) return null;

  const generateInsights = () => {
    const insights = [];

    if (modelType === 'anomaly' && shap.is_anomaly) {
      insights.push('⚠️ Anomalous transaction detected - review recommended');
    }

    if (shap.feature_contributions && shap.feature_contributions.length > 0) {
      insights.push(`📊 Top factor: ${shap.feature_contributions[0].feature || shap.feature_contributions[0].token}`);
    }

    if (shap.elapsed_time && lime.elapsed_time) {
      const faster = Math.min(shap.elapsed_time, lime.elapsed_time) === shap.elapsed_time ? 'SHAP' : 'LIME';
      insights.push(`⏱️ ${faster} is ${Math.abs(shap.elapsed_time - lime.elapsed_time).toFixed(1)}ms faster`);
    }

    return insights;
  };

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle>Key Insights</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {generateInsights().map((insight, idx) => (
              <div key={idx} className="flex items-start gap-2 p-2 bg-gray-50 rounded">
                <CheckCircle className="h-4 w-4 mt-0.5 text-blue-600" />
                <span className="text-sm">{insight}</span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Recommendations</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2 text-sm">
            <p>• Use SHAP for production decisions requiring maximum accuracy</p>
            <p>• Use LIME for interactive dashboards requiring real-time response</p>
            <p>• Compare both methods for critical predictions</p>
            {onGenerateReport && (
              <Button onClick={() => onGenerateReport({ shap, lime, modelType })} className="mt-4 w-full">
                <FileDown className="mr-2 h-4 w-4" />
                Generate Full Report
              </Button>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

// ==================== FEATURE LIST COMPONENT ====================

const FeatureList: React.FC<{ 
  features: FeatureContribution[]; 
  title: string; 
  color: 'green' | 'red' | 'cyan' | 'orange' 
}> = ({ features, title, color }) => {
  const colorMap = {
    green: 'border-green-200 bg-green-50',
    red: 'border-red-200 bg-red-50',
    cyan: 'border-cyan-200 bg-cyan-50',
    orange: 'border-orange-200 bg-orange-50'
  };

  return (
    <Card className={`${colorMap[color]} border-2`}>
      <CardHeader>
        <CardTitle className="text-sm">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-2">
          {features.slice(0, 5).map((feat, idx) => (
            <div key={idx} className="flex items-center justify-between text-sm">
              <span className="font-medium">{feat.feature || feat.token}</span>
              <div className="flex items-center gap-2">
                <Progress value={Math.min((feat.importance || 0) * 100, 100)} className="w-20" />
                <span className="text-xs font-semibold min-w-[40px]">
                  {(feat.importance || 0).toFixed(3)}
                </span>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default EnhancedExplainabilityDashboard;