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
  <path d="M30,31.36H2c-0.199,0-0.36-0.161-0.36-0.36V13c0-0.199,0.161-0.36,0.36-0.36h11.64V1	c0-0.199,0.161-0.36,0.36-0.36h16c0.199,0,0.36,0.161,0.36,0.36v30C30.36,31.199,30.199,31.36,30,31.36z M14.36,30.64h15.28V1.36	H14.36V13c0,0.199-0.161,0.36-0.36,0.36H2.36v17.28h7.28V23c0-0.199,0.161-0.36,0.36-0.36h4c0.199,0,0.36,0.161,0.36,0.36V30.64z M10.36,30.64h3.28v-7.28h-3.28V30.64z M26.36,25h-0.72v-2h0.721L26.36,25L26.36,25z M22.36,25h-0.72v-2h0.721L22.36,25L22.36,25z M18.36,25h-0.72v-2h0.721L18.36,25L18.36,25z M6.36,25H5.64v-2h0.72C6.36,23,6.36,25,6.36,25z M26.36,19h-0.72v-2h0.721L26.36,19	L26.36,19z M22.36,19h-0.72v-2h0.721L22.36,19L22.36,19z M18.36,19h-0.72v-2h0.721L18.36,19L18.36,19z M14.36,19h-0.72v-2h0.72V19z M10.36,19H9.64v-2h0.72C10.36,17,10.36,19,10.36,19z M6.36,19H5.64v-2h0.72C6.36,17,6.36,19,6.36,19z M26.36,13h-0.72v-2h0.721	L26.36,13L26.36,13z M22.36,13h-0.72v-2h0.721L22.36,13L22.36,13z M18.36,13h-0.72v-2h0.721L18.36,13L18.36,13z M26.36,7h-0.72V5	h0.721L26.36,7L26.36,7z M22.36,7h-0.72V5h0.721L22.36,7L22.36,7z M18.36,7h-0.72V5h0.721L18.36,7L18.36,7z"></path>
</svg>