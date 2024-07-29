<template>
	<div class="mx-auto w-[30%]">
		<div v-for="field in formFields.base" class="mb-2">
			<label
				:for="field.key"
				class="block mb-2 text-sm font-medium text-gray-900"
				>{{ field.label }} <span class="text-red-500">*</span></label
			>
			<input
				v-if="field.type === 'number'"
				:type="field.type"
				:id="field.key"
				v-model="form[field.key]"
				:min="field.minValue"
				required
			/>
			<input
				v-else
				:type="field.type"
				:id="field.key"
				v-model="form[field.key]"
				required
			/>
		</div>
		<label class="block text-sm font-medium text-gray-900"
			>Asutaja(d) <span class="text-red-500">*</span></label
		>
	</div>
	<div class="mb-2 mx-auto" :class="fie ? 'w-[30%]' : 'w-[60%]'">
		<div class="w-full min-w-min">
			<ShareholderTable
				v-if="form.shareholder.length > 0"
				:shareholders="form.shareholder"
				:totalCapital="form.total_capital"
				:isFormEdit="true"
				:isAdd="true"
			/>
		</div>

		<div class="flex justify-start py-1 mx-auto w-min">
			<input type="checkbox" v-model="fie" class="mr-2" />
			<label class="block text-sm font-medium text-gray-900">FIE</label>
		</div>
		<Searchbar
			v-if="fie"
			@search="fetchSearchResults"
			@select="addJuridicalFounder"
			:searchResults="searchResults"
		/>

		<div v-if="!fie" class="flex w-[200%] relative">
			<div class="mr-2" v-for="field in formFields.founder">
				<label
					class="block text-sm font-medium text-gray-900"
					:for="field.key"
					>{{ field.label }}</label
				>
				<input
					:type="field.type"
					:id="field.key"
					v-model="physicalFounder[field.key]"
					:required="form.shareholder.length < 1"
				/>
			</div>
			<button
				class="mt-5 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium text-sm w-full sm:w-auto px-5 py-2.5 text-center"
				@click="addPhysicalFounder()"
			>
				Lisa
			</button>
		</div>
	</div>
	<div class="w-min mx-auto">
		<button
			class="mt-5 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium text-sm w-full sm:w-auto px-5 py-2.5 text-center"
			@click="submitForm()"
		>
			Salvesta
		</button>
	</div>
</template>
<script>
import ShareholderTable from '../views/components/ShareholderTable.vue';
import Searchbar from './components/Searchbar.vue';
export default {
	name: 'AddEnterpriseView',
	components: { ShareholderTable, Searchbar },
	emits: ['search'],
	data() {
		return {
			form: {
				name: '',
				registry_code: '',
				first_entry_date: '',
				total_capital: 2500,
				shareholder: [],
			},
			formFields: {
				base: {
					name: {
						label: 'Osaühingu nimi',
						type: 'text',
						key: 'name',
					},
					registry_code: {
						label: 'Registrikood',
						type: 'text',
						key: 'registry_code',
					},
					first_entry_date: {
						label: 'Asutamise kuupäev',
						type: 'date',
						key: 'first_entry_date',
					},
					total_capital: {
						label: 'Kogukapitali suurus (€)',
						type: 'number',
						key: 'total_capital',
						minValue: 2500,
					},
				},
				founder: {
					firstName: {
						label: 'Eesnimi',
						type: 'text',
						key: 'first_name',
					},
					lastName: {
						label: 'Perekonnanimi',
						type: 'text',
						key: 'last_name',
					},
					nic: {
						label: 'Isikukood',
						type: 'text',
						key: 'nic',
					},
					capacity: {
						label: 'Osaniku osa suurus (€)',
						type: 'number',
						key: 'capacity',
						minValue: 1,
					},
				},
			},
			fie: false,
			physicalFounder: {
				first_name: '',
				last_name: '',
				nic: '',
				capacity: 1,
				shareholderType: 'physical',
			},
			juridicalFounder: {
				name: '',
				registry_code: '',
				capacity: 0,
				shareholderType: 'fie',
			},
			searchMode: 'fie',
			searchResults: [],
		};
	},
	methods: {
		addPhysicalFounder() {
			this.form.shareholder.push(this.physicalFounder);
			this.physicalFounder = {
				first_name: '',
				last_name: '',
				nic: '',
				capacity: 1,
				shareholderType: 'physical',
			};
		},
		addJuridicalFounder(fie) {
			this.juridicalFounder.name = fie.name;
			this.juridicalFounder.registry_code = fie.registry_code;
			this.form.shareholder.push(this.juridicalFounder);
			this.juridicalFounder = {
				name: '',
				registry_code: '',
				capacity: 0,
			};
		},
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
		submitForm() {
			this.validateForm();
			this.$http
				.post('enterprise', this.form)
				.then((response) => {
					this.$router.push({
						path: `/enterprise/${response.data.id}`,
					});
				})
				.catch((error) => {
					console.log(error);
				});
		},
		validateForm() {
			let nameLengthValidation =
				this.form.name.length >= 3 && this.form.name.length <= 100;
			let registry_codeLengthValidation = this.form.registry_code.length == 7;
			let currentDate = new Date();
			let dateValidation = new Date(this.form.first_entry_date) <= currentDate;
			let total_capitalSizeValidation = this.form.total_capital >= 2500;
			// let foundersTotal_capitalValidation = this.foundersTotal_capital();
		},
	},
};
</script>
