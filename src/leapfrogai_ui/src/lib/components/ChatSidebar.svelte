<script lang="ts">
	import {
		Button,
		Modal,
		OverflowMenu,
		OverflowMenuItem,
		SideNav,
		SideNavDivider,
		SideNavLink,
		SideNavMenu,
		SideNavMenuItem,
		TextInput
	} from 'carbon-components-svelte';
	import { AddComment, Download, Export, Settings } from 'carbon-icons-svelte';
	import { dates } from '$helpers';
	import { MAX_LABEL_SIZE } from '$lib/constants';
	import { conversationsStore, toastStore } from '$stores';
	import { page } from '$app/stores';

	let deleteModalOpen = false;
	let editConversationId: string | null = null;
	let editLabelText: string | undefined = undefined;
	let inputDisabled = false;

	$: activeConversation = $conversationsStore.conversations.find(
		(conversation) => conversation.id === $page.params.conversation_id
	);

	$: organizedConversations = dates.organizeConversationsByDate($conversationsStore.conversations);

	$: dateCategories = Array.from(
		new Set([
			'Today',
			'Yesterday',
			'This Month',
			...dates.sortMonthsReverse(
				Object.keys(organizedConversations).filter((item) => item !== 'Old')
			),
			'Old'
		])
	);

	const resetEditMode = () => {
		editConversationId = null;
		editLabelText = undefined;
		inputDisabled = false;
	};

	const saveNewLabel = async () => {
		if (editConversationId && editLabelText) {
			inputDisabled = true;
			const response = await fetch('/api/conversations/update/label', {
				method: 'PUT',
				body: JSON.stringify({ id: editConversationId, label: editLabelText }),
				headers: {
					'Content-Type': 'application/json'
				}
			});

			if (response.ok) {
				conversationsStore.updateConversationLabel(editConversationId, editLabelText);
			} else {
				toastStore.addToast({
					kind: 'error',
					title: 'Error',
					subtitle: 'Error updating label'
				});
			}
			resetEditMode();
		}
	};

	const handleEdit = async (e: KeyboardEvent) => {
		if (e.key === 'Escape') {
			resetEditMode();
			return;
		}

		if (e.key === 'Enter' || e.key === 'Tab') {
			await saveNewLabel();
		}
	};

	const handleDelete = async () => {
		if (activeConversation?.id) {
			// A constraint on messages table will cascade delete all messages when the conversation is deleted
			const res = await fetch('/api/conversations/delete', {
				method: 'DELETE',
				body: JSON.stringify({ conversationId: activeConversation.id }),
				headers: {
					'Content-Type': 'application/json'
				}
			});
			if (res.ok) {
				conversationsStore.deleteConversation(activeConversation.id);
			} else {
				toastStore.addToast({
					kind: 'error',
					title: 'Error',
					subtitle: 'Error deleting conversation'
				});
			}
		}

		deleteModalOpen = false;
	};
</script>

<SideNav aria-label="side navigation" isOpen={true} style="background-color: g90;">
	<div class="new-chat-container">
		<Button
			kind="secondary"
			size="small"
			icon={AddComment}
			class="new-chat-btn"
			id="new-chat-btn"
			on:click={() => conversationsStore.changeConversation(null)}>New Chat</Button
		>
		<TextInput light size="sm" placeholder="Search..." />
		<SideNavDivider />
	</div>

	<div class="conversations" data-testid="conversations">
		{#each dateCategories as category}
			<SideNavMenu text={category} expanded data-testid="side-nav-menu">
				{#if organizedConversations[category]}
					{#each organizedConversations[category] as conversation (conversation.id)}
						{@const editMode = editConversationId && editConversationId === conversation.id}
						<div class:label-edit-mode={editMode}>
							<SideNavMenuItem
								data-testid="side-nav-menu-item-{conversation.label}"
								isSelected={activeConversation?.id === conversation.id}
								on:click={() => conversationsStore.changeConversation(conversation.id)}
							>
								<div class="menu-content">
									{#if editMode}
										<TextInput
											bind:value={editLabelText}
											size="sm"
											class="edit-conversation"
											on:keydown={(e) => handleEdit(e)}
											on:blur={async () => {
												await saveNewLabel();
												resetEditMode();
											}}
											autofocus
											maxlength={MAX_LABEL_SIZE}
											readonly={inputDisabled}
											aria-label="edit conversation"
										/>
									{:else}
										<div data-testid="conversation-label-{conversation.id}" class="menu-text">
											{conversation.label}
										</div>
										<OverflowMenu
											on:click={(e) => {
												e.stopPropagation();
												if (activeConversation?.id !== conversation.id) {
													conversationsStore.changeConversation(conversation.id);
												}
											}}
											data-testid="overflow-menu-{conversation.label}"
										>
											<OverflowMenuItem
												text="Edit"
												on:click={() => {
													editConversationId = conversation.id;
													editLabelText = conversation.label;
												}}
											/>
											<OverflowMenuItem
												text="Delete"
												on:click={() => (deleteModalOpen = true)}
												data-testid="overflow-menu-delete-{conversation.label}"
											/>
										</OverflowMenu>
									{/if}
								</div>
							</SideNavMenuItem>
						</div>
					{/each}
				{/if}
			</SideNavMenu>
		{/each}
	</div>
	<Modal
		danger
		bind:open={deleteModalOpen}
		modalHeading="Delete Chat"
		primaryButtonText="Delete"
		secondaryButtonText="Cancel"
		on:click:button--secondary={() => (deleteModalOpen = false)}
		on:open
		on:close
		on:submit={handleDelete}
		>Are you sure you want to delete your <strong
			>{activeConversation?.label.substring(0, MAX_LABEL_SIZE)}</strong
		> chat?</Modal
	>

	<div class="sidenav-links">
		<SideNavLink>Import Data<slot name="icon"><Download /></slot></SideNavLink>
		<SideNavLink>Export Data<slot name="icon"><Export /></slot></SideNavLink>
		<SideNavLink>System Settings<slot name="icon"><Settings /></slot></SideNavLink>
	</div>
</SideNav>

<!-- NOTE - Carbon Components Svelte does not yet support theming of the UI Shell components so several
properties had to be manually overridden.
https://github.com/carbon-design-system/carbon-components-svelte/issues/892
We might also want to investigate the Layer component once implemented in  Carbon Components Svelte V11.
-->
<style lang="scss">
	.new-chat-container {
		display: flex;
		flex-direction: column;
		gap: 8px;
		padding: 16px;
		:global(button.new-chat-btn) {
			width: 100%;
		}
		:global(.bx--side-nav__divider) {
			margin: 8px 0 0 0;
			background-color: themes.$border-subtle-01;
		}
	}
	.sidenav-links {
		display: flex;
		flex-direction: column;
		padding: 8px 0 8px 0;
		stroke: themes.$text-secondary;
		:global(.bx--side-nav__link-text) {
			color: themes.$text-secondary;
		}
	}
	.menu-content {
		width: 100% !important;
		position: relative;
		display: flex;
		align-items: center;
		justify-content: space-between;
		width: 208px;
		.menu-text {
			width: 192px;
			overflow: hidden;
			text-overflow: ellipsis;
			color: themes.$text-secondary;
		}

		:global(.bx--overflow-menu) {
			width: 16px;
			height: 32px;
		}
	}

	// The following overflow: visible !important overrides allow the OverflowMenu component
	// to display correctly. There may be a better way to do this, but just realize you have
	// to override things at several levels to get results.
	// The !important is necessary for the changes to work in production builds.
	.conversations {
		flex-grow: 1;
		overflow-y: scroll;
		scrollbar-width: none;
		border-bottom: 2px solid themes.$border-subtle-01;
		overflow: visible !important;
	}

	:global(.bx--side-nav__navigation) {
		overflow: visible !important;
		:global(.bx--side-nav__item) {
			overflow: visible !important;
		}
	}

	:global(.bx--side-nav__link) {
		&:hover {
			background-color: #4d4d4d !important;
		}
	}

	:global(.bx--side-nav__link[aria-current='page']) {
		background-color: #4d4d4d !important;
	}

	:global(.bx--side-nav__link-text) {
		position: relative;
		display: flex;
		flex-grow: 1;
		justify-content: space-between;
		overflow: visible !important;
		color: themes.$text-secondary !important;
	}

	:global(.bx--side-nav__navigation) {
		background-color: themes.$layer-01 !important;
		list-style: none;
		height: calc(100vh - var(--header-height)) !important;
		color: themes.$text-secondary !important;
	}

	:global(.bx--side-nav__submenu) {
		color: themes.$text-secondary !important;
		:global(svg) {
			stroke: themes.$text-secondary;
		}
		&:hover {
			background-color: #4d4d4d !important;
		}
	}

	.label-edit-mode {
		:global(.bx--side-nav__link) {
			padding: 0 layout.$spacing-04 0 layout.$spacing-07;
		}
		:global(.bx--side-nav__link[aria-current='page']) {
			background-color: themes.$layer-01 !important;
		}
		:global(input) {
			height: 1.5rem;
		}
		:global(.bx--text-input) {
			border-bottom: none;
		}
	}
</style>
