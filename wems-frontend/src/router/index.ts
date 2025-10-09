import { createRouter, createWebHistory } from 'vue-router'
import axios from 'axios'
import {
  isTokenExpired,
  requiresAuth,
  isAdminAccessingUserRoute,
  isNonAdminAccessingAdminRoute,
  isAdminType,
  secureLogout
} from '@/utils/auth'

// ---- Route Definitions ----
const routes = [
  // Public Routes (No Layout)
  {
    path: '/',
    name: 'Welcome',
    component: () => import('@/Pages/WelcomePage.vue'),
    meta: { title: 'Welcome', isPublic: true },
  },
  {
    path: '/signin',
    name: 'Signin',
    component: () => import('@/views/Auth/Signin.vue'),
    meta: { title: 'Signin', isPublic: true },
  },
  {
    path: '/signup',
    name: 'Signup',
    component: () => import('@/views/Auth/Signup.vue'),
    meta: { title: 'Signup', requiresSignupToken: true, isPublic: true },
  },
  {
    path: '/error-404',
    name: '404 Error',
    component: () => import('@/views/Errors/FourZeroFour.vue'),
    meta: { title: '404 Error', isPublic: true },
  },
  {
    path: '/unauthorized',
    name: 'Unauthorized',
    component: () => import('@/views/Errors/Unauthorized.vue'),
    meta: { title: 'Unauthorized Access', isPublic: true },
  },
  {
    path: '/MadrashaCheck',
    name: 'MadrashaCheck',
    component: () => import('@/views/Auth/MadrashaCheck.vue'),
    meta: { title: 'MadrashaCheck', isPublic: true },
  },

  // Admin Routes (Admin Layout)
  {
    path: '/admin',
    component: () => import('@/components/layout/admin/AdminLayout.vue'),
    meta: { requiresAuth: true, role: 'admin', layoutType: 'admin' },
    children: [
      {
        path: '', // Empty path for default admin route
        redirect: '/admin/dashboard'
      },
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: () => import('@/views/Pages/Admin/dashboard/AdminDashboard.vue'),
        meta: { title: 'অ্যাডমিন ড্যাশবোর্ড', requiresAuth: true, role: 'admin' },
      },
      {
        path: '/user/setup',
        name: 'UserSetup',
        component: () => import('@/views/Pages/Admin/users/CreateUsers.vue'),
        meta: { title: 'ব্যবহারকারী সেটাপ', requiresAuth: true, role: 'admin' },
      },
      {
        path: 'marhala/setup',
        name: 'MarhalaSetup',
        component: () => import('@/views/Pages/Admin/setup/marhala/MarhalaSetup.vue'),
        meta: { title: 'মারহালা সেটাপ', requiresAuth: true, role: 'admin' },
      },

      {
        path: 'subject/setup/create',
        name: 'SubjectSetupCreate',
        component: () => import('@/views/Pages/Admin/setup/marhala/MarhalaSubjectInfo.vue'),
        meta: { title: 'বিষয় তৈরি', requiresAuth: true, role: 'admin' },
      },

      {
        path: 'setup/marhala/edit/:id',
        name: 'MarhalaEdit',
        component: () => import('@/views/Pages/Admin/setup/marhala/edit.vue'),
        meta: { title: 'মারহালা সম্পাদনা', requiresAuth: true, role: 'admin' },
      },


 {
        path: '/setup/list',
        name: 'subjectSetup',
        component: () => import('@/views/Pages/Admin/setup/subject/list.vue'),
        meta: { title: 'বিষয় তালিকা', requiresAuth: true, role: 'admin' },
      },


       {
        path: '/setup/edit/:id',
        name: 'subjectEdit',
        component: () => import('@/views/Pages/Admin/setup/subject/edit.vue'),
        meta: { title: 'বিষয় সংশোধন ', requiresAuth: true, role: 'admin' },
      },


// সেন্ট্রাল এক্সাম

 {
        path: '/central-exam/setup',
        name: 'CentralExamSetup',
        component: () => import('@/views/Pages/Admin/setup/CentralExam/CentralExamMange.vue'),
        meta: { title: 'সেন্ট্রাল এক্সাম সেটাপ', requiresAuth: true, role: 'admin' },
      },


 {
        path: '/central/exam/Create',
        name: 'CentralExamCreate',
        component: () => import('@/views/Pages/Admin/setup/CentralExam/Create.vue'),
        meta: { title: 'সেন্ট্রাল এক্সাম তৈরি', requiresAuth: true, role: 'admin' },
      },


       {
        path: '/central/exam/FeeSetups',
        name: 'CentralExamFeeSetups',
        component: () => import('@/views/Pages/Admin/setup/CentralExam/FeeSetups.vue'),
        meta: { title: 'সেন্ট্রাল এক্সাম ফি সেটআপ', requiresAuth: true, role: 'admin' },
      },

{
        path: '/central/exam/FeeEdit/:id',
        name: 'CentralExamFeeEdit',
        component: () => import('@/views/Pages/Admin/setup/CentralExam/FeeEdit.vue'),
        meta: { title: 'সেন্ট্রাল এক্সাম ফি সম্পাদনা', requiresAuth: true, role: 'admin' },
      },


 {
        path: '/central/exam/edit/:id',
        name: 'CentralExamEdit',
        component: () => import('@/views/Pages/Admin/setup/CentralExam/edit.vue'),
        meta: { title: 'সেন্ট্রাল এক্সাম তৈরি', requiresAuth: true, role: 'admin' },
      },


// মাদরাসা সংক্রান্ত


 {
        path: '/madrasah/list',
        name: 'madrashaList',
        component: () => import('@/views/Pages/Admin/madrasha/madrashaList.vue'),
        meta: { title: 'মাদরাসার তালিকা', requiresAuth: true, role: 'admin' },
      },




// মারকায সংক্রান্ত

 {
        path: '/markaz/list',
        name: 'markazList',
        component: () => import('@/views/Pages/Admin/markaz/markazList.vue'),
        meta: { title: 'মারকায তালিকা', requiresAuth: true, role: 'admin' },
      },




// নেগরান/মুমতাহিন


 {
        path: 'negaran/application-list',
        name: 'NegranCreate',
        component: () => import('@/views/Pages/Admin/negran/negran.vue'),
        meta: { title: 'নেগরান তৈরি', requiresAuth: true, role: 'admin' },
      },



    // একাউন্টস


 {
        path: '/accounts/ledger/journals',
        name: 'AccountsLedgerJournals',
        component: () => import('@/views/Pages/Accounts/create.vue'),
        meta: { title: 'একাউন্টস লেজার জুরিয়ালস', requiresAuth: true, role: 'admin' },
      },




// তালিম তারবিয়াত

 {
        path: '/talim/courses',
        name: 'TalimCourses',
        component: () => import('@/views/Pages/Talim-Tarbiat/talimTarbiat.vue'),
        meta: { title: 'তালিম তারবিয়াত', requiresAuth: true, role: 'admin' },
      },




    ]
  },

  // Direct admin routes for backward compatibility
  {
    path: '/AdminDashboard',
    redirect: '/admin/dashboard'
  },
  {
    path: '/user/setup',
    redirect: '/admin/user/setup'
  },
  {
    path: '/marhala/setup',
    redirect: '/admin/marhala/setup'
  },
  {
    path: '/subject/setup/create',
    redirect: '/admin/subject/setup/create'
  },
  {
    path: '/setup/list',
    redirect: '/admin/setup/list'
  },

// সেন্ট্রাল পরীক্ষা


  {
    path: '/central-exam/setup',
    redirect: '/admin/central-exam/setup'
  },


  {
    path: '/central/exam/Create',
    redirect: '/admin/CentralExam/Create'
  },

   {
    path: '/central/exam/FeeSetups',
    redirect: '/admin/CentralExamFeeSetups/FeeSetups'
  },

 {
    path: '/central/exam/FeeEdit/:id',
      redirect: (to: { params: { id: string } }) => `/admin/CentralExam/FeeEdit/${to.params.id}`
  },


  {
    path: '/central/exam/edit/:id',
    redirect: (to: { params: { id: string } }) => `/admin/CentralExam/edit/${to.params.id}`
  },


  {
    path: '/setup/edit/:id',
    redirect: (to: { params: { id: string } }) => `/admin/setup/edit/${to.params.id}`
  },




  {
    path: '/setup/marhala/edit/:id',
    redirect: (to: { params: { id: string } }) => `/admin/setup/marhala/edit/${to.params.id}`
  },
// নেগরান/মুমতাহিন
  {
    path: '/negaran/application-list',
    redirect: '/admin/negaran/application-list'
  },



// মাদরাসা তালিকা

  {
    path: '/madrasha/list/',
    redirect: '/admin/madrasha/list'
  },

// মারকায তালিকা

  {
    path: '/markaz/list',
    redirect: '/admin/markaz/list'
  },

// একাউন্টস

  {
    path: '/accounts/ledger/journals',
    redirect: '/admin/accounts/list'
  },

// তালিম তারবিয়াত

  {
    path: '/talim/courses',
    redirect: '/admin/talim/courses'
  },




  // User Routes (User Layout)
  {
    path: '/user',
    component: () => import('@/components/layout/AdminLayout.vue'),
    meta: { requiresAuth: true, role: 'user', layoutType: 'user' },
    children: [
      {
        path: '', // Empty path for default user route
        redirect: '/user/dashboard'
      },
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Ecommerce.vue'),
        meta: { title: 'ইউজার ড্যাশবোর্ড', requiresAuth: true, role: 'user' },
      },

      // Markaz Management (User Layout এর অধীনে)

// মারকায সংক্রান্ত  রাউট

      {
        path: 'markaz/list',
        name: 'MarkazList',
        component: () => import('@/views/Pages/markaz/MarkazList.vue'),
        meta: { title: 'মারকায তালিকা', requiresAuth: true, role: 'user' },
      },
      {
        path: 'markaz/apply',
        name: 'MarkazApply',
        component: () => import('@/views/Pages/markaz/markazApply.vue'),
        meta: { title: 'মারকায আবেদন', requiresAuth: true, role: 'user' },
      },


       {
        path: 'markaz/edit/:id',
        name: 'MarkazEdit',
        component: () => import('@/views/Pages/markaz/MarkazEdit.vue'),
      meta: { title: 'মারকায সম্পাদনা', requiresAuth: true, role: 'user' },
      },


      {
        path: 'markaz/change',
        name: 'MarkazChange',
        component: () => import('@/views/Pages/markaz/markazChange.vue'),
        meta: { title: 'মারকায পরিবর্তন', requiresAuth: true, role: 'user' },
      },
      {
        path: 'markaz/change/form',
        name: 'MarkazChangeForm',
        component: () => import('@/views/Pages/markaz/markazChangeForm.vue'),
        meta: { title: 'MarkazChangeForm', requiresAuth: true, role: 'user' },
      },
      {
        path: 'markaz/setup',
        name: 'MarkazSetup',
        component: () => import('@/views/Pages/markaz/markazSetup.vue'),
        meta: { title: 'MarkazSetup', requiresAuth: true, role: 'user' },
      },
      {
        path: 'confirmation',
        name: 'Confirmation',
        component: () => import('@/views/Pages/markaz/confirmation.vue'),
        meta: { title: 'Confirmation', requiresAuth: true, role: 'user' },
      },
      {
        path: 'marhala/change',
        name: 'MarhalaChange',
        component: () => import('@/views/Pages/markaz/marhalaChange.vue'),
        meta: { title: 'MarhalaChange', requiresAuth: true, role: 'user' },
      },

      // Registration (User Layout এর অধীনে)
      {
        path: 'registration/overview',
        name: 'StudentRegistrationOverview',
        component: () => import('@/views/Pages/registraion/registrationOverview.vue'),
        meta: { title: 'Student Registration Overview', requiresAuth: true, role: 'user' },
      },
      {
        path: 'registration/list',
        name: 'RegistrationList',
        component: () => import('@/views/Pages/registraion/registrationList.vue'),
        meta: { title: 'Registration List', requiresAuth: true, role: 'user' },
      },
      {
        path: 'student/old/list',
        name: 'OldStudentList',
        component: () => import('@/views/Pages/registraion/oldStudentList.vue'),
        meta: { title: 'Old Student List', requiresAuth: true, role: 'user' },
      },

      {
        path: 'student/old/verify/:marhala_id',
        name: 'VerifyOldStudents',
        component: () => import('@/views/Pages/registraion/verifyOldStudents.vue'),
        meta: { title: 'পুরাতন ছাত্রদের তথ্য যাচাই', requiresAuth: true, role: 'user' },
      },


      {
        path: 'student/old/registration/form',
        name: 'OldStudentReg',
        component: () => import('@/views/Pages/registraion/oldStudentReg.vue'),
        meta: { title: 'Old Student Registration', requiresAuth: true, role: 'user' },
      },
      {
        path: 'registration/list',
        name: 'RegistrationList',
        component: () => import('@/views/Pages/registraion/registrationTable.vue'),
        meta: { title: 'registrationTable', requiresAuth: true, role: 'user' },
      },
      {
        path: 'registration/table',
        name: 'RegistrationTable',
        component: () => import('@/views/Pages/registraion/registrationTable.vue'),
        meta: { title: 'Registration Table', requiresAuth: true, role: 'user' },
      },
      {
        path: 'restore',
        name: 'Restore',
        component: () => import('@/views/Pages/registraion/restore.vue'),
        meta: { title: 'Restore', requiresAuth: true, role: 'user' },
      },
      {
        path: 'payment',
        name: 'Payment',
        component: () => import('@/views/Pages/registraion/payment.vue'),
        meta: { title: 'Payment', requiresAuth: true, role: 'user' },
      },

      // Subject and other user routes
      {
        path: 'subject/list',
        name: 'SubjectList',
        component: () => import('@/views/Pages/Admin/setup/subject/list.vue'),
        meta: { title: 'বিষয় তালিকা', requiresAuth: true, role: 'admin' },
      },
      {
        path: 'setup/subject/list',
        name: 'SubjectSetupList',
        component: () => import('@/views/Pages/Admin/setup/subject/list.vue'),
        meta: { title: 'বিষয় সেটাপ তালিকা', requiresAuth: true, role: 'admin' },
      },
      {
        path: 'student/inclution',
        name: 'StudentInclusion',
        component: () => import('@/views/Pages/Inclusion/StudentInclusion.vue'),
        meta: { title: 'MadrashaCheck', requiresAuth: true, role: 'user' },
      },
    ]
  },

  // Direct user routes for backward compatibility
  {
    path: '/dashboard',
    redirect: '/user/dashboard'
  },

  // মারকায সংক্রান্ত  রাউট



  {
    path: '/markaz/MarkazList',
    redirect: '/user/markaz/list'
  },
  {
    path: '/markazApply',
    redirect: '/user/markaz/apply'
  },

{
    path: '/MarkazEdit/:id',
    redirect: '/user/markaz/edit/:id'
  },


  {
    path: '/markazChange',
    redirect: '/user/markaz/change'
  },
  {
    path: '/markaz/change/form',
    redirect: '/user/markaz/change/form'
  },
  {
    path: '/markazSetup',
    redirect: '/user/markaz/setup'
  },
  {
    path: '/confirmation',
    redirect: '/user/confirmation'
  },
  {
    path: '/marhalaChange',
    redirect: '/user/marhala/change'
  },
  {
    path: '/student/registration/overview',
    redirect: '/user/registration/overview'
  },
  {
    path: '/registration/list',
    redirect: '/user/registration/list'
  },
  {
    path: '/oldStudentList',
    redirect: '/user/student/old/list'
  },


  {
    path: '/student/old/verify/:marhala_id',
      redirect: (to: { params: { marhala_id: string } }) => `/user/student/old/verify/${to.params.marhala_id}`
  },



  {
    path: '/student/old/registration/form',
    redirect: '/user/student/old/registration/form'
  },
  {
    path: '/registraionCard',
    redirect: '/user/registration/card'
  },
  {
    path: '/registrationTable',
    redirect: '/user/registration/table'
  },
  {
    path: '/restore',
    redirect: '/user/restore'
  },
  {
    path: '/payment',
    redirect: '/user/payment'
  },
  {
    path: '/subject/list',
    redirect: '/user/subject/list'
  },

  // Other/Legacy routes (without specific layout) - to be removed or restructured
  /*
  // These routes are now moved to their respective layouts above
  */

  // Legacy single routes (will be deprecated)
  // Keep only those that might be accessed by both roles or need to be public
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/Errors/FourZeroFour.vue'),
    meta: { title: '404 Error', isPublic: true },
  },
]

// ---- Router ----
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { left: 0, top: 0 }
  },
  routes,
})

export default router

// ---- Navigation Guard ----
router.beforeEach(async (to, from, next) => {
  document.title = `${to.meta.title} | মাদরাসা পেনেল`

  // Use session/localStorage for userType (not JWT)
  const token = localStorage.getItem('token');
  const routeName = String(to.name || '');
  const routePath = to.path;
  let userType = localStorage.getItem('user_type');
  if (!userType && token) {
    // fallback: try to get from backend if needed
    try {
      const response = await axios.get('/auth/profile/', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.data?.user?.user_type) {
        userType = response.data.user.user_type;
        localStorage.setItem('user_type', userType ?? '');
      }
    } catch {
      userType = null;
    }
  }

  console.log(`🚀 Layout-based Route Guard: ${routeName} (${routePath}) - User: ${userType || 'anonymous'}`);

  // Special handling for Signup route - requires signup token
  if (routeName === 'Signup') {
    const signupToken = to.query.token as string;
    if (!signupToken) {
      console.log('❌ Signup access denied: No signup token provided');
      next({ name: 'MadrashaCheck' });
      return;
    }

    try {
      const response = await axios.get(`/auth/validate-signup-token/?token=${signupToken}`);
      if (response.data.valid) {
        console.log('✅ Valid signup token, allowing access to Signup');
        next();
        return;
      } else {
        console.log('❌ Invalid signup token, redirecting to MadrashaCheck');
        next({ name: 'MadrashaCheck' });
        return;
      }
    } catch (error: unknown) {
      console.log('❌ Error validating signup token, redirecting to MadrashaCheck', error);
      next({ name: 'MadrashaCheck' });
      return;
    }
  }

  // Layout-based role check
  if (to.meta.role && userType) {
    if (to.meta.role === 'admin' && !isAdminType(userType)) {
      console.log(`❌ Access denied: Non-admin user (${userType}) trying to access admin layout`);
      next({ name: 'Dashboard' });
      return;
    }
    if (to.meta.role === 'user' && isAdminType(userType)) {
      console.log(`❌ Access denied: Admin user trying to access user layout`);
      next({ name: 'AdminDashboard' });
      return;
    }
  }

  // Auth required and missing token
  if (requiresAuth(routeName) && !token) {
    console.log(`❌ Authentication required for ${routeName}, redirecting to signin`);
    next({ name: 'Signin' });
    return;
  }

  // Token exists - validate/role check
  if (token) {
    // Expired token
    if (isTokenExpired(token)) {
      console.log('❌ Token expired, clearing localStorage and redirecting to signin');
      await secureLogout();
      next({ name: 'Signin' });
      return;
    }

    // Enhanced role-based access control
    console.log(`👤 Current user type: ${userType}, accessing route: ${routeName}`);

    if (requiresAuth(routeName)) {
      // Block non-admin users from admin routes
      if (isNonAdminAccessingAdminRoute(routeName, userType || '')) {
        console.log(`❌ Access denied: Non-admin user (${userType}) trying to access admin route ${routeName}`);
        next({ name: 'Dashboard' });
        return;
      }
      // Block admin users from user-only routes
      if (isAdminAccessingUserRoute(routeName, userType || '')) {
        console.log(`❌ Access denied: Admin user trying to access user-only route ${routeName}`);
        next({ name: 'AdminDashboard' });
        return;
      }
      // Auto-redirect authenticated users accessing signin page
      if (routeName === 'Signin') {
        if (isAdminType(userType || '')) {
          console.log('✅ Auto-redirecting authenticated admin to AdminDashboard');
          next({ name: 'AdminDashboard' });
          return;
        } else if (userType === 'Madrasah' || userType === 'Madrasa') {
          console.log('✅ Auto-redirecting authenticated madrasa user to Dashboard');
          next({ name: 'Dashboard' });
          return;
        }
      }
    }
  }

  console.log(`✅ Access granted to ${routeName}`);
  next();
});
