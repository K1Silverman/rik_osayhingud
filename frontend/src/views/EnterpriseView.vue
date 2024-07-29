<template>
	<div class="w-full">
		<div
			v-if="enterprise.id !== undefined"
			class="w-[70%] mx-auto text-center mb-5"
			v-for="field in enterpriseUI"
		>
			<h2 class="text-xl text-blue-700">{{ field.label }}</h2>
			<span v-if="field.key === 'total_capital'">{{ realTotalCapital }} €</span>
			<span v-else-if="field.key === 'first_entry_date'">{{
				formatDate(enterprise[field.key])
			}}</span>
			<span v-else>{{ enterprise[field.key] }}</span>
		</div>
		<div class="w-[50%] mx-auto">
			<ShareholderTable
				:shareholders="enterprise.shareholder"
				:totalCapital="enterprise.total_capital"
				:isFormEdit="isEdit"
			/>
		</div>
		<div v-if="isEdit" class="w-[50%] mx-auto">
			<div class="flex justify-start py-1">
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
				<div class="mr-2" v-for="field in physicalFounderFormUI">
					<label
						class="block text-sm font-medium text-gray-900"
						:for="field.key"
						>{{ field.label }}</label
					>
					<input
						:type="field.type"
						:id="field.key"
						v-model="physicalFounder[field.key]"
						:required="enterprise.shareholder.length < 1"
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
		<div v-if="!isEdit" class="w-min mx-auto">
			<button
				class="mt-5 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium text-sm w-full sm:w-auto px-5 py-2.5 text-center"
				@click="toggleEdit()"
			>
				Muuda
			</button>
		</div>
		<div v-if="isEdit" class="w-min mx-auto flex">
			<button
				class="mt-5 mr-2 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium text-sm w-full sm:w-auto px-5 py-2.5 text-center"
				@click="saveEnterprise(), emptyFields()"
			>
				Salvesta
			</button>
			<button
				class="mt-5 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium text-sm w-full sm:w-auto px-5 py-2.5 text-center"
				@click="toggleEdit()"
			>
				Tühista
			</button>
		</div>
	</div>
</template>
<script>
import ShareholderTable from './components/ShareholderTable.vue';
import Searchbar from './components/Searchbar.vue';
import { toRaw } from 'vue';
import { format, parseISO } from 'date-fns';

export default {
	name: 'EnterpriseView',
	components: { ShareholderTable, Searchbar },
	data: () => {
		return {
			enterpriseUI: [
				{
					label: 'Nimi',
					key: 'name',
				},
				{
					label: 'Registrikood',
					key: 'registry_code',
				},
				{
					label: 'Asutamise kuupäev',
					key: 'first_entry_date',
				},
				{
					label: 'Kogukapital',
					key: 'total_capital',
				},
			],
			physicalFounderFormUI: {
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
			enterprise: {},
			searchResults: [],
			searchMode: 'fie',
			isEdit: false,
		};
	},
	methods: {
		formatDate(date) {
			const rawDateTime = toRaw(date);
			if (typeof rawDateTime === 'string') {
				const date = parseISO(rawDateTime);
				const dateFormat = 'dd/MM/yyyy';

				if (!isNaN(date.getTime())) {
					return format(date, dateFormat);
				}
			}
			return 'Invalid Date';
		},
		toggleEdit() {
			this.isEdit = !this.isEdit;
		},
		addPhysicalFounder() {
			this.enterprise.shareholder.push(this.physicalFounder);
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
			this.enterprise.shareholder.push(this.juridicalFounder);
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
		saveEnterprise() {
			this.$http
				.patch('enterprise/' + this.enterprise.id, this.enterprise)
				.then((response) => {
					console.log(response.data);
					this.isEdit = false;
				})
				.catch((error) => {
					console.log(error);
				});
		},
		emptyFields() {
			this.physicalFounder = {
				first_name: '',
				last_name: '',
				nic: '',
				capacity: 1,
				shareholderType: 'physical',
			};
			this.juridicalFounder = {
				name: '',
				registry_code: '',
				capacity: 0,
			};
			this.physicalFounder = {
				first_name: '',
				last_name: '',
				nic: '',
				capacity: 0,
			};
			this.searchResults = [];
		},
	},
	created() {
		this.$http.get('enterprise/' + this.$route.params.id).then((response) => {
			this.enterprise = response.data;
		});
	},
	computed: {
		realTotalCapital() {
			let totalCapital = 0;
			this.enterprise.shareholder.forEach((shareholder) => {
				totalCapital += shareholder.capacity;
			});
			return totalCapital;
		},
	},
};
</script>
