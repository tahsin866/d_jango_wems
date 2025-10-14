export const publicationsModulesAndMenus = {
  modules: [
    { id: 3, name: 'Publication Management', description: 'Publishing operations', icon: 'fas fa-book-open' },
    { id: 4, name: 'Content Management', description: 'Content creation', icon: 'fas fa-edit' }
  ],
  menus: [
    { id: 5, module_id: 3, name: 'Books', description: 'Published books', href: '/publication/books', icon: 'fas fa-book' },
    { id: 6, module_id: 3, name: 'Authors', description: 'Author management', href: '/publication/authors', icon: 'fas fa-user-edit' },
    { id: 7, module_id: 4, name: 'Content Editor', description: 'Content editing', href: '/publication/editor', icon: 'fas fa-edit' },
    { id: 8, module_id: 4, name: 'Publishing Queue', description: 'Publishing schedule', href: '/publication/queue', icon: 'fas fa-clock' }
  ]
}
