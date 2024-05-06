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
  <path d="M31,0.64H10C9.801,0.64,9.64,0.801,9.64,1v2.64H1	C0.801,3.64,0.64,3.801,0.64,4v27c0,0.199,0.161,0.36,0.36,0.36h21c0.199,0,0.36-0.161,0.36-0.36v-2.64H31	c0.199,0,0.36-0.161,0.36-0.36V1C31.36,0.801,31.199,0.64,31,0.64z M1.36,30.64V4.36h14.28V10c0,0.199,0.161,0.36,0.36,0.36h5.64	v20.28H1.36z M16.36,4.869l4.771,4.771H16.36V4.869z M30.64,27.64h-8.28V10c0-0.096-0.038-0.187-0.105-0.254l-6-6	C16.187,3.678,16.096,3.64,16,3.64h-5.64V1.36h20.28C30.64,1.36,30.64,27.64,30.64,27.64z M4,15.64h15v0.72H4V15.64z M4,18.64h15	v0.721H4V18.64z M4,21.64h15v0.721H4V21.64z M4,24.64h15v0.721H4V24.64z"></path>
</svg>