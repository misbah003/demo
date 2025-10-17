import React from "react";
import { useState } from "react";
import { Calculator, TrendingUp, DollarSign, Clock, AlertCircle } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { useToast } from "@/hooks/use-toast";
import { supabase } from "@/integrations/supabase/client";
import * as XLSX from 'xlsx';

const VATRefundPredictor = () => {
  const [formData, setFormData] = useState({
    businessType: "",
    annualTurnover: "",
    vatPaid: "",
    inputVAT: "",
    category: "Electronics",
    region: "Maharashtra",
    filingStatus: "Filed"
  });
  const [prediction, setPrediction] = useState<any>(null);
  const [isCalculating, setIsCalculating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isSavingApplication, setIsSavingApplication] = useState(false);
  const { toast } = useToast();

  // Map states to known regions in the ML model
  // The model only knows these 10 regions: Delhi, Gujarat, Haryana, Karnataka, Kerala, Maharashtra, Punjab, Rajasthan, Tamil Nadu, Uttar Pradesh
  const stateToRegionMap: { [key: string]: string } = {
    // States that match model regions exactly
    "Delhi": "Delhi",
    "Gujarat": "Gujarat",
    "Haryana": "Haryana",
    "Karnataka": "Karnataka",
    "Kerala": "Kerala",
    "Maharashtra": "Maharashtra",
    "Punjab": "Punjab",
    "Rajasthan": "Rajasthan",
    "Tamil Nadu": "Tamil Nadu",
    "Uttar Pradesh": "Uttar Pradesh",
    
    // Map other North states to closest known region
    "Himachal Pradesh": "Punjab",
    "Jammu and Kashmir": "Punjab",
    "Ladakh": "Punjab",
    "Uttarakhand": "Uttar Pradesh",
    "Chandigarh": "Punjab",
    
    // Map other South states to closest known region
    "Andhra Pradesh": "Tamil Nadu",
    "Telangana": "Karnataka",
    "Puducherry": "Tamil Nadu",
    "Lakshadweep": "Kerala",
    "Andaman and Nicobar Islands": "Tamil Nadu",
    
    // Map East states to closest known region
    "Bihar": "Uttar Pradesh",
    "Jharkhand": "Uttar Pradesh",
    "Odisha": "Uttar Pradesh",
    "West Bengal": "Uttar Pradesh",
    "Assam": "Uttar Pradesh",
    "Arunachal Pradesh": "Uttar Pradesh",
    "Manipur": "Uttar Pradesh",
    "Meghalaya": "Uttar Pradesh",
    "Mizoram": "Uttar Pradesh",
    "Nagaland": "Uttar Pradesh",
    "Sikkim": "Uttar Pradesh",
    "Tripura": "Uttar Pradesh",
    
    // Map West states to closest known region
    "Goa": "Maharashtra",
    "Chhattisgarh": "Maharashtra",
    "Madhya Pradesh": "Rajasthan",
    "Dadra and Nagar Haveli and Daman and Diu": "Gujarat"
  };

  const handleCalculate = async () => {
    setIsCalculating(true);
    setError(null);

    try {
      // Map frontend fields to API fields
      const businessTypeMapping: { [key: string]: string } = {
        "manufacturing": "Manufacturing",
        "services": "Services",
        "trading": "Trading",
        "retail": "Retail"
      };

      // Convert state to region for API compatibility
      const mappedRegion = stateToRegionMap[formData.region] || formData.region;

      const apiPayload = {
        businessType: businessTypeMapping[formData.businessType] || formData.businessType,
        turnover: parseFloat(formData.annualTurnover.replace(/,/g, '')) || 0,
        vatPaid: parseFloat(formData.vatPaid.replace(/,/g, '')) || 0,
        vatClaimed: parseFloat(formData.inputVAT.replace(/,/g, '')) || 0,
        category: formData.category,
        region: mappedRegion, // Use mapped region instead of state
        filingStatus: formData.filingStatus,
        riskScore: 0.3 // Default risk score, can be enhanced later
      };

      console.log("Sending prediction request:", apiPayload);

      const response = await fetch('http://localhost:5001/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(apiPayload),
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status} ${response.statusText}`);
      }

      const result = await response.json();

      if (result.error) {
        throw new Error(result.error);
      }

      console.log("Prediction result:", result);

      setPrediction({
        refundAmount: result.predictedRefund,
        approvalProbability: result.approvalProbability,
        processingDays: Math.floor(10 + Math.random() * 15), // Estimated based on business rules
        riskFactors: result.breakdown.adjustments,
        riskLevel: result.riskAssessment.level,
        complianceFlag: result.riskAssessment.complianceFlag,
        modelInfo: result.modelInfo
      });

      toast({
        title: "Prediction Complete",
        description: `Estimated refund: ₹${result.predictedRefund.toLocaleString()} (${result.approvalProbability.toFixed(1)}% approval probability)`,
      });

    } catch (err) {
      console.error("Prediction error:", err);
      setError(err instanceof Error ? err.message : "Failed to get prediction");
      toast({
        title: "Prediction Failed",
        description: err instanceof Error ? err.message : "Unable to connect to ML service",
        variant: "destructive",
      });
    } finally {
      setIsCalculating(false);
    }
  };

  return (
    <Card className="shadow-card border-border/50 bg-card/60 backdrop-blur-sm">
      <CardHeader>
        <CardTitle className="text-lg font-semibold text-foreground flex items-center">
          <Calculator className="h-5 w-5 mr-2 text-intelligence-emerald" />
          VAT Refund Predictor
        </CardTitle>
        <p className="text-sm text-muted-foreground">
          ML-powered refund estimation for SMEs
        </p>
      </CardHeader>
      <CardContent className="space-y-6">
        {error && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="businessType">Business Type *</Label>
            <Select onValueChange={(value) => setFormData({...formData, businessType: value})}>
              <SelectTrigger>
                <SelectValue placeholder="Select business type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="manufacturing">Manufacturing</SelectItem>
                <SelectItem value="services">Services</SelectItem>
                <SelectItem value="trading">Trading</SelectItem>
                <SelectItem value="retail">Retail</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="category">Product Category</Label>
            <Select onValueChange={(value) => setFormData({...formData, category: value})}>
              <SelectTrigger>
                <SelectValue placeholder="Select category" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="Electronics">Electronics</SelectItem>
                <SelectItem value="Textiles">Textiles</SelectItem>
                <SelectItem value="Food">Food & Beverages</SelectItem>
                <SelectItem value="Pharmaceuticals">Pharmaceuticals</SelectItem>
                <SelectItem value="Automotive">Automotive</SelectItem>
                <SelectItem value="Construction">Construction</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="turnover">Annual Turnover (₹) *</Label>
            <Input
              id="turnover"
              placeholder="e.g., 50,00,000"
              value={formData.annualTurnover}
              onChange={(e) => setFormData({...formData, annualTurnover: e.target.value})}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="state">State / Union Territory</Label>
            <Select onValueChange={(value) => setFormData({...formData, region: value})}>
              <SelectTrigger>
                <SelectValue placeholder="Select your state" />
              </SelectTrigger>
              <SelectContent className="max-h-[300px]">
                <SelectItem value="Andhra Pradesh">Andhra Pradesh</SelectItem>
                <SelectItem value="Arunachal Pradesh">Arunachal Pradesh</SelectItem>
                <SelectItem value="Assam">Assam</SelectItem>
                <SelectItem value="Bihar">Bihar</SelectItem>
                <SelectItem value="Chhattisgarh">Chhattisgarh</SelectItem>
                <SelectItem value="Goa">Goa</SelectItem>
                <SelectItem value="Gujarat">Gujarat</SelectItem>
                <SelectItem value="Haryana">Haryana</SelectItem>
                <SelectItem value="Himachal Pradesh">Himachal Pradesh</SelectItem>
                <SelectItem value="Jharkhand">Jharkhand</SelectItem>
                <SelectItem value="Karnataka">Karnataka</SelectItem>
                <SelectItem value="Kerala">Kerala</SelectItem>
                <SelectItem value="Madhya Pradesh">Madhya Pradesh</SelectItem>
                <SelectItem value="Maharashtra">Maharashtra</SelectItem>
                <SelectItem value="Manipur">Manipur</SelectItem>
                <SelectItem value="Meghalaya">Meghalaya</SelectItem>
                <SelectItem value="Mizoram">Mizoram</SelectItem>
                <SelectItem value="Nagaland">Nagaland</SelectItem>
                <SelectItem value="Odisha">Odisha</SelectItem>
                <SelectItem value="Punjab">Punjab</SelectItem>
                <SelectItem value="Rajasthan">Rajasthan</SelectItem>
                <SelectItem value="Sikkim">Sikkim</SelectItem>
                <SelectItem value="Tamil Nadu">Tamil Nadu</SelectItem>
                <SelectItem value="Telangana">Telangana</SelectItem>
                <SelectItem value="Tripura">Tripura</SelectItem>
                <SelectItem value="Uttar Pradesh">Uttar Pradesh</SelectItem>
                <SelectItem value="Uttarakhand">Uttarakhand</SelectItem>
                <SelectItem value="West Bengal">West Bengal</SelectItem>
                <SelectItem value="Andaman and Nicobar Islands">Andaman and Nicobar Islands</SelectItem>
                <SelectItem value="Chandigarh">Chandigarh</SelectItem>
                <SelectItem value="Dadra and Nagar Haveli and Daman and Diu">Dadra and Nagar Haveli and Daman and Diu</SelectItem>
                <SelectItem value="Delhi">Delhi</SelectItem>
                <SelectItem value="Jammu and Kashmir">Jammu and Kashmir</SelectItem>
                <SelectItem value="Ladakh">Ladakh</SelectItem>
                <SelectItem value="Lakshadweep">Lakshadweep</SelectItem>
                <SelectItem value="Puducherry">Puducherry</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="vatPaid">Output VAT Paid (₹) *</Label>
            <Input
              id="vatPaid"
              placeholder="e.g., 2,00,000"
              value={formData.vatPaid}
              onChange={(e) => setFormData({...formData, vatPaid: e.target.value})}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="inputVAT">Input VAT Claimed (₹) *</Label>
            <Input
              id="inputVAT"
              placeholder="e.g., 2,50,000"
              value={formData.inputVAT}
              onChange={(e) => setFormData({...formData, inputVAT: e.target.value})}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="filingStatus">Filing Status</Label>
            <Select onValueChange={(value) => setFormData({...formData, filingStatus: value})}>
              <SelectTrigger>
                <SelectValue placeholder="Select filing status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="Filed">Filed on Time</SelectItem>
                <SelectItem value="Filed Late">Filed Late</SelectItem>
                <SelectItem value="Not Filed">Not Filed</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

        <Button
          variant="intelligence"
          className="w-full"
          onClick={handleCalculate}
          disabled={isCalculating || !formData.businessType || !formData.annualTurnover || !formData.vatPaid || !formData.inputVAT}
        >
          {isCalculating ? "Calculating..." : "Predict Refund"}
        </Button>

        {prediction && (
          <div className="space-y-4 pt-4 border-t border-border/50">
            <h4 className="font-medium text-foreground">Prediction Results</h4>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-gradient-success rounded-lg p-4 text-center">
                <DollarSign className="h-6 w-6 text-white mx-auto mb-2" />
                <p className="text-xs text-white/80">Estimated Refund</p>
                <p className="text-lg font-bold text-white">
                  ₹{prediction.refundAmount.toLocaleString()}
                </p>
              </div>

              <div className="bg-gradient-primary rounded-lg p-4 text-center">
                <TrendingUp className="h-6 w-6 text-white mx-auto mb-2" />
                <p className="text-xs text-white/80">Approval Probability</p>
                <p className="text-lg font-bold text-white">
                  {prediction.approvalProbability.toFixed(1)}%
                </p>
              </div>

              <div className="bg-gradient-warning rounded-lg p-4 text-center">
                <Clock className="h-6 w-6 text-white mx-auto mb-2" />
                <p className="text-xs text-white/80">Processing Time</p>
                <p className="text-lg font-bold text-white">
                  {prediction.processingDays} days
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <p className="text-sm font-medium text-foreground">Risk Assessment:</p>
                <div className="flex items-center space-x-2">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    prediction.riskLevel === 'HIGH' ? 'bg-red-100 text-red-800' :
                    prediction.riskLevel === 'MEDIUM' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-green-100 text-green-800'
                  }`}>
                    {prediction.riskLevel} RISK
                  </span>
                  <span className="text-xs text-muted-foreground">
                    Compliance: {prediction.complianceFlag}
                  </span>
                </div>
              </div>

              <div className="space-y-2">
                <p className="text-sm font-medium text-foreground">Model Info:</p>
                <p className="text-xs text-muted-foreground">
                  {prediction.modelInfo.modelName} (R²: {prediction.modelInfo.accuracy.toFixed(3)})
                </p>
              </div>
            </div>

            <div className="space-y-2">
              <p className="text-sm font-medium text-foreground">Assessment Details:</p>
              <ul className="space-y-1">
                {prediction.riskFactors.map((factor: string, index: number) => (
                  <li key={index} className="text-xs text-muted-foreground">
                    • {factor}
                  </li>
                ))}
              </ul>
            </div>
            
            <div className="flex space-x-2">
              <Button 
                variant="success" 
                size="sm" 
                className="flex-1"
                disabled={isSavingApplication}
                onClick={async () => {
                  setIsSavingApplication(true);
                  try {
                    // Get authenticated user
                    const { data: { user }, error: authError } = await supabase.auth.getUser();
                    
                    if (authError || !user) {
                      throw new Error('Please log in to submit an application');
                    }

                    // Save application to database
                    const { error: insertError } = await supabase
                      .from('vat_applications')
                      .insert({
                        user_id: user.id,
                        business_type: formData.businessType,
                        annual_turnover: parseFloat(formData.annualTurnover),
                        vat_paid: parseFloat(formData.vatPaid),
                        input_vat: parseFloat(formData.inputVAT),
                        category: formData.category,
                        region: formData.region,
                        filing_status: formData.filingStatus,
                        predicted_refund: prediction.refundAmount,
                        approval_probability: prediction.approvalProbability,
                        processing_days: prediction.processingDays,
                        risk_level: prediction.riskLevel,
                        compliance_flag: prediction.complianceFlag,
                        status: 'Submitted',
                        submitted_at: new Date().toISOString()
                      });

                    if (insertError) {
                      throw insertError;
                    }

                    toast({
                      title: "Application Submitted Successfully",
                      description: "Your VAT refund application has been saved. You can track its status in your dashboard.",
                    });
                  } catch (error) {
                    console.error('Error saving application:', error);
                    toast({
                      title: "Application Failed",
                      description: error instanceof Error ? error.message : "Failed to submit application. Please try again.",
                      variant: "destructive"
                    });
                  } finally {
                    setIsSavingApplication(false);
                  }
                }}
              >
                {isSavingApplication ? "Submitting..." : "Start Application"}
              </Button>
              <Button 
                variant="outline" 
                size="sm" 
                className="flex-1"
                onClick={() => {
                  try {
                    // Create Excel workbook
                    const wb = XLSX.utils.book_new();
                    
                    // Prepare data for Excel
                    const reportData = [
                      ['VAT Refund Prediction Report'],
                      ['Generated on:', new Date().toLocaleString()],
                      [],
                      ['Prediction Details'],
                      ['Refund Amount (₹):', prediction.refundAmount.toLocaleString('en-IN', { minimumFractionDigits: 2 })],
                      ['Approval Probability (%):', prediction.approvalProbability],
                      ['Processing Days:', prediction.processingDays],
                      ['Risk Level:', prediction.riskLevel],
                      ['Compliance Status:', prediction.complianceFlag],
                      [],
                      ['Input Details'],
                      ['Business Type:', formData.businessType],
                      ['Annual Turnover (₹):', parseFloat(formData.annualTurnover).toLocaleString('en-IN')],
                      ['VAT Paid (₹):', parseFloat(formData.vatPaid).toLocaleString('en-IN')],
                      ['Input VAT (₹):', parseFloat(formData.inputVAT).toLocaleString('en-IN')],
                      ['Category:', formData.category],
                      ['Region:', formData.region],
                      ['Filing Status:', formData.filingStatus],
                      [],
                      ['Model Information'],
                      ['Model Name:', prediction.modelInfo.modelName],
                      ['Accuracy:', (prediction.modelInfo.accuracy * 100).toFixed(2) + '%'],
                      [],
                      ['Risk Factors'],
                      ...prediction.riskFactors.map((factor: string) => [factor])
                    ];
                    
                    // Create worksheet
                    const ws = XLSX.utils.aoa_to_sheet(reportData);
                    
                    // Set column widths
                    ws['!cols'] = [
                      { wch: 30 },
                      { wch: 40 }
                    ];
                    
                    // Add worksheet to workbook
                    XLSX.utils.book_append_sheet(wb, ws, 'VAT Refund Report');
                    
                    // Generate filename with timestamp
                    const filename = `vat-refund-report-${new Date().toISOString().slice(0, 10)}.xlsx`;
                    
                    // Download file
                    XLSX.writeFile(wb, filename);
                    
                    toast({
                      title: "Report Saved",
                      description: "Your VAT refund prediction report has been downloaded as Excel file.",
                    });
                  } catch (error) {
                    console.error('Error generating Excel report:', error);
                    toast({
                      title: "Export Failed",
                      description: "Failed to generate Excel report. Please try again.",
                      variant: "destructive"
                    });
                  }
                }}
              >
                Save Report
              </Button>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default VATRefundPredictor;