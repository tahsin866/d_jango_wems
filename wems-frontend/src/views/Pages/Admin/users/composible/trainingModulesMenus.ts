export const trainingModulesAndMenus = {
  modules: [
    { id: 13, name: 'Training Programs', description: 'Training coordination', icon: 'fas fa-clipboard-list' },
    { id: 14, name: 'Resource Management', description: 'Training resources', icon: 'fas fa-box' }
  ],
  menus: [
    { id: 21, module_id: 13, name: 'Program Scheduling', description: 'Schedule training', href: '/training-dept/schedule', icon: 'fas fa-calendar' },
    { id: 22, module_id: 13, name: 'Participant Management', description: 'Manage participants', href: '/training-dept/participants', icon: 'fas fa-users' },
    { id: 23, module_id: 14, name: 'Resource Allocation', description: 'Allocate resources', href: '/training-dept/resources', icon: 'fas fa-box' }
  ]
}
