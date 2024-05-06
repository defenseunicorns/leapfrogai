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
  <path d="M30,26.36h-4v-0.72h4V26.36z M22,26.36h-4v-0.72h4V26.36z M14,26.36h-4v-0.72h4V26.36z M6,26.36H2v-0.72h4	V26.36z M26,22.36h-4v-0.72h4V22.36z M18,22.36h-4v-0.72h4V22.36z M10,22.36H6v-0.72h4V22.36z M30,18.36h-4v-0.72h4V18.36z M22,18.36h-4v-0.72h4V18.36z M14,18.36h-4v-0.72h4V18.36z M6,18.36H2v-0.72h4V18.36z M26,14.36h-4v-0.72h4V14.36z M18,14.36h-4	v-0.72h4V14.36z M10,14.36H6v-0.72h4V14.36z M30,10.36h-4V9.64h4V10.36z M22,10.36h-4V9.64h4V10.36z M14,10.36h-4V9.64h4V10.36z M6,10.36H2V9.64h4V10.36z M26,6.36h-4V5.64h4V6.36z M18,6.36h-4V5.64h4V6.36z M10,6.36H6V5.64h4V6.36z"></path>
</svg>