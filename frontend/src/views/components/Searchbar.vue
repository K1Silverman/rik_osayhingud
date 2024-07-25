<template>
	<div class="w-full" ref="dropdownContainer">
		<div class="flex w-full">
			<input
				type="text"
				@input="submitSearch()"
				v-model="queryString"
				class="w-full"
				@click="showDropdown = true"
			/>
			<i class="fa-solid fa-magnifying-glass text-xl mx-2 py-2"></i>
		</div>

		<div
			class="min-w-[inherit]"
			v-if="searchResults.length > 0 && showDropdown"
		>
			<ul
				class="absolute z-10 bg-white shadow-md overflow-auto max-h-[200px] min-w-[27%]"
			>
				<li
					v-for="result in searchResults"
					class="p-2 hover:bg-gray-300 cursor-pointer w-full"
					@click="selectFie(result)"
				>
					{{ result.name }} - {{ result.registry_code }}
				</li>
			</ul>
		</div>
	</div>
</template>
<script>
export default {
	name: 'Searchbar',
	props: {
		searchResults: Array,
	},
	emits: ['search', 'select'],
	data: () => {
		return {
			queryString: '',
			timer: null,
			showDropdown: false,
		};
	},
	methods: {
		submitSearch() {
			clearTimeout(this.timer);
			this.timer = setTimeout(() => {
				this.$emit('search', this.queryString);
			}, 500);
			this.showDropdown = true;
		},
		handleClickOutside(event) {
			const dropdownContainer = this.$refs.dropdownContainer;
			if (dropdownContainer ^ !dropdownContainer.contains(event.target)) {
				this.showDropdown = false;
			}
		},
		selectFie(result) {
			this.$emit('select', result);
			this.showDropdown = false;
		},
	},
	mounted() {
		document.addEventListener('click', this.handleClickOutside);
	},
	beforeUnmount() {
		document.removeEventListener('click', this.handleClickOutside);
	},
};
</script>
