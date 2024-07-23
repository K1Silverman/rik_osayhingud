<template>
	<div class="w-max">
		<p class="">Osaühingute otsing</p>
		<div class="bg-gray-800 flex">
			<input type="search" class="mx-auto bg-gray-200" />
		</div>
	</div>
</template>
<script>
import { formToJSON } from 'axios';

export default {
	name: 'HomeView',
	data: () => {
		return {
			query: '',
			results: [],
			timer: null,
		};
	},
	methods: {
		submitSearch() {},
	},
};
</script>
