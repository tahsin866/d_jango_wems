import { ref } from 'vue';

export type AssociatedMadrasa = {
  id: number;
  madrasa_id: number;
  madrasa_name: string;
  total_students: number;
};

export type Agreement = {
  id: number;
  application_date: string;
  markaz_type: string;
  main_madrasa: string;
  associated_madrasas: AssociatedMadrasa[];
  exam_name: string;
  main_total_students: number;
  associated_total_students: number;
  main_class_counts?: Record<string, number>;
  associated_class_counts?: Record<string, number>;
  status: 'pending' | 'submitted' | 'processing' | 'approved' | 'rejected';
};

export type Stats = {
  total: number;
  pending: number;
  submitted: number;
  processing: number;
  approved: number;
  rejected: number;
};

// Global reactive state
const agreements = ref<Agreement[]>([]);
const loading = ref<boolean>(false);
const stats = ref<Stats>({
  total: 0,
  pending: 0,
  submitted: 0,
  processing: 0,
  approved: 0,
  rejected: 0
});
const examName = ref<string>('উদাহরণ পরীক্ষা ২০২৫ (ফেক ডেটা)');

// Helper function to update stats
function updateStats() {
  const allAgreements = agreements.value;
  stats.value = {
    total: allAgreements.length,
    pending: allAgreements.filter(a => a.status === 'pending').length,
    submitted: allAgreements.filter(a => a.status === 'submitted').length,
    processing: allAgreements.filter(a => a.status === 'processing').length,
    approved: allAgreements.filter(a => a.status === 'approved').length,
    rejected: allAgreements.filter(a => a.status === 'rejected').length,
  };
}



export function useAgreements() {
  // Backend fetch function
  async function fetchAgreements() {
    try {
      loading.value = true;
      const axios = (await import('@/utils/axios')).default;
      const res = await axios.get('http://localhost:8000/api/markaz/table/', {
        withCredentials: true
      });
      const data = res.data?.data || [];
      agreements.value = data.map((item: any) => ({
        id: item.id,
        application_date: item.created_at,
        markaz_type: item.markaz_type,
        main_madrasa: item.main_madrasa_name,
        associated_madrasas: item.associated_madrasas || [],
        exam_name: item.exam_name,
        main_total_students: item.main_total_students,
        associated_total_students: item.associated_total_students,
        main_class_counts: item.main_class_counts || {},
        associated_class_counts: item.associated_class_counts || {},
        status: item.status,
      }));
      updateStats();
    } catch (error) {
      console.error('Error fetching agreements:', error);
      agreements.value = [];
      updateStats();
    } finally {
      loading.value = false;
    }
  }

  // Delete agreement by ID
  function deleteAgreementById(id: number) {
    // Backend DELETE request
    import('@/utils/axios').then(({ default: axios }) => {
      axios.delete(`http://localhost:8000/api/markaz/table/${id}/`, { withCredentials: true })
        .then(() => {
          const index = agreements.value.findIndex(a => a.id === id);
          if (index !== -1) {
            agreements.value.splice(index, 1);
            updateStats();
          }
        })
        .catch((err) => {
          console.error('Delete failed:', err);
        });
    });
    return true;
  }

  // Submit agreement by ID
  function submitAgreementById(id: number) {
    const agreement = agreements.value.find(a => a.id === id);
    if (agreement && agreement.status === 'pending') {
      agreement.status = 'submitted';
      updateStats();
      return true;
    }
    return false;
  }

  // Get agreement by ID
  function getAgreementById(id: number): Agreement | undefined {
    return agreements.value.find(a => a.id === id);
  }

  // Update agreement
  function updateAgreement(id: number, updatedData: Partial<Agreement>) {
    const index = agreements.value.findIndex(a => a.id === id);
    if (index !== -1) {
      agreements.value[index] = { ...agreements.value[index], ...updatedData };
      updateStats();
      return true;
    }
    return false;
  }

  return {
    // State
    agreements,
    loading,
    stats,
    examName,

    // Actions
    fetchAgreements,
    deleteAgreementById,
    submitAgreementById,
    getAgreementById,
    updateAgreement,
    updateStats
  };
}
