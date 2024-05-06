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
  <path d="M30.745,31.255l-9.385-9.386V30h-0.72v-9.36H30v0.721h-8.131l9.386,9.385L30.745,31.255z M1.254,31.255 l-0.509-0.51l9.385-9.385H2v-0.72h9.36V30h-0.72v-8.131L1.254,31.255z M30,11.36h-9.36V2h0.721v8.131l9.385-9.385l0.51,0.509 l-9.386,9.386H30V11.36z M11.36,11.36H2v-0.72h8.131L0.746,1.254l0.509-0.509l9.386,9.385V2h0.72v9.36H11.36z"></path>
</svg>