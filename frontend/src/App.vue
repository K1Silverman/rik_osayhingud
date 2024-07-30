<template>
	<Menu></Menu>
	<div class="min-w-full relative mt-10">
		<AlertBox
			:variant="alert.alertType"
			:text="alert.alertText"
			:show="alert.show"
			:closeAlertBox="closeAlertBox"
		></AlertBox>
		<RouterView></RouterView>
	</div>
</template>
<script>
import Menu from './views/components/Menu.vue';
import AlertBox from './views/components/Alertbox.vue';

export default {
	name: 'App',
	components: { Menu, AlertBox },
	inject: ['eventBus'],
	data() {
		return {
			alert: {
				show: false,
				alertText: 'Error',
				alertType: 'danger',
				timeout: 10000,
			},
		};
	},
	methods: {
		closeAlertBox() {
			this.alert.show = false;
		},
	},
	created() {
		this.eventBus.on('show-alert', (evt) => {
			this.alert = evt;
			this.alert.show = true;

			if (!this.alert.timeout) {
				this.alert.timeout = 5000;
			}

			if (this.alert.timeout != -1) {
				setTimeout(() => {
					this.alert.show = false;
				}, this.alert.timeout);
			}
		});
	},
};
</script>
