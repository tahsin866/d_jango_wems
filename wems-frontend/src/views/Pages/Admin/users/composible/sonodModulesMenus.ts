export const talimModulesAndMenus = {
  modules: [
    { id: 5, name: 'Training Management', description: 'Training programs', icon: 'fas fa-chalkboard-teacher' },
    { id: 6, name: 'Curriculum Development', description: 'Course development', icon: 'fas fa-graduation-cap' }
  ],
  menus: [
    { id: 9, module_id: 5, name: 'Training Sessions', description: 'Training sessions', href: '/training/sessions', icon: 'fas fa-users' },
    { id: 10, module_id: 5, name: 'Materials', description: 'Training materials', href: '/training/materials', icon: 'fas fa-file-alt' },
    { id: 11, module_id: 6, name: 'Curriculum', description: 'Course curriculum', href: '/training/curriculum', icon: 'fas fa-graduation-cap' }
  ]
}
