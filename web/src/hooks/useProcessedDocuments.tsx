import { useState, useEffect } from 'react';
import { supabase } from '@/integrations/supabase/client';
import type { Tables } from '@/integrations/supabase/types';

export type ProcessedDocument = Tables<'processed_documents'>;

export const useProcessedDocuments = () => {
  const [documents, setDocuments] = useState<ProcessedDocument[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDocuments = async () => {
    try {
      setLoading(true);
      const { data, error: fetchError } = await supabase
        .from('processed_documents')
        .select('*')
        .order('processed_at', { ascending: false });

      if (fetchError) throw fetchError;

      setDocuments(data || []);
      setError(null);
    } catch (err) {
      console.error('Error fetching documents:', err);
      setError(err instanceof Error ? err.message : 'Failed to fetch documents');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();

    // Set up real-time subscription
    const channel = supabase
      .channel('processed_documents_changes')
      .on(
        'postgres_changes',
        {
          event: '*',
          schema: 'public',
          table: 'processed_documents'
        },
        (payload) => {
          console.log('Document change detected:', payload);
          fetchDocuments(); // Refetch all documents when changes occur
        }
      )
      .subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  }, []);

  return { documents, loading, error, refetch: fetchDocuments };
};