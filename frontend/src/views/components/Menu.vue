<template>
	<div class="w-max mx-auto mt-5">
		<RouterLink to="/" class="menuButton">Avalehele</RouterLink>
		<RouterLink
			to="/add"
			v-if="currentUrl === '/' || currentUrl.startsWith('/enterprise/')"
			class="menuButton"
			>Osaühingu asutamise vorm</RouterLink
		>
	</div>
</template>
<script>
export default {
	name: 'Menu',
	computed: {
		currentUrl: function () {
			return this.$route.path;
		},
	},
};
</script>
