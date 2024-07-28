<template>
	<div class="w-full">
		<div class="mx-auto w-[30%]">
			<h1 class="">Osaühingute otsing</h1>
			<Searchbar
				@search="fetchSearchResults"
				:searchResults="searchResults"
			></Searchbar>
		</div>
	</div>
</template>
<script>
import Searchbar from './components/Searchbar.vue';

export default {
	name: 'HomeView',
	components: { Searchbar },
	data: () => {
		return {
			query: '',
			searchResults: [],
			searchMode: 'enterprise',
		};
	},
	methods: {
		fetchSearchResults(query) {
			this.$http
				.get('search', {
					params: {
						queryString: query,
						searchMode: this.searchMode,
					},
				})
				.then((response) => {
					this.searchResults = response.data;
				});
		},
	},
};
</script>
