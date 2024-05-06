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
  <path d="M26,31.36H7c-0.199,0-0.36-0.161-0.36-0.36V1c0-0.199,0.161-0.36,0.36-0.36h19	c0.199,0,0.36,0.161,0.36,0.36v30C26.36,31.199,26.199,31.36,26,31.36z M7.36,30.64h18.28V1.36H7.36V30.64z M23,26.36h-2v-0.72h2	V26.36z M23,22.36H10v-0.72h13V22.36z M23,18.36h-2v-0.72h2V18.36z M17,18.36h-7v-0.72h7V18.36z M23,14.36h-2v-0.72h2V14.36z M17,14.36h-7v-0.72h7V14.36z M23,10.36h-2V9.64h2V10.36z M17,10.36h-7V9.64h7V10.36z M23,6.36h-2V5.64h2V6.36z M17,6.36h-7V5.64h7	V6.36z"></path>
</svg>