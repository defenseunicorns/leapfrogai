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
  <path d="M16.36,31h-0.72V16.36H1v-0.72h14.64V8.109	l-0.971-1.456C12.877,3.965,9.878,2.36,6.648,2.36H1V1.64h5.648c3.472,0,6.694,1.725,8.62,4.613l0.372,0.558V1h0.72v6.891	l0.971,1.456c1.791,2.688,4.79,4.293,8.021,4.293H31v0.72h-5.648c-3.472,0-6.694-1.725-8.62-4.613L16.36,9.189v6.451H31v0.72H16.36	V31z"></path>
</svg>