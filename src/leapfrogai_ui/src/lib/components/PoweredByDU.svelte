<script>
	import doug from '$assets/Doug.png';
	import DefenseUnicorns from '$assets/DefenseUnicorns.png';
</script>

<div class="flex">
	<img alt="Doug" src={doug} class="icon" />
	<span class="legal">Powered By</span>
	<img alt="Defense Unicorns" src={DefenseUnicorns} class="wordmark" />
</div>

<style lang="scss">
	.flex {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: layout.$spacing-02;
	}
	.legal {
		@include type.type-style('legal-01');
	}
	.icon {
		height: 24px;
	}
	.wordmark {
		width: 6.75rem;
	}
</style>
