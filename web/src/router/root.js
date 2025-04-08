// 路由表
const constantRouterMap = [

  {
    path: '/',
    redirect: '/admin',
  },
  {
    path: '/adminLogin',
    name: 'adminLogin',
    component: () => import('/@/views/admin-login.vue'),
  },
  {
    path: '/admin',
    name: 'admin',
    redirect: '/admin/standard',
    component: () => import('/@/views/main.vue'),
    children: [
      { path: 'standard', name: 'standard', component: () => import('/@/views/standard.vue') },
      { path: 'user', name: 'user', component: () => import('/@/views/user.vue') },
      { path: 'zxsubmit', name: 'zxsubmit', component: () => import('/@/views/zxsubmit.vue') },
      { path: 'show2', name: 'show2', component: () => import('/src/views/show2.vue') },
      // n
      { path: 'loginLog', name: 'loginLog', component: () => import('/@/views/login-log.vue') },
      { path: 'opLog', name: 'opLog', component: () => import('/@/views/op-log.vue') },
      { path: 'errorLog', name: 'errorLog', component: () => import('/@/views/error-log.vue') },
      { path: 'sysInfo', name: 'sysInfo', component: () => import('/@/views/sys-info.vue') },
    ],
  },
];

export default constantRouterMap;
