import React from "react";
import { useState, useEffect } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Calendar, Download, RefreshCw, FileText, AlertCircle } from "lucide-react";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Calendar as CalendarComponent } from "@/components/ui/calendar";
import { format } from "date-fns";
import { useToast } from "@/hooks/use-toast";
import { supabase } from "@/integrations/supabase/client";
import { Alert, AlertDescription } from "@/components/ui/alert";

interface ForecastData {
  month: string;
  actual: number | null;
  predicted: number;
  confidence_lower?: number;
  confidence_upper?: number;
}

interface ForecastResponse {
  success: boolean;
  hasUserData?: boolean;
  documentsAnalyzed?: number;
  message?: string;
  forecast: {
    months: string[];
    actual_collections?: (number | null)[];
    predicted_collections: number[];
    confidence_intervals?: {
      lower: number[];
      upper: number[];
    };
    model?: string;
    accuracy: {
      r2_score: number;
      mape?: number;
      confidence_level?: number;
      model_name?: string;
      data_points?: number;
    };
    statistics?: {
      average: number;
      max: number;
      min: number;
      trend: string;
    };
  };
}

const PredictiveChart = () => {
  const [selectedDate, setSelectedDate] = useState<Date | undefined>(new Date());
  const [data, setData] = useState<ForecastData[]>([]);
  const [modelAccuracy, setModelAccuracy] = useState<number>(0);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [hasUserData, setHasUserData] = useState<boolean>(false);
  const [documentsAnalyzed, setDocumentsAnalyzed] = useState<number>(0);
  const [forecastMessage, setForecastMessage] = useState<string>('');
  const { toast } = useToast();

  // Fetch forecast data from Supabase Edge Function
  const fetchForecastData = async (date: Date | undefined) => {
    if (!date) return;
    
    setIsLoading(true);
    try {
      // Check if user is authenticated
      const { data: { user }, error: authError } = await supabase.auth.getUser();
      
      if (authError || !user) {
        throw new Error('User not authenticated');
      }

      const startMonth = format(date, 'yyyy-MM');
      
      // Call Supabase Edge Function for user-based VAT forecast
      const { data: result, error } = await supabase.functions.invoke('user-vat-forecast', {
        body: { 
          start_month: startMonth, 
          num_months: 8 
        }
      });

      if (error) {
        throw new Error(`Forecast request failed: ${error.message}`);
      }

      const forecastResponse = result as ForecastResponse;
      
      if (forecastResponse.success && forecastResponse.forecast) {
        // Store metadata about the forecast
        setHasUserData(forecastResponse.hasUserData || false);
        setDocumentsAnalyzed(forecastResponse.documentsAnalyzed || 0);
        setForecastMessage(forecastResponse.message || '');

        // Transform API data to chart format
        const chartData: ForecastData[] = forecastResponse.forecast.months.map((month, index) => {
          // Convert YYYY-MM to short month name
          const monthDate = new Date(month + '-01');
          const monthName = monthDate.toLocaleDateString('en-US', { month: 'short' });
          
          return {
            month: monthName,
            actual: forecastResponse.forecast.actual_collections 
              ? forecastResponse.forecast.actual_collections[index] 
              : null,
            predicted: forecastResponse.forecast.predicted_collections[index],
            confidence_lower: forecastResponse.forecast.confidence_intervals 
              ? forecastResponse.forecast.confidence_intervals.lower[index]
              : undefined,
            confidence_upper: forecastResponse.forecast.confidence_intervals
              ? forecastResponse.forecast.confidence_intervals.upper[index]
              : undefined
          };
        });
        
        setData(chartData);
        setModelAccuracy(forecastResponse.forecast.accuracy.r2_score * 100);

        // Show appropriate message based on data source
        if (!forecastResponse.hasUserData) {
          toast({
            title: "Generic Forecast",
            description: "No VAT documents found. Upload documents for personalized predictions.",
            variant: "default"
          });
        }
      }
    } catch (error) {
      console.error('Failed to fetch forecast data:', error);
      toast({
        title: "Forecast Error",
        description: error instanceof Error ? error.message : "Failed to load forecast data.",
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Load data on mount and when date changes
  useEffect(() => {
    fetchForecastData(selectedDate);
  }, [selectedDate]);

  const handleDateSelect = (date: Date | undefined) => {
    setSelectedDate(date);
  };

  const handleRefresh = () => {
    fetchForecastData(selectedDate);
    toast({
      title: "Refreshing Forecast",
      description: "Loading latest predictions..."
    });
  };

  return (
    <Card className="shadow-card border-border/50 bg-card/60 backdrop-blur-sm">
      <CardHeader className="flex flex-row items-center justify-between">
        <div className="flex-1">
          <CardTitle className="text-lg font-semibold text-foreground">
            VAT Collection Forecast
          </CardTitle>
          <p className="text-sm text-muted-foreground">
            {hasUserData 
              ? `Personalized predictions based on ${documentsAnalyzed} document${documentsAnalyzed !== 1 ? 's' : ''}`
              : 'ML-powered predictions with confidence intervals'
            }
          </p>
          {!hasUserData && documentsAnalyzed === 0 && (
            <Alert className="mt-2 py-2">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription className="text-xs">
                Upload VAT refund documents to get personalized forecasts based on your actual data
              </AlertDescription>
            </Alert>
          )}
        </div>
        <div className="flex space-x-2">
          <Popover>
            <PopoverTrigger asChild>
              <Button variant="outline" size="sm" disabled={isLoading}>
                <Calendar className="h-4 w-4 mr-2" />
                {selectedDate ? format(selectedDate, "MMM yyyy") : "Select Date"}
              </Button>
            </PopoverTrigger>
            <PopoverContent className="w-auto p-0" align="start">
              <CalendarComponent
                mode="single"
                selected={selectedDate}
                onSelect={handleDateSelect}
                initialFocus
                className="p-3 pointer-events-auto"
              />
            </PopoverContent>
          </Popover>
          <Button variant="outline" size="sm" onClick={handleRefresh} disabled={isLoading}>
            <RefreshCw className={`h-4 w-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
          <Button variant="outline" size="sm">
            <Download className="h-4 w-4 mr-2" />
            Export
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        {!hasUserData && documentsAnalyzed === 0 ? (
          // Show empty state when no user data
          <div className="h-80 flex items-center justify-center">
            <div className="text-center space-y-4">
              <div className="mx-auto w-16 h-16 rounded-full bg-muted flex items-center justify-center">
                <FileText className="h-8 w-8 text-muted-foreground" />
              </div>
              <div className="space-y-2">
                <h3 className="text-lg font-semibold text-foreground">No VAT Data Available</h3>
                <p className="text-sm text-muted-foreground max-w-md">
                  Upload VAT refund documents to see personalized forecasts and predictions based on your actual data.
                </p>
              </div>
              <Button 
                variant="intelligence" 
                size="sm"
                onClick={() => window.location.href = '/documents'}
              >
                <FileText className="h-4 w-4 mr-2" />
                Upload Documents
              </Button>
            </div>
          </div>
        ) : (
          // Show chart when user has data
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                <defs>
                  <linearGradient id="predictedGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="hsl(var(--intelligence-blue))" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="hsl(var(--intelligence-blue))" stopOpacity={0.1}/>
                  </linearGradient>
                  <linearGradient id="actualGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="hsl(var(--intelligence-emerald))" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="hsl(var(--intelligence-emerald))" stopOpacity={0.1}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis 
                  dataKey="month" 
                  stroke="hsl(var(--muted-foreground))"
                  fontSize={12}
                />
                <YAxis 
                  stroke="hsl(var(--muted-foreground))"
                  fontSize={12}
                  tickFormatter={(value) => `$${(value / 1000000).toFixed(1)}M`}
                />
                <Tooltip 
                  contentStyle={{
                    backgroundColor: 'hsl(var(--card))',
                    border: '1px solid hsl(var(--border))',
                    borderRadius: '6px',
                    fontSize: '12px'
                  }}
                  formatter={(value, name) => [
                    `$${(value as number / 1000000).toFixed(2)}M`,
                    name === 'actual' ? 'Actual' : 'Predicted'
                  ]}
                />
                <Area
                  type="monotone"
                  dataKey="actual"
                  stroke="hsl(var(--intelligence-emerald))"
                  strokeWidth={3}
                  fill="url(#actualGradient)"
                  name="actual"
                />
                <Area
                  type="monotone"
                  dataKey="predicted"
                  stroke="hsl(var(--intelligence-blue))"
                  strokeWidth={2}
                  strokeDasharray="5 5"
                  fill="url(#predictedGradient)"
                  name="predicted"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        )}
        <div className="flex items-center justify-between mt-4 text-sm text-muted-foreground">
          <div className="flex items-center space-x-4">
            <div className="flex items-center">
              <div className="w-3 h-3 bg-intelligence-emerald rounded-full mr-2"></div>
              <span>Actual Collections</span>
            </div>
            <div className="flex items-center">
              <div className="w-3 h-3 bg-intelligence-blue rounded-full mr-2"></div>
              <span>ML Predictions</span>
            </div>
          </div>
          <div className="text-xs">
            Model Accuracy: <span className="text-success font-medium">
              {isLoading ? 'Loading...' : `${modelAccuracy.toFixed(1)}%`}
            </span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default PredictiveChart;