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
	inject: ['eventBus'],
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
				capacity: 0,
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
				capacity: 0,
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
			let errorMessages = this.validateForm();
			if (errorMessages.length > 0) {
				this.eventBus.emit('show-alert', {
					alertType: 'danger',
					alertText: errorMessages.join(),
				});
			} else {
				this.$http
					.post('enterprise', this.form)
					.then((response) => {
						this.$router.push({
							path: `/enterprise/${response.data.id}`,
						});
						this.eventBus.emit('show-alert', {
							alertType: 'success',
							alertText: 'Osaühing on edukalt lisatud',
						});
					})
					.catch((error) => {
						let errorText = error.response.data.error;
						for (const [key, value] of Object.entries(
							error.response.data.serializer_errors
						)) {
							if (key == 'registry_code') {
								errorText += ' - ' + value;
							}
						}

						this.eventBus.emit('show-alert', {
							alertType: 'danger',
							alertText: errorText,
						});
					});
			}
		},
		validateForm() {
			let currentDate = new Date();
			let formValidation = [
				{
					errorText:
						'Osaühingu nimi peab olema 3 kuni 100 tähemärki pikk.<br/>',
					valid: this.form.name.length >= 3 && this.form.name.length <= 100,
				},
				{
					errorText:
						'Registrikood peab olema unikaalne ja 7 tähemärki pikk.<br/>',
					valid: this.form.registry_code.length == 7,
				},
				{
					errorText: 'Asutamise kuupäev ei tohi olla tulevikus.<br/>',
					valid: new Date(this.form.first_entry_date) <= currentDate,
				},
				{
					errorText: 'Kogukapitali suurus peab olema vähemalt 2500€.<br/>',
					valid: this.form.total_capital >= 2500,
				},
				{
					errorText: 'Osaühingul peab olema vähemalt üks asutaja.<br/>',
					valid: this.form.shareholder.length > 0,
				},
				{
					errorText:
						'Osanike osade summa ei võrdu kogukapitali suurusega.<br/>',
					valid: this.shareholdersTotalCapitalValidation,
				},
			];
			let errorMessages = [];
			formValidation.map((validation) => {
				if (!validation.valid) {
					errorMessages.push(validation.errorText);
				}
			});
			return errorMessages;
		},
	},
	computed: {
		shareholdersTotalCapitalValidation() {
			if (
				this.form.shareholder !== undefined &&
				this.form.shareholder.length > 0
			) {
				let shareholdersCapitalTotal = 0;
				this.form.shareholder.forEach((shareholder) => {
					shareholdersCapitalTotal += shareholder.capacity;
				});
				return shareholdersCapitalTotal == this.form.total_capital;
			}
		},
	},
};
</script>
