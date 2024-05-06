<script>
  /**
   * Specify the pictogram title.
   * @type {string}
   */
  export let title = undefined;

  $: labelled =  $$props["aria-label"] || $$props["aria-labelledby"] || $$props["title"];
  $: attributes = {
    "aria-hidden": labelled ? undefined : true,
    role: labelled ? "img" : undefined,
    focusable: Number($$props["tabindex"]) === 0  ? true : undefined,
  };
</script>

<svg
  preserveAspectRatio="xMidYMid meet"
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 32 32"
  width="64"
  height="64"
  fill="currentColor"
  {title}
  {...attributes}
  {...$$restProps}>
  <path d="M16,0.59L4.64,6.786V20c0,6.158,5.202,11.36,11.36,11.36S27.36,26.158,27.36,20V6.786L16,0.59z M25.84,23.957L16,18.592v0.821l9.536,5.198c-0.699,1.407-1.694,2.651-2.909,3.636L16,24.635v0.821l5.995,3.268	c-1.721,1.2-3.791,1.916-5.995,1.916c-5.768,0-10.64-4.872-10.64-10.64V7.214L16,1.41l10.64,5.804v5.18L16,6.592v0.82l10.64,5.801	v5.137L16,12.549v0.82l10.64,5.802V20C26.64,21.39,26.351,22.726,25.84,23.957z"></path>
</svg>