import { ref } from 'vue';

export type Agreement = {
  id: number;
  application_date: string;
  markaz_type: string;
  main_madrasa: string;
  associated_madrasas: string[];
  exam_name: string;
  main_total_students: number;
  associated_total_students: number;
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
  // Mock fetch function
  async function fetchAgreements() {
    try {
      loading.value = true;

      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 300));

      const mockData: Agreement[] = [
        {
          id: 1,
          application_date: '2025-08-06',
          markaz_type: 'প্রধান',
          main_madrasa: 'মাদরাসা আল-হুদা',
          associated_madrasas: ['মাদরাসা ফারুকিয়া', 'মাদরাসা ইসলামিয়া'],
          exam_name: 'বার্ষিক পরীক্ষা',
          main_total_students: 120,
          associated_total_students: 80,
          status: 'pending'
        },
        {
          id: 2,
          application_date: '2025-08-01',
          markaz_type: 'সহযোগী',
          main_madrasa: 'মাদরাসা নূরানী',
          associated_madrasas: [],
          exam_name: 'ফাইনাল পরীক্ষা',
          main_total_students: 75,
          associated_total_students: 0,
          status: 'approved'
        },
        {
          id: 3,
          application_date: '2025-08-03',
          markaz_type: 'প্রধান',
          main_madrasa: 'মাদরাসা দারুল উলুম',
          associated_madrasas: ['মাদরাসা তাকওয়া', 'মাদরাসা হিদায়া'],
          exam_name: 'মধ্যবর্তী পরীক্ষা',
          main_total_students: 95,
          associated_total_students: 60,
          status: 'submitted'
        }
      ];

      agreements.value = mockData;
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
    const index = agreements.value.findIndex(a => a.id === id);
    if (index !== -1) {
      agreements.value.splice(index, 1);
      updateStats();
      return true;
    }
    return false;
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
