<script lang="ts">
	import { ToastNotification } from 'carbon-components-svelte';
	import { slide } from 'svelte/transition';
	import { toastStore } from '$stores';
</script>

{#if $toastStore.toasts}
	<section>
		{#each $toastStore.toasts as toast (toast.id)}
			<div transition:slide>
				<ToastNotification
					timeout={toast.timeout}
					kind={toast.kind}
					title={toast.title}
					subtitle={toast.subtitle}
					caption={new Date().toLocaleString()}
					on:click={() => toastStore.dismissToast(toast.id)}
				/>
			</div>
		{/each}
	</section>
{/if}

<style lang="scss">
	section {
		position: absolute;
		top: 0 + var(--header-height);
		right: 0;
		display: flex;
		justify-content: center;
		flex-direction: column;
		z-index: 100000;
	}
</style>
