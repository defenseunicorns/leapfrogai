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
  <path d="M31,31.36H1c-0.199,0-0.36-0.161-0.36-0.36V1h0.72v9.264l8.419-6.548	c0.127-0.097,0.303-0.101,0.433-0.007l10.808,7.86l9.795-5.877c0.112-0.067,0.249-0.068,0.363-0.005C31.29,5.75,31.36,5.87,31.36,6	v14c0,0.126-0.066,0.243-0.175,0.309l-10,6c-0.124,0.074-0.279,0.067-0.397-0.018L10.007,18.45L1.36,25.176v5.464H31V31.36z M10,17.64c0.074,0,0.148,0.023,0.212,0.069l10.808,7.859l9.62-5.772v-6.16l-9.454,5.673c-0.124,0.075-0.279,0.068-0.397-0.018	L10.007,11.45L1.36,18.176v6.088l8.419-6.548C9.844,17.665,9.922,17.64,10,17.64z M10,10.64c0.074,0,0.148,0.023,0.212,0.069	l10.808,7.859l9.62-5.772v-6.16l-9.454,5.673c-0.124,0.075-0.279,0.068-0.397-0.018L10.007,4.45L1.36,11.176v6.087l8.419-6.548	C9.844,10.666,9.922,10.64,10,10.64z"></path>
</svg>