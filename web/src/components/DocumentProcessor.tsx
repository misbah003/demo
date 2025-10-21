import React from "react";
import { useState, useRef, useEffect } from "react";
import { Upload, FileText, Scan, Brain, CheckCircle, AlertCircle } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { useToast } from "@/hooks/use-toast";
import { ToastAction } from "@/components/ui/toast";
import { supabase } from "@/integrations/supabase/client";
import { useNavigate } from "react-router-dom";
import { Badge } from "@/components/ui/badge";

const DocumentProcessor = () => {
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [results, setResults] = useState<any[]>([]);
  const [selectedFiles, setSelectedFiles] = useState<FileList | null>(null);
  const [mlApiStatus, setMlApiStatus] = useState<'checking' | 'online' | 'offline'>('checking');
  const { toast } = useToast();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();

  // Check ML API status on component mount
  useEffect(() => {
    const checkMLStatus = async () => {
      try {
        const response = await fetch('http://localhost:8000/health');
        const data = await response.json();
        setMlApiStatus(data.status === 'healthy' && data.model_loaded ? 'online' : 'offline');
      } catch (error) {
        setMlApiStatus('offline');
      }
    };
    
    checkMLStatus();
    // Check every 30 seconds
    const interval = setInterval(checkMLStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  const handleFileSelect = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files && files.length > 0) {
      setSelectedFiles(files);
      processFiles(files);
    }
  };

  const processFiles = async (files: FileList) => {
    setIsProcessing(true);
    setProgress(0);

    try {
      // Get current user
      const { data: { user }, error: authError } = await supabase.auth.getUser();
      
      if (authError || !user) {
        throw new Error('You must be logged in to upload documents');
      }

      const formData = new FormData();
      
      // Add user_id to form data
      formData.append('user_id', user.id);

      for (let i = 0; i < files.length; i++) {
        formData.append('documents', files[i]);
      }

      setProgress(25); // Upload started

      const response = await fetch('http://localhost:3001/api/process-document', {
        method: 'POST',
        body: formData,
      });

      setProgress(50); // Processing

      if (!response.ok) {
        throw new Error('Failed to process documents');
      }

      const data = await response.json();

      setProgress(75); // Analysis

      if (data.success) {
        setResults(data.results);
        console.log('Documents processed successfully:', data.results);
        
        // Create a summary of processed documents
        const documentSummary = data.results.map((result: any) => 
          `• ${result.filename} - ${result.classification}`
        ).join('\n');
        
        toast({
          title: "Documents Processed",
          description: (
            <div className="space-y-2">
              <p className="font-medium">Successfully processed {data.results.length} document(s):</p>
              <div className="text-sm space-y-1">
                {data.results.map((result: any, index: number) => (
                  <div key={index} className="flex items-center space-x-2">
                    <span className="text-muted-foreground">•</span>
                    <span className="font-medium">{result.filename}</span>
                    <span className="text-xs text-muted-foreground">-</span>
                    <span className={`text-xs ${
                      result.classification === "Compliant" ? "text-green-600" : "text-yellow-600"
                    }`}>
                      {result.classification}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          ),
          action: (
            <ToastAction altText="View Documents" onClick={() => navigate('/documents')}>
              View Documents
            </ToastAction>
          )
        });
      } else {
        throw new Error(data.error || 'Processing failed');
      }

      setProgress(100); // Complete

    } catch (error) {
      console.error('Processing error:', error);
      toast({
        title: "Processing Failed",
        description: error instanceof Error ? error.message : "An error occurred while processing documents",
        variant: "destructive"
      });
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <Card className="shadow-card border-border/50 bg-card/60 backdrop-blur-sm">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="text-lg font-semibold text-foreground flex items-center">
              <Brain className="h-5 w-5 mr-2 text-intelligence-blue" />
              AI Document Processing
            </CardTitle>
            <p className="text-sm text-muted-foreground">
              OCR + NLP for intelligent tax document analysis
            </p>
          </div>
          <div>
            {mlApiStatus === 'checking' && (
              <Badge variant="outline" className="animate-pulse">
                🔄 Checking...
              </Badge>
            )}
            {mlApiStatus === 'online' && (
              <Badge className="bg-green-500 hover:bg-green-600 text-white">
                🤖 ML Active (95%)
              </Badge>
            )}
            {mlApiStatus === 'offline' && (
              <Badge variant="secondary" className="bg-yellow-500/20 text-yellow-700 dark:text-yellow-400">
                📝 Regex Mode (70%)
              </Badge>
            )}
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        {!isProcessing && results.length === 0 && (
          <div className="border-2 border-dashed border-border rounded-lg p-8 text-center">
            <Upload className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
            <p className="text-sm text-muted-foreground mb-4">
              Drop tax documents here or click to upload (PDF, Excel, Images, etc.)
            </p>
            <Button variant="intelligence" onClick={handleFileSelect}>
              <FileText className="h-4 w-4 mr-2" />
              Upload Documents
            </Button>
            <input
              ref={fileInputRef}
              type="file"
              multiple
              accept=".pdf,.doc,.docx,.jpg,.jpeg,.png,.txt,.xlsx,.xls"
              onChange={handleFileChange}
              className="hidden"
            />
          </div>
        )}

        {isProcessing && (
          <div className="space-y-4">
            <div className="flex items-center space-x-3">
              <Scan className="h-5 w-5 text-intelligence-blue animate-pulse" />
              <div className="flex-1">
                <p className="text-sm font-medium text-foreground">Processing documents...</p>
                <p className="text-xs text-muted-foreground">AI models analyzing content</p>
              </div>
            </div>
            <Progress value={progress} className="h-2" />
            <p className="text-xs text-center text-muted-foreground">
              {progress}% complete
            </p>
          </div>
        )}

        {results.length > 0 && (
          <div className="space-y-4">
            <h4 className="font-medium text-foreground">Processing Results</h4>
            {results.map((result, index) => (
              <div key={index} className="border border-border/50 rounded-lg p-4 space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <FileText className="h-4 w-4 text-intelligence-blue" />
                    <span className="text-sm font-medium text-foreground">
                      {result.filename}
                    </span>
                  </div>
                  <div className="flex items-center space-x-2">
                    {result.classification === "Compliant" ? (
                      <CheckCircle className="h-4 w-4 text-success" />
                    ) : (
                      <AlertCircle className="h-4 w-4 text-intelligence-amber" />
                    )}
                    <span className={`text-xs ${
                      result.classification === "Compliant" ? "text-success" : "text-intelligence-amber"
                    }`}>
                      {result.classification}
                    </span>
                  </div>
                </div>
                
                <div className="space-y-2">
                  <p className="text-xs text-muted-foreground">
                    Type: <span className="text-foreground">{result.type}</span>
                  </p>
                  <p className="text-xs text-muted-foreground">
                    Confidence: <span className="text-foreground">{(result.confidence * 100).toFixed(1)}%</span>
                  </p>
                  <div className="text-xs text-muted-foreground">
                    <p className="font-medium text-foreground mb-1">Extracted Information:</p>
                    <div className="grid grid-cols-2 gap-2">
                      {(() => {
                        // Group entities by type and count them
                        const entityCounts: Record<string, number> = {};
                        const entitySamples: Record<string, string[]> = {};
                        
                        result.entities.forEach((entity: string) => {
                          const [type, value] = entity.split(': ');
                          if (!entityCounts[type]) {
                            entityCounts[type] = 0;
                            entitySamples[type] = [];
                          }
                          entityCounts[type]++;
                          // Keep only first 2 samples
                          if (entitySamples[type].length < 2) {
                            entitySamples[type].push(value);
                          }
                        });

                        return Object.entries(entityCounts).map(([type, count]) => (
                          <div key={type} className="text-foreground">
                            <span className="font-medium">{type}:</span> {count}
                            {entitySamples[type].length > 0 && (
                              <div className="text-xs text-muted-foreground ml-2">
                                {entitySamples[type].slice(0, 1).join(', ')}
                                {count > 1 && ` +${count - 1} more`}
                              </div>
                            )}
                          </div>
                        ));
                      })()}
                    </div>
                  </div>
                </div>
              </div>
            ))}
            
            <div className="flex space-x-2">
              <Button variant="intelligence" size="sm" className="flex-1" onClick={() => navigate('/documents')}>
                <FileText className="h-4 w-4 mr-2" />
                View All Documents
              </Button>
              <Button variant="outline" size="sm" className="flex-1" onClick={handleFileSelect}>
                Process More
              </Button>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default DocumentProcessor;