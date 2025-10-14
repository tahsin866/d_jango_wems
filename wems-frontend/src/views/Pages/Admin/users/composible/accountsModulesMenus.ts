export const accountsModulesAndMenus = {
  modules: [
    { id: 1, name: 'Accounts Management', description: 'Financial operations', icon: 'fas fa-money-check-alt' },
    { id: 2, name: 'Budget Planning', description: 'Budget management', icon: 'fas fa-calculator' }
  ],
  menus: [
    { id: 1, module_id: 1, name: 'Dashboard', description: 'Accounts overview', href: '/accounts/dashboard', icon: 'fas fa-tachometer-alt' },
    { id: 2, module_id: 1, name: 'Transactions', description: 'Financial transactions', href: '/accounts/transactions', icon: 'fas fa-exchange-alt' },
    { id: 3, module_id: 1, name: 'Reports', description: 'Financial reports', href: '/accounts/reports', icon: 'fas fa-chart-bar' },
    { id: 4, module_id: 2, name: 'Budget Planning', description: 'Annual budget', href: '/accounts/budget', icon: 'fas fa-calculator' }
  ]
}
