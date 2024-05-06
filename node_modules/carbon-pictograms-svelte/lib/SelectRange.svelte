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
  <path d="M21,27.36H11v-0.72h10V27.36z M28.36,26h-0.72v-3c0-0.199,0.161-0.36,0.36-0.36h3v0.721h-2.64V26z M26,23.36H4c-0.199,0-0.36-0.161-0.36-0.36V8c0-0.199,0.161-0.36,0.36-0.36h24c0.199,0,0.36,0.161,0.36,0.36v13h-0.72V8.36H4.36	v14.28H26V23.36z M21,18.36H11v-0.72h10V18.36z M21,13.36H11v-0.72h10V13.36z M21,4.36H11V3.64h10V4.36z"></path>
</svg>