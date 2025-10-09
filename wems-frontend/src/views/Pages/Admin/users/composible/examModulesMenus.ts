export const examModulesAndMenus = {
  modules: [
    { id: 15, name: 'Exam Management', description: 'Examination system', icon: 'fas fa-file-signature' },
    { id: 16, name: 'Result Processing', description: 'Result management', icon: 'fas fa-chart-line' }
  ],
  menus: [
    { id: 24, module_id: 15, name: 'Exam Dashboard', description: 'Exam overview', href: '/exam/dashboard', icon: 'fas fa-tachometer-alt' },
    { id: 25, module_id: 15, name: 'Question Bank', description: 'Question management', href: '/exam/questions', icon: 'fas fa-question-circle' },
    { id: 26, module_id: 15, name: 'Exam Schedule', description: 'Schedule exams', href: '/exam/schedule', icon: 'fas fa-calendar-alt' },
    { id: 27, module_id: 16, name: 'Result Processing', description: 'Process results', href: '/exam/results', icon: 'fas fa-chart-line' },
    { id: 28, module_id: 16, name: 'Result Publication', description: 'Publish results', href: '/exam/publish', icon: 'fas fa-bullhorn' }
  ]
}
