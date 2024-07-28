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
				<td scope="row" v-if="shareholder.nic && !shareholder.isEdit">
					{{ shareholder.first_name }} {{ shareholder.last_name }}
				</td>
				<td
					scope="row"
					v-else-if="shareholder.nic && shareholder.isEdit"
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
				</td>
				<!-- REG. KOOD/IK -->
				<td v-if="shareholder.nic && !shareholder.isEdit">
					{{ shareholder.nic }}
				</td>
				<td v-else-if="shareholder.nic && shareholder.isEdit">
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
				<td v-if="shareholder.isEdit || shareholder.capacity < 1">
					<input
						type="number"
						v-model="shareholder.capacity"
						placeholder="Osaniku osa suurus (€)"
					/>
				</td>
				<td v-else-if="!shareholder.isEdit">{{ shareholder.capacity }}</td>
				<td v-if="shareholder.isEdit || shareholder.capacity < 1" class="w-20">
					<i
						class="fa-solid fa-check hover:text-green-500 mx-2"
						@click="saveChanges(index)"
					></i>
					<i
						class="fa-solid fa-xmark hover:text-red-500"
						@click="discardChanges(index)"
					></i>
				</td>
				<td v-else-if="!shareholder.isEdit" class="w-20">
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
		<tfoot>
			<tr>
				<td class="text-right text-xs leading-3" colspan="2">
					Osanike osade suuruste summa peab võrduma kogukapitaliga
				</td>
				<td>
					<span :class="value === 0 ? '' : 'text-red-500'">{{
						shareholdersTotalCapital
					}}</span>
				</td>
			</tr>
		</tfoot>
	</table>
</template>
<script>
export default {
	name: 'ShareholderTable',
	props: {
		shareholders: Array,
		totalCapital: 0,
	},
	data() {
		return {};
	},
	methods: {
		removeShareholder(index) {
			this.shareholders.splice(index, 1);
		},
		editRow(index) {
			this.modifiedShareholders[index].isEdit = true;
			this.$forceUpdate();
		},
		saveChanges(index) {
			this.shareholders[index] = this.modifiedShareholders[index];
			this.modifiedShareholders[index].isEdit = false;
		},
		discardChanges(index) {
			console.log('discardChanges1: ', this.modifiedShareholders[index]);

			this.modifiedShareholders[index] = {
				...this.shareholders[index],
				isEdit: false,
			};
			console.log('discardChanges2: ', this.modifiedShareholders[index]);
			this.$forceUpdate();
		},
	},
	computed: {
		modifiedShareholders() {
			return this.shareholders.map((shareholder) => ({
				...shareholder,
				isEdit: false,
			}));
		},
		shareholdersTotalCapital() {
			let shareholdersCapitalTotal = 0;
			this.shareholders.forEach((shareholder) => {
				shareholdersCapitalTotal += shareholder.capacity;
			});
			return shareholdersCapitalTotal - this.totalCapital;
		},
	},
};
</script>
