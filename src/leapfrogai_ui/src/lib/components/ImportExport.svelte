<script lang="ts">
	import { Download, Export } from 'carbon-icons-svelte';
	import { Button } from 'carbon-components-svelte';
	import LFFileUploader from '$components/LFFileUploader.svelte';
	import { conversationsStore, toastStore } from '$stores';
	import { conversationsSchema } from '../../schemas/chat';

	const readFileAsJson = (file: File): Promise<any> => {
		return new Promise((resolve, reject) => {
			const reader = new FileReader();

			reader.onload = (event: ProgressEvent<FileReader>) => {
				if (event.target && typeof event.target.result === 'string') {
					try {
						const jsonObject = JSON.parse(event.target.result);
						resolve(jsonObject);
					} catch (error) {
						reject(error);
					}
				}
			};
			reader.onerror = (error) => {
				reject(error);
			};
			reader.readAsText(file);
		});
	};

	const onUpload = async (files: FileList) => {
		let conversations: Conversation[] = [];
		try {
			conversations = await readFileAsJson(files[0]);
			await conversationsSchema.validate(conversations);
		} catch {
			toastStore.addToast({
				kind: 'error',
				title: 'Error',
				subtitle: `Conversations are incorrectly formatted.`
			});
			return;
		}
		await conversationsStore.importConversations(conversations);
	};

	const onExport = () => {
		try {
			const dataStr =
				'data:text/json; charset=utf-8,' +
				encodeURIComponent(JSON.stringify($conversationsStore.conversations));
			const downloadAnchorNode = document.createElement('a');

			downloadAnchorNode.setAttribute('href', dataStr);
			downloadAnchorNode.setAttribute('download', 'conversations.json');
			document.body.appendChild(downloadAnchorNode);
			downloadAnchorNode.click();
			downloadAnchorNode.remove();
		} catch {
			toastStore.addToast({
				kind: 'error',
				title: 'Error',
				subtitle: `Error exporting conversations.`
			});
		}
	};
</script>

<!--TODO - can we change system upload modal button to say import?-->
<div class="import-export-btns-container">
	<LFFileUploader
		accept={['application/json']}
		icon={Download}
		labelText="Import data"
		{onUpload}
	/>
	<Button
		id="export-btn"
		kind="ghost"
		icon={Export}
		iconDescription="Export conversations"
		on:click={onExport}>Export data</Button
	>
</div>

<style lang="scss">
	.import-export-btns-container {
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		:global(.bx--btn) {
			width: 100%;
			color: themes.$text-secondary;
			font-weight: bold;
		}
	}
</style>
