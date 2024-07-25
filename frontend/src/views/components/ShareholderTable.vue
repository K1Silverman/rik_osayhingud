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
			<tr v-for="(founder, index) in modifiedShareholders" :key="index">
				<!-- NIMI -->
				<td scope="row" v-if="founder.nic && !founder.isEdit">
					{{ founder.firstName }} {{ founder.lastName }}
				</td>
				<td scope="row" v-else-if="founder.nic && founder.isEdit" class="flex">
					<input
						class="mr-2"
						type="text"
						v-model="founder.firstName"
						placeholder="Eesnimi"
					/>
					<input
						type="text"
						v-model="founder.lastName"
						placeholder="Perekonnanimi"
					/>
				</td>
				<td scope="row" v-else-if="founder.registryCode">
					{{ founder.name }}
				</td>
				<!-- REG. KOOD/IK -->
				<td v-if="founder.nic && !founder.isEdit">
					{{ founder.nic }}
				</td>
				<td v-else-if="founder.nic && founder.isEdit">
					<input type="text" v-model="founder.nic" placeholder="Isikukood" />
				</td>
				<td v-else-if="founder.registryCode">
					{{ founder.registryCode }}
				</td>
				<td v-else-if="founder.registryCode && founder.isEdit">
					<input
						type="text"
						v-model="founder.registryCode"
						placeholder="Registrikood"
					/>
				</td>
				<!-- CAPACITY -->
				<td v-if="founder.isEdit || founder.capacity < 1">
					<input
						type="number"
						v-model="founder.capacity"
						placeholder="Osaniku osa suurus (€)"
					/>
				</td>
				<td v-else-if="!founder.isEdit">{{ founder.capacity }}</td>
				<td v-if="founder.isEdit || founder.capacity < 1" class="w-20">
					<i
						class="fa-solid fa-check hover:text-green-500 mx-2"
						@click="saveChanges(index)"
					></i>
					<i
						class="fa-solid fa-xmark hover:text-red-500"
						@click="discardChanges(index)"
					></i>
				</td>
				<td v-else-if="!founder.isEdit" class="w-20">
					<i
						class="fa-regular fa-pen-to-square cursor-pointer hover:text-blue-500 mx-2"
						@click="editRow(index)"
					></i>
					<i
						class="fa-regular fa-trash-can cursor-pointer hover:text-red-500"
						@click="removeFounder(index)"
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
		removeFounder(index) {
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
