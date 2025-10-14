import { ref } from 'vue'

const agreements = ref([])
const loading = ref(false)
const stats = ref({
  total: 0,
  pending: 0,
  submitted: 0,
  processing: 0,
  approved: 0,
  rejected: 0
})
const examName = ref('উদাহরণ পরীক্ষা ২০২৫ (ফেক ডেটা)')

// Helper function to update stats
function updateStats() {
  const allAgreements = agreements.value
  stats.value = {
    total: allAgreements.length,
    pending: allAgreements.filter(a => a.status === 'pending').length,
    submitted: allAgreements.filter(a => a.status === 'submitted').length,
    processing: allAgreements.filter(a => a.status === 'processing').length,
    approved: allAgreements.filter(a => a.status === 'approved').length,
    rejected: allAgreements.filter(a => a.status === 'rejected').length,
  }
}

export function useAgreements() {
  // Backend fetch function
  async function fetchAgreements() {
    try {
      loading.value = true
      const axios = (await import('@/utils/axios')).default
      const res = await axios.get('http://localhost:8000/api/markaz/table/', {
        withCredentials: true
      })
      const data = res.data?.data || []
      agreements.value = data.map(item => ({
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
      }))
      updateStats()
    } catch  {
      agreements.value = []
      updateStats()
    } finally {
      loading.value = false
    }
  }

  // Delete agreement by ID
  function deleteAgreementById(id) {
    import('@/utils/axios').then(({ default: axios }) => {
      axios.delete(`http://localhost:8000/api/markaz/table/${id}/`, { withCredentials: true })
        .then(() => {
          const index = agreements.value.findIndex(a => a.id === id)
          if (index !== -1) {
            agreements.value.splice(index, 1)
            updateStats()
          }
        })
        .catch(() => {})
    })
    return true
  }

  // Submit agreement by ID
  function submitAgreementById(id) {
    const agreement = agreements.value.find(a => a.id === id)
    if (agreement && agreement.status === 'pending') {
      agreement.status = 'submitted'
      updateStats()
      return true
    }
    return false
  }

  // Get agreement by ID
  function getAgreementById(id) {
    return agreements.value.find(a => a.id === id)
  }

  // Update agreement
  function updateAgreement(id, updatedData) {
    const index = agreements.value.findIndex(a => a.id === id)
    if (index !== -1) {
      agreements.value[index] = { ...agreements.value[index], ...updatedData }
      updateStats()
      return true
    }
    return false
  }

  return {
    agreements,
    loading,
    stats,
    examName,
    fetchAgreements,
    deleteAgreementById,
    submitAgreementById,
    getAgreementById,
    updateAgreement,
    updateStats
  }
}
