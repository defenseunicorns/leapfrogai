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
  <path d="M17.5,30.36h-4v-0.72h4V30.36z M23.5,26.36h-8v-0.72h8V26.36z M25.5,22.36h-12v-0.72h12V22.36z M21.5,18.36	h-12v-0.72h12V18.36z M28.5,14.36h-17v-0.72h17V14.36z M25.5,10.36h-17V9.64h17V10.36z M23.5,6.36h-20V5.64h20V6.36z M26.5,2.36h-20	V1.64h20V2.36z"></path>
</svg>