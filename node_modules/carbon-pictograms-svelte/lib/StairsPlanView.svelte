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
  <path d="M16.36,30h-0.72v-5.64H2c-0.199,0-0.36-0.161-0.36-0.36V4c0-0.199,0.161-0.36,0.36-0.36h13.64V2	h0.72v5.64H30c0.199,0,0.36,0.161,0.36,0.36v20c0,0.199-0.161,0.36-0.36,0.36H16.36V30z M16.36,27.64h13.28v-3.28H16.36V27.64z M16.36,23.64h13.28v-3.28H16.36V23.64z M2.36,23.64h13.28v-3.28H2.36V23.64z M16.36,19.64h13.28v-3.28H16.36V19.64z M2.36,19.64	h13.28v-3.28H2.36V19.64z M16.36,15.64h13.28v-3.28H16.36V15.64z M2.36,15.64h13.28v-3.28H2.36V15.64z M16.36,11.64h13.28V8.36	H16.36V11.64z M2.36,11.64h13.28V8.36H2.36V11.64z M2.36,7.64h13.28V4.36H2.36V7.64z"></path>
</svg>