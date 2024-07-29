import { createRouter, createWebHistory } from "vue-router"
import HomeView from "./views/HomeView.vue"
import EnterpriseView from "./views/EnterpriseView.vue"
import AddEnterpriseView from "./views/AddEnterpriseView.vue"

const routes = [
	{
		path: '/',
		name: 'homePageRoute',
		component: HomeView
	},
	{
		path: '/enterprise/:id',
		name: 'enterprisePageRoute',
		component: EnterpriseView,
	},
	{
		name: 'addEnterprisePageRoute',
		path: '/add',
		component: AddEnterpriseView
	}
]

export default createRouter({
	history: createWebHistory(),
  routes
});