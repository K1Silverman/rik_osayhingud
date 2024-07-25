<template>
	<div class="w-max mx-auto mt-5">
		<RouterLink to="/" v-if="!isHomepage" class="menuButton"
			>Avalehele</RouterLink
		>
		<RouterLink to="/add" class="menuButton"
			>Osaühingu asutamise vorm</RouterLink
		>
	</div>
</template>
<script>
export default {
	name: 'Menu',
	props: {
		isHomepage: true,
	},
};
</script>
