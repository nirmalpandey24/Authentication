import { createRouter, createWebHashHistory } from 'vue-router';
import Login from '../components/Login.vue'; 
import UserForm from '../components/UserForm.vue';
import UserTable from '../components/UserTable.vue';
import Blog from '@/components/Blog.vue';
import Navbar from '@/components/Navbar.vue'


const routes = [
  {
    path: '/', 
    name: 'Login', 
    component: Login 
  },
  {
    path: '/user-form',
    name: 'Userform',
    component: UserForm
  },
  {
    path: '/user-table',
    name: 'userTable',
    component: UserTable,
    props: true 
  },
  {
    path:'/blog',
    name:'blog',
    component: Blog
  },
  {
    path:'/navbar',
    name:'navbar',
    component: Navbar
  },
 
];

const router = createRouter({
  history: createWebHashHistory(),
  routes
});

export default router;
