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
  <path d="M31.36,9h-0.72V1.36H1.36V9H0.64V1c0-0.199,0.161-0.36,0.36-0.36h30c0.199,0,0.36,0.161,0.36,0.36V9z"></path><path d="M16.36 31L15.64 31 15.64 9.869 10.254 15.254 9.746 14.746 16 8.491 22.255 14.746 21.745 15.254 16.36 9.869z"></path>
</svg>