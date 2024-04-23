<!--This is a custom version of Carbon Components Svelte's FileUploaderButton to support usage of an inline icon-->

<script lang="ts">
	/** Obtain a reference to the input HTML element */
	export let ref: HTMLInputElement | null = null;
	export let icon: any;
	export let labelText = 'Add File';
	export let accept: string[] = [];
	export let onUpload: (files: FileList) => void;

	let files: FileList;

	$: if (files) {
		onUpload(files);
	}
</script>

<div>
	<label
		id="import-conversations-label"
		for="import-conversations"
		tabindex="0"
		class:bx--btn={true}
		class:bx--btn--ghost={true}
		on:keydown
		on:keydown={({ key }) => {
			if (key === ' ' || key === 'Enter') {
				ref?.click();
			}
		}}
		><span role="button"><slot name="labelText">{labelText}</slot></span>
		<svelte:component this={icon} />
	</label>

	<input
		id="import-conversations"
		bind:this={ref}
		type="file"
		tabindex="-1"
		accept={accept.join(',')}
		multiple={false}
		name="import"
		bind:files
		class:bx--visually-hidden={true}
	/>
</div>
