<template>
	<div class="mx-auto w-[30%]">
		<div v-for="field in formFields.base" class="mb-2">
			<label
				:for="field.key"
				class="block mb-2 text-sm font-medium text-gray-900"
				>{{ field.label }}</label
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
		<div class="mb-2">
			<label class="block text-sm font-medium text-gray-900">Asutaja(d)</label>
			<div class="w-full min-w-min">
				<ShareholderTable
					v-if="form.founders.length > 0"
					:shareholders="form.founders"
					:totalCapital="form.totalCapital"
				/>
			</div>

			<div class="flex justify-start py-1">
				<input type="checkbox" v-model="fie" class="mr-2" />
				<label class="block text-sm font-medium text-gray-900">FIE</label>
			</div>

			<input
				v-if="fie"
				type="text"
				id=""
				:required="form.founders.length < 1"
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
						:required="form.founders.length < 1"
					/>
				</div>
				<button
					class="mt-5 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium text-sm w-full sm:w-auto px-5 py-2.5 text-center"
					@click="addFounder()"
				>
					Lisa
				</button>
			</div>
		</div>
		<button
			class="mt-5 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium text-sm w-full sm:w-auto px-5 py-2.5 text-center"
			@click="submitForm()"
		>
			Submit
		</button>
	</div>
</template>
<script>
import ShareholderTable from '../views/components/ShareholderTable.vue';

export default {
	name: 'AddEnterpriseView',
	components: { ShareholderTable },
	data() {
		return {
			form: {
				name: '',
				registryCode: '',
				dateOfFoundation: '',
				totalCapital: 2500,
				founders: [],
			},
			formFields: {
				base: {
					name: {
						label: 'Osaühingu nimi',
						type: 'text',
						key: 'name',
					},
					registryCode: {
						label: 'Registrikood',
						type: 'text',
						key: 'registryCode',
					},
					dateOfFoundation: {
						label: 'Asutamise kuupäev',
						type: 'date',
						key: 'dateOfFoundation',
					},
					totalCapital: {
						label: 'Kogukapitali suurus (€)',
						type: 'number',
						key: 'totalCapital',
						minValue: 2500,
					},
				},
				founder: {
					firstName: {
						label: 'Eesnimi',
						type: 'text',
						key: 'firstName',
					},
					lastName: {
						label: 'Perekonnanimi',
						type: 'text',
						key: 'lastName',
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
				firstName: '',
				lastName: '',
				nic: '',
				capacity: 1,
			},
			juridicalFounder: {
				name: '',
				registryCode: '',
				capacity: 1,
			},
			queryString: '',
		};
	},
	methods: {
		addFounder() {
			this.form.founders.push(this.physicalFounder);
			this.physicalFounder = {
				firstName: '',
				lastName: '',
				nic: '',
				capacity: 1,
			};
		},
		submitForm() {
			this.validateForm();
		},
		validateForm() {
			let nameLengthValidation =
				this.form.name.length >= 3 && this.form.name.length <= 100;
			let registryCodeLengthValidation = this.form.registryCode.length == 7;
			let currentDate = new Date();
			let dateValidation = new Date(this.form.dateOfFoundation) <= currentDate;
			let totalCapitalSizeValidation = this.form.totalCapital >= 2500;
			let foundersTotalCapitalValidation = this.foundersTotalCapital();
			console.log('nameLengthValidation: ' + nameLengthValidation);
			console.log(
				'registryCodeLengthValidation: ' + registryCodeLengthValidation
			);
			console.log('dateValidation: ' + dateValidation);
			console.log('totalCapitalSizeValidation: ' + totalCapitalSizeValidation);
			console.log(
				'foundersTotalCapitalValidation: ' + foundersTotalCapitalValidation
			);
		},
		foundersTotalCapital() {
			let foundersCapitalTotal = 0;
			this.form.founders.forEach((founder) => {
				foundersCapitalTotal += founder.capacity;
			});
			return this.form.totalCapital === foundersCapitalTotal;
		},
	},
};
</script>
