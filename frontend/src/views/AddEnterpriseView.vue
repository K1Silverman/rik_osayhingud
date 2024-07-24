<template>
	<div class="max-w-sm mx-auto w-[200%]">
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
				class="bg-gray-50 border border-gray-300 text-gray-900 text-sm focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
				required
			/>
			<input
				v-else
				:type="field.type"
				:id="field.key"
				v-model="form[field.key]"
				class="bg-gray-50 border border-gray-300 text-gray-900 text-sm focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
				required
			/>
		</div>
		<div class="mb-2 flex-auto">
			<label class="block text-sm font-medium text-gray-900">Asutaja(d)</label>
			<table
				v-if="this.form.founders.length > 0"
				class="w-[200%] left-[-50%] relative border-collapse"
			>
				<thead>
					<tr>
						<th scope="col">Nimi</th>
						<th scope="col">Reg. kood/IK</th>
						<th scope="col">Osaniku osa suurus (€)</th>
						<th scope="col">Osaniku osa suurus (%)</th>
					</tr>
				</thead>
				<tbody class="">
					<tr v-for="(founder, index) in form.founders">
						<td scope="row" v-if="founder.nic">
							{{ founder.firstName }} {{ founder.lastName }}
						</td>
						<td scope="row" v-else-if="founder.registryCode">
							{{ founder.name }}
						</td>
						<td v-if="founder.nic">
							{{ founder.nic }}
						</td>
						<td v-else-if="registryCode">{{ founder.registryCode }}</td>
						<td>{{ founder.capacity }} €</td>
						<td
							v-if="
								(founder.capacity / form.totalCapital) * 100 > 0 &&
								(founder.capacity / form.totalCapital) * 100 < 100
							"
						>
							{{ ((founder.capacity / form.totalCapital) * 100).toFixed(2) }} %
						</td>
						<td>
							<i
								class="fa-regular fa-trash-can cursor-pointer"
								@click="removeFounder(index)"
							></i>
						</td>
					</tr>
				</tbody>
			</table>
			<div class="flex py-1">
				<input type="checkbox" v-model="fie" class="mr-2" />
				<label class="block text-sm font-medium text-gray-900">FIE</label>
			</div>

			<input
				v-if="fie"
				type="text"
				id=""
				class="bg-gray-50 border border-gray-300 text-gray-900 text-sm focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
				:required="form.founders.length < 1"
			/>
			<div v-if="!fie" class="flex w-[200%] left-[-50%] relative">
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
						class="bg-gray-50 border border-gray-300 text-gray-900 text-sm focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
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
export default {
	name: 'AddEnterpriseView',
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
						type: 'input',
						key: 'name',
					},
					registryCode: {
						label: 'Registrikood',
						type: 'input',
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
		removeFounder(index) {
			this.form.founders.splice(index, 1);
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
