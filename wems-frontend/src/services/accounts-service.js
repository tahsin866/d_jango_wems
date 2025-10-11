import axios from 'axios'

// Department-specific service for accounts department (department_id: 2)
class AccountsService {
  baseUrl = 'http://127.0.0.1:8000/api/sidebar'
  departmentId = 2 // Accounts department

  // Get accounts-specific sidebar data
  async getSidebarData() {
    try {
      const response = await axios.get(`${this.baseUrl}/?department_id=${this.departmentId}`)
      return response.data
    } catch (error) {
      console.error('Failed to fetch accounts sidebar data:', error)
      throw error
    }
  }

  // Get department name
  getDepartmentName() {
    return 'accounts'
  }

  // Get department display name
  getDepartmentDisplayName() {
    return 'একাউন্টস'
  }

  // Generate welcome message for accounts dashboard
  getWelcomeMessage() {
    return 'Hello accounts'
  }

  // Check if user has access to accounts module
  hasAccess(userDepartmentId) {
    return userDepartmentId === this.departmentId
  }

  // Get accounts-specific menu items
  getAccountingModules() {
    return [
      {
        label: 'সাধারণ লেজার',
        icon: 'fas fa-book',
        items: [
          { label: 'জার্নাল এন্ট্রি', href: '/accounts/ledger/journals', icon: 'fas fa-pencil-alt' },
          { label: 'হিসাবের তালিকা', href: '/accounts/ledger/chart', icon: 'fas fa-list-alt' }
        ],
        department_id: 2
      },
      {
        label: 'পাওনাদার হিসাব',
        icon: 'fas fa-file-invoice-dollar',
        items: [
          { label: 'বিক্রেতা তালিকা', href: '/accounts/payable/vendors', icon: 'fas fa-address-book' },
          { label: 'নতুন বিল যুক্ত করুন', href: '/accounts/payable/invoice/create', icon: 'fas fa-file-invoice' },
          { label: 'বিল পরিশোধ', href: '/accounts/payable/pay', icon: 'fas fa-dollar-sign' }
        ],
        department_id: 2
      },
      {
        label: 'গ্রাহক হিসাব',
        icon: 'fas fa-money-bill-wave',
        items: [
          { label: 'গ্রাহক তালিকা', href: '/accounts/receivable/customers', icon: 'fas fa-users' },
          { label: 'নতুন বিল তৈরী করুন', href: '/accounts/receivable/invoice/create', icon: 'fas fa-file-invoice' },
          { label: 'টাকা গ্রহণ', href: '/accounts/receivable/payment/receive', icon: 'fas fa-cash-register' }
        ],
        department_id: 2
      }
    ]
  }
}

// Create singleton instance
export const accountsService = new AccountsService()

// Export composable for Vue components
export function useAccountsService() {
  return {
    getSidebarData: accountsService.getSidebarData.bind(accountsService),
    getDepartmentName: accountsService.getDepartmentName.bind(accountsService),
    getDepartmentDisplayName: accountsService.getDepartmentDisplayName.bind(accountsService),
    getWelcomeMessage: accountsService.getWelcomeMessage.bind(accountsService),
    hasAccess: accountsService.hasAccess.bind(accountsService),
    getAccountingModules: accountsService.getAccountingModules.bind(accountsService)
  }
}
