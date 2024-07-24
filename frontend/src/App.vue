<template>
	<Menu></Menu>
	<div class="w-full mx-auto mt-10">
		<RouterView></RouterView>
	</div>
</template>
<script>
import Menu from './views/components/Menu.vue';

export default {
	name: 'App',
	components: { Menu },
	data() {
		return {};
	},
};
</script>
