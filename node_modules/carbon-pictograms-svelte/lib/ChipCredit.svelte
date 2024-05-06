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
  <path d="M29,28.36H3c-1.301,0-2.36-1.059-2.36-2.36V6c0-1.301,1.059-2.36,2.36-2.36h26	c1.302,0,2.36,1.059,2.36,2.36v20C31.36,27.302,30.302,28.36,29,28.36z M22.36,27.64H29c0.904,0,1.64-0.735,1.64-1.64v-3.64h-8.28	V27.64z M10.36,27.64h11.28V10c0-0.199,0.161-0.36,0.36-0.36h8.64V6c0-0.904-0.735-1.64-1.64-1.64H10.36V27.64z M1.36,22.36V26	c0,0.904,0.736,1.64,1.64,1.64h6.64v-5.28H1.36z M22.36,21.64h8.279v-5.28H22.36V21.64z M1.36,21.64h8.28v-5.28H1.36V21.64z M22.36,15.64h8.279v-5.28H22.36V15.64z M1.36,15.64h8.28v-5.28H1.36V15.64z M1.36,9.64h8.28V4.36H3C2.096,4.36,1.36,5.096,1.36,6	V9.64z"></path>
</svg>