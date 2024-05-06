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
  <path d="M31,20.36h-8v-0.72h7.64V1.36H1.36v18.28H9v0.721H1c-0.199,0-0.36-0.161-0.36-0.36V1c0-0.199,0.161-0.36,0.36-0.36h30 c0.199,0,0.36,0.161,0.36,0.36v19C31.36,20.199,31.199,20.36,31,20.36z"></path><path d="M16.36 31L15.64 31 15.64 7.869 10.254 13.254 9.746 12.746 16 6.491 22.255 12.746 21.745 13.254 16.36 7.869z"></path>
</svg>