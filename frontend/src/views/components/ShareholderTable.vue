<template>
	<table class="w-full">
		<thead>
			<tr>
				<th scope="col">Nimi</th>
				<th scope="col">Reg. kood/IK</th>
				<th scope="col">Osaniku osa suurus (€)</th>
				<th scope="col"></th>
			</tr>
		</thead>
		<tbody class="">
			<tr v-for="(shareholder, index) in modifiedShareholders" :key="index">
				<!-- NIMI -->
				<td
					scope="row"
					v-if="
						(shareholder.nic && !shareholder.isEdit) ||
						(shareholder.founder && !shareholder.registry_code)
					"
				>
					{{ shareholder.first_name }} {{ shareholder.last_name }}
					<span v-if="shareholder.founder" class="italic">(Asutaja)</span>
				</td>
				<td
					scope="row"
					v-else-if="
						shareholder.nic && !shareholder.founder && shareholder.isEdit
					"
					class="flex"
				>
					<input
						class="mr-2"
						type="text"
						v-model="shareholder.first_name"
						placeholder="Eesnimi"
					/>
					<input
						type="text"
						v-model="shareholder.last_name"
						placeholder="Perekonnanimi"
					/>
				</td>
				<td scope="row" v-else-if="shareholder.registry_code">
					{{ shareholder.name }}
					<span v-if="shareholder.founder" class="italic">(Asutaja)</span>
				</td>
				<!-- REG. KOOD/IK -->
				<td
					v-if="
						(shareholder.nic && !shareholder.isEdit) ||
						(shareholder.founder && !shareholder.registry_code)
					"
				>
					{{ shareholder.nic }}
				</td>
				<td
					v-else-if="
						shareholder.nic && !shareholder.founder && shareholder.isEdit
					"
				>
					<input
						type="text"
						v-model="shareholder.nic"
						placeholder="Isikukood"
					/>
				</td>
				<td v-else-if="shareholder.registry_code">
					{{ shareholder.registry_code }}
				</td>
				<td v-else-if="shareholder.registry_code && shareholder.isEdit">
					<input
						type="text"
						v-model="shareholder.registry_code"
						placeholder="Registrikood"
					/>
				</td>
				<!-- CAPACITY -->
				<td
					v-if="shareholder.isEdit || shareholder.capacity < 1"
					class="w-[20%]"
				>
					<input
						type="number"
						v-model="shareholder.capacity"
						placeholder="Osaniku osa suurus (€)"
					/>
				</td>
				<td v-else-if="!shareholder.isEdit" class="w-[20%]">
					{{ shareholder.capacity }}
				</td>
				<td
					v-if="(isFormEdit && shareholder.isEdit) || shareholder.capacity < 1"
					class="w-20"
				>
					<i
						class="fa-solid fa-check hover:text-green-500 mx-2"
						@click="saveChanges(index)"
					></i>
					<i
						class="fa-solid fa-xmark hover:text-red-500"
						@click="discardChanges(index)"
					></i>
				</td>
				<td v-else-if="isFormEdit && !shareholder.isEdit" class="w-20">
					<i
						class="fa-regular fa-pen-to-square cursor-pointer hover:text-blue-500 mx-2"
						@click="editRow(index)"
					></i>
					<i
						class="fa-regular fa-trash-can cursor-pointer hover:text-red-500"
						@click="removeShareholder(index)"
					></i>
				</td>
			</tr>
		</tbody>
		<tfoot v-if="isAdd">
			<tr>
				<td class="text-right text-xs leading-3" colspan="2">
					Osanike osade suuruste summa peab võrduma kogukapitaliga
				</td>
				<td>
					<span
						:class="
							value === undefined || value === 0
								? 'text-green-500'
								: 'text-red-500'
						"
						>{{ shareholdersTotalCapital }}</span
					>
				</td>
			</tr>
		</tfoot>
	</table>
</template>
<script>
export default {
	name: 'ShareholderTable',
	inject: ['eventBus'],
	props: {
		shareholders: Array,
		totalCapital: 0,
		isFormEdit: false,
		isAdd: false,
	},
	data() {
		return {
			editingRows: [],
		};
	},
	methods: {
		removeShareholder(index) {
			this.shareholders.splice(index, 1);
		},
		editRow(index) {
			this.editingRows[index] = true;
			this.$forceUpdate();
		},
		saveChanges(index) {
			let validation = this.validateChanges(index);
			if (validation.length > 0) {
				this.eventBus.emit('show-alert', {
					alertType: 'danger',
					alertText: validation,
				});
			} else {
				this.shareholders[index] = this.modifiedShareholders[index];
				this.editingRows[index] = !this.editingRows[index];
			}
		},
		discardChanges(index) {
			this.editingRows[index] = false;
			this.$forceUpdate();
		},
		validateChanges(index) {
			let errorTexts = [];
			if ('nic' in this.modifiedShareholders[index]) {
				errorTexts = this.validatePhysicalShareholder(
					this.modifiedShareholders[index]
				).join('');
			}
			if (
				typeof this.modifiedShareholders[index].capacity == String ||
				this.modifiedShareholders[index].capacity < 1
			) {
				errorTexts = errorTexts.concat(
					'Osaniku osa suurus peab olema suurem kui 1.<br />'
				);
			}
			return errorTexts;
		},
		validatePhysicalShareholder(shareholder) {
			let fieldsValidation = [
				{
					errorText: 'Eesnimi on kohustuslik. Pikkus: 2-100 tähemärki.<br />',
					valid:
						shareholder.first_name.length >= 2 &&
						shareholder.first_name.length <= 100,
				},
				{
					errorText:
						'Perekonnanimi on kohustuslik. Pikkus: 2-100 tähemärki.<br />',
					valid:
						shareholder.last_name.length >= 2 &&
						shareholder.last_name.length <= 100,
				},
				{
					errorText: 'Isikukood on kohustuslik. Pikkus: 7-12 tähemärki.<br />',
					valid: shareholder.nic.length >= 7 && shareholder.nic.length <= 12,
				},
			];

			let errorTexts = [];

			fieldsValidation.map((field) => {
				if (!field.valid) {
					errorTexts.push(field.errorText);
				}
			});
			return errorTexts;
		},
	},
	computed: {
		modifiedShareholders() {
			if (this.shareholders !== undefined && this.shareholders.length > 0) {
				return this.shareholders.map((shareholder, index) => ({
					...shareholder,
					isEdit: this.editingRows[index] || false,
				}));
			}
		},
		shareholdersTotalCapital() {
			if (this.shareholders !== undefined && this.shareholders.length > 0) {
				let shareholdersCapitalTotal = 0;
				this.shareholders.forEach((shareholder) => {
					shareholdersCapitalTotal += shareholder.capacity;
				});
				return shareholdersCapitalTotal - this.totalCapital;
			}
		},
	},
};
</script>
