import React from "react";
import { useState } from "react";
import { FileText, CheckCircle, AlertCircle, Calendar, Tag, Download, Trash2, Search, CheckSquare, Square, Eye } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { useProcessedDocuments } from "@/hooks/useProcessedDocuments";
import Layout from "@/components/Layout";
import { format } from "date-fns";
import { useToast } from "@/hooks/use-toast";
import { supabase } from "@/integrations/supabase/client";
import * as XLSX from 'xlsx';

const Documents = () => {
  const { documents, loading, error, refetch } = useProcessedDocuments();
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedDocuments, setSelectedDocuments] = useState<string[]>([]);
  const [isDeleting, setIsDeleting] = useState(false);
  const { toast } = useToast();

  // Filter documents based on search query
  const filteredDocuments = documents.filter((doc) =>
    doc.filename.toLowerCase().includes(searchQuery.toLowerCase()) ||
    doc.type.toLowerCase().includes(searchQuery.toLowerCase()) ||
    doc.classification.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Toggle document selection
  const toggleDocumentSelection = (docId: string) => {
    setSelectedDocuments(prev => 
      prev.includes(docId) 
        ? prev.filter(id => id !== docId)
        : [...prev, docId]
    );
  };

  // Select all documents
  const selectAllDocuments = () => {
    if (selectedDocuments.length === filteredDocuments.length) {
      setSelectedDocuments([]);
    } else {
      setSelectedDocuments(filteredDocuments.map(doc => doc.id));
    }
  };

  // Download single document
  const handleDownload = async (docId: string, filename: string) => {
    try {
      const { data: docData, error: fetchError } = await supabase
        .from('processed_documents')
        .select('*')
        .eq('id', docId)
        .single();

      if (fetchError || !docData) {
        throw new Error('Document not found');
      }

      // Create Excel workbook
      const wb = XLSX.utils.book_new();

      // Sheet 1: Document Information
      const docInfo = [
        ['Document Report'],
        [''],
        ['Field', 'Value'],
        ['Filename', docData.filename],
        ['Type', docData.type],
        ['Classification', docData.classification],
        ['Confidence', docData.confidence ? `${(docData.confidence * 100).toFixed(2)}%` : 'N/A'],
        ['Processed At', docData.processed_at ? format(new Date(docData.processed_at), 'PPpp') : 'N/A'],
        ['Created At', docData.created_at ? format(new Date(docData.created_at), 'PPpp') : 'N/A'],
        ['Document ID', docData.id],
      ];
      const ws1 = XLSX.utils.aoa_to_sheet(docInfo);
      
      // Set column widths
      ws1['!cols'] = [{ wch: 20 }, { wch: 50 }];
      
      XLSX.utils.book_append_sheet(wb, ws1, 'Document Info');

      // Sheet 2: Extracted Entities
      if (docData.entities && typeof docData.entities === 'object') {
        const entities = docData.entities as Record<string, any>;
        const entityData = [
          ['Extracted Entities'],
          [''],
          ['Entity Type', 'Value'],
        ];

        Object.entries(entities).forEach(([key, value]) => {
          if (value !== null && value !== undefined) {
            const displayValue = typeof value === 'object' ? JSON.stringify(value) : String(value);
            entityData.push([key, displayValue]);
          }
        });

        const ws2 = XLSX.utils.aoa_to_sheet(entityData);
        ws2['!cols'] = [{ wch: 25 }, { wch: 60 }];
        XLSX.utils.book_append_sheet(wb, ws2, 'Entities');
      }

      // Generate Excel file and download
      const excelBuffer = XLSX.write(wb, { bookType: 'xlsx', type: 'array' });
      const blob = new Blob([excelBuffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${filename.replace(/\.[^/.]+$/, '')}_report.xlsx`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      toast({
        title: "Download Successful",
        description: `${filename} report downloaded as Excel file.`,
      });
    } catch (error) {
      console.error('Download error:', error);
      const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
      toast({
        title: "Download Failed",
        description: errorMessage,
        variant: "destructive",
      });
    }
  };

  // View/Download original file
  const handleViewOriginal = async (docId: string, filename: string) => {
    try {
      // Fetch document to get file_path
      const { data: docData, error: fetchError } = await supabase
        .from('processed_documents')
        .select('file_path')
        .eq('id', docId)
        .single();

      if (fetchError || !docData) {
        throw new Error('Document not found');
      }

      if (!docData.file_path) {
        toast({
          title: "Original File Not Available",
          description: "This document was processed before file storage was enabled. Only the processed report is available.",
          variant: "destructive",
        });
        return;
      }

      // Download file from Supabase Storage
      const { data: fileData, error: downloadError } = await supabase.storage
        .from('documents')
        .download(docData.file_path);

      if (downloadError || !fileData) {
        throw new Error('Failed to download original file');
      }

      // Create download link
      const url = window.URL.createObjectURL(fileData);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      toast({
        title: "Download Successful",
        description: `Original file "${filename}" downloaded successfully.`,
      });
    } catch (error) {
      console.error('View original error:', error);
      const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
      toast({
        title: "Download Failed",
        description: errorMessage,
        variant: "destructive",
      });
    }
  };

  // Delete single document
  const handleDelete = async (docId: string, filename: string) => {
    if (!confirm(`Are you sure you want to delete "${filename}"?`)) {
      return;
    }

    setIsDeleting(true);
    try {
      const { error: deleteError } = await supabase
        .from('processed_documents')
        .delete()
        .eq('id', docId);

      if (deleteError) {
        throw deleteError;
      }
      
      toast({
        title: "Document Deleted",
        description: `${filename} has been deleted successfully.`,
      });

      // Refresh the documents list
      refetch();
    } catch (error) {
      console.error('Delete error:', error);
      const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
      toast({
        title: "Delete Failed",
        description: errorMessage,
        variant: "destructive",
      });
    } finally {
      setIsDeleting(false);
    }
  };

  // Bulk delete documents
  const handleBulkDelete = async () => {
    if (selectedDocuments.length === 0) {
      toast({
        title: "No Documents Selected",
        description: "Please select documents to delete.",
        variant: "destructive",
      });
      return;
    }

    if (!confirm(`Are you sure you want to delete ${selectedDocuments.length} document(s)?`)) {
      return;
    }

    setIsDeleting(true);
    try {
      const { error: deleteError } = await supabase
        .from('processed_documents')
        .delete()
        .in('id', selectedDocuments);

      if (deleteError) {
        throw deleteError;
      }

      toast({
        title: "Documents Deleted",
        description: `${selectedDocuments.length} document(s) deleted successfully.`,
      });

      // Clear selection and refresh
      setSelectedDocuments([]);
      refetch();
    } catch (error) {
      console.error('Bulk delete error:', error);
      const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
      toast({
        title: "Delete Failed",
        description: errorMessage,
        variant: "destructive",
      });
    } finally {
      setIsDeleting(false);
    }
  };

  const getClassificationColor = (classification: string) => {
    switch (classification.toLowerCase()) {
      case "compliant":
        return "bg-green-500/10 text-green-600 border-green-500/20";
      case "basic information":
        return "bg-blue-500/10 text-blue-600 border-blue-500/20";
      case "partial information":
        return "bg-yellow-500/10 text-yellow-600 border-yellow-500/20";
      case "missing key information":
        return "bg-red-500/10 text-red-600 border-red-500/20";
      default:
        return "bg-gray-500/10 text-gray-600 border-gray-500/20";
    }
  };

  const getClassificationIcon = (classification: string) => {
    if (classification.toLowerCase() === "compliant") {
      return <CheckCircle className="h-4 w-4" />;
    }
    return <AlertCircle className="h-4 w-4" />;
  };

  if (loading) {
    return (
      <Layout>
        <div className="container mx-auto p-6">
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-intelligence-blue mx-auto mb-4"></div>
              <p className="text-muted-foreground">Loading documents...</p>
            </div>
          </div>
        </div>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout>
        <div className="container mx-auto p-6">
          <Card className="border-red-500/20 bg-red-500/5">
            <CardContent className="pt-6">
              <div className="flex items-center space-x-2 text-red-600">
                <AlertCircle className="h-5 w-5" />
                <p>Error loading documents: {error}</p>
              </div>
            </CardContent>
          </Card>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="container mx-auto p-6 space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-foreground">Uploaded Documents</h1>
            <p className="text-muted-foreground mt-1">
              View and manage all your processed tax documents
            </p>
          </div>
          <Badge variant="outline" className="text-lg px-4 py-2">
            {documents.length} {documents.length === 1 ? "Document" : "Documents"}
          </Badge>
        </div>

        {/* Search Bar */}
        <Card>
          <CardContent className="pt-6">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                type="text"
                placeholder="Search by filename, type, or classification..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
          </CardContent>
        </Card>

        {/* Bulk Actions Toolbar */}
        {filteredDocuments.length > 0 && (
          <Card className="bg-muted/50">
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={selectAllDocuments}
                    className="flex items-center space-x-2"
                  >
                    {selectedDocuments.length === filteredDocuments.length ? (
                      <CheckSquare className="h-4 w-4" />
                    ) : (
                      <Square className="h-4 w-4" />
                    )}
                    <span>
                      {selectedDocuments.length === filteredDocuments.length
                        ? "Deselect All"
                        : "Select All"}
                    </span>
                  </Button>
                  {selectedDocuments.length > 0 && (
                    <Badge variant="secondary" className="text-sm">
                      {selectedDocuments.length} selected
                    </Badge>
                  )}
                </div>
                {selectedDocuments.length > 0 && (
                  <Button
                    variant="destructive"
                    size="sm"
                    onClick={handleBulkDelete}
                    disabled={isDeleting}
                    className="flex items-center space-x-2"
                  >
                    <Trash2 className="h-4 w-4" />
                    <span>{isDeleting ? "Deleting..." : `Delete ${selectedDocuments.length} Document(s)`}</span>
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Documents List */}
        {filteredDocuments.length === 0 ? (
          <Card>
            <CardContent className="pt-6">
              <div className="text-center py-12">
                <FileText className="h-16 w-16 text-muted-foreground mx-auto mb-4 opacity-50" />
                <h3 className="text-lg font-semibold text-foreground mb-2">
                  {searchQuery ? "No documents found" : "No documents uploaded yet"}
                </h3>
                <p className="text-muted-foreground">
                  {searchQuery
                    ? "Try adjusting your search query"
                    : "Upload your first document to get started"}
                </p>
              </div>
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-4">
            {filteredDocuments.map((doc) => (
              <Card 
                key={doc.id} 
                className={`hover:shadow-lg transition-all ${
                  selectedDocuments.includes(doc.id) 
                    ? 'ring-2 ring-intelligence-blue bg-intelligence-blue/5' 
                    : ''
                }`}
              >
                <CardContent className="pt-6">
                  <div className="flex items-start justify-between">
                    {/* Checkbox */}
                    <div className="flex items-start space-x-4 flex-1">
                      <button
                        onClick={() => toggleDocumentSelection(doc.id)}
                        className="mt-1 flex-shrink-0 focus:outline-none focus:ring-2 focus:ring-intelligence-blue rounded"
                      >
                        {selectedDocuments.includes(doc.id) ? (
                          <CheckSquare className="h-5 w-5 text-intelligence-blue" />
                        ) : (
                          <Square className="h-5 w-5 text-muted-foreground hover:text-intelligence-blue" />
                        )}
                      </button>

                      {/* Left Section - Document Info */}
                      <div className="flex-1 space-y-3">
                      {/* Filename and Type */}
                      <div className="flex items-center space-x-3">
                        <FileText className="h-5 w-5 text-intelligence-blue flex-shrink-0" />
                        <div>
                          <h3 className="font-semibold text-foreground text-lg">
                            {doc.filename}
                          </h3>
                          <p className="text-sm text-muted-foreground">
                            Type: {doc.type}
                          </p>
                        </div>
                      </div>

                      {/* Classification Badge */}
                      <div className="flex items-center space-x-2">
                        <Badge
                          variant="outline"
                          className={`${getClassificationColor(doc.classification)} flex items-center space-x-1`}
                        >
                          {getClassificationIcon(doc.classification)}
                          <span>{doc.classification}</span>
                        </Badge>
                        <Badge variant="outline" className="bg-intelligence-blue/10 text-intelligence-blue border-intelligence-blue/20">
                          Confidence: {(doc.confidence * 100).toFixed(1)}%
                        </Badge>
                      </div>

                      {/* Extracted Entities */}
                      {doc.entities && Array.isArray(doc.entities) && doc.entities.length > 0 && (
                        <div className="space-y-2">
                          <p className="text-sm font-medium text-foreground flex items-center">
                            <Tag className="h-4 w-4 mr-2 text-intelligence-blue" />
                            Extracted Information:
                          </p>
                          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                            {(() => {
                              // Group entities by type and count them
                              const entityCounts: Record<string, number> = {};
                              const entitySamples: Record<string, string[]> = {};
                              
                              doc.entities.forEach((entity: string) => {
                                const [type, value] = entity.split(': ');
                                if (!entityCounts[type]) {
                                  entityCounts[type] = 0;
                                  entitySamples[type] = [];
                                }
                                entityCounts[type]++;
                                // Keep only first sample
                                if (entitySamples[type].length < 1) {
                                  entitySamples[type].push(value);
                                }
                              });

                              return Object.entries(entityCounts).map(([type, count]) => (
                                <div key={type} className="bg-muted/50 rounded-lg p-3 border border-border/50">
                                  <div className="text-sm font-semibold text-foreground">
                                    {type}
                                  </div>
                                  <div className="text-lg font-bold text-intelligence-blue">
                                    {count}
                                  </div>
                                  {entitySamples[type].length > 0 && (
                                    <div className="text-xs text-muted-foreground truncate mt-1">
                                      {entitySamples[type][0]}
                                      {count > 1 && ` +${count - 1}`}
                                    </div>
                                  )}
                                </div>
                              ));
                            })()}
                          </div>
                        </div>
                      )}

                      {/* Date */}
                      <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                        <Calendar className="h-4 w-4" />
                        <span>
                          Processed: {format(new Date(doc.processed_at), "PPpp")}
                        </span>
                      </div>
                      </div>
                    </div>

                    {/* Right Section - Actions */}
                    <div className="flex flex-col space-y-2 ml-4">
                      <Button 
                        variant="outline" 
                        size="sm" 
                        className="w-full"
                        onClick={() => handleDownload(doc.id, doc.filename)}
                      >
                        <Download className="h-4 w-4 mr-2" />
                        Download Report
                      </Button>
                      <Button 
                        variant="outline" 
                        size="sm" 
                        className="w-full"
                        onClick={() => handleViewOriginal(doc.id, doc.filename)}
                      >
                        <Eye className="h-4 w-4 mr-2" />
                        View Original
                      </Button>
                      <Button 
                        variant="outline" 
                        size="sm" 
                        className="w-full text-red-600 hover:text-red-700 hover:bg-red-50"
                        onClick={() => handleDelete(doc.id, doc.filename)}
                        disabled={isDeleting}
                      >
                        <Trash2 className="h-4 w-4 mr-2" />
                        {isDeleting ? "Deleting..." : "Delete"}
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </Layout>
  );
};

export default Documents;