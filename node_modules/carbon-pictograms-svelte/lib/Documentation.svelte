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
  <path d="M28,31.36H4c-0.199,0-0.36-0.161-0.36-0.36V1	c0-0.199,0.161-0.36,0.36-0.36h18c0.096,0,0.188,0.038,0.255,0.105l6,6C28.322,6.813,28.36,6.904,28.36,7v24	C28.36,31.199,28.199,31.36,28,31.36z M4.36,30.64h23.28V7.36H22c-0.199,0-0.36-0.161-0.36-0.36V1.36H4.36V30.64z M22.36,6.64h4.771	L22.36,1.869V6.64z M24,27.36H8v-0.72h16V27.36z M24,23.36H8v-0.72h16V23.36z M24,19.36H8v-0.72h16V19.36z M24,15.36H8v-0.72h16	V15.36z M24,11.36H8v-0.72h16V11.36z"></path>
</svg>