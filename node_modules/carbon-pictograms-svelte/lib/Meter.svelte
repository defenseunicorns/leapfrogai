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
  <path d="M16,31.36C7.53,31.36,0.64,24.47,0.64,16S7.53,0.64,16,0.64S31.36,7.53,31.36,16S24.47,31.36,16,31.36z M16,1.36C7.927,1.36,1.36,7.927,1.36,16c0,8.072,6.567,14.64,14.64,14.64c8.072,0,14.64-6.567,14.64-14.64S24.072,1.36,16,1.36z M4.922,22.812l-0.36-0.623l0.866-0.5l0.36,0.623L4.922,22.812z M27.079,22.812l-3.899-2.251l0.359-0.623l3.899,2.251L27.079,22.812	z M29,16.36h-4v-0.72h4V16.36z M4.5,16.36H3v-0.72h1.5V16.36z M16.18,16.312l-0.36-0.624l11.259-6.5l0.359,0.624L16.18,16.312z M6.32,10.827L4.562,9.812l0.36-0.624l1.758,1.016L6.32,10.827z M20.931,8.18l-0.623-0.36l1.881-3.258l0.623,0.36L20.931,8.18z M10.492,7.18L9.188,4.922l0.624-0.36l1.304,2.258L10.492,7.18z M16.36,6h-0.72V3h0.72V6z"></path>
</svg>