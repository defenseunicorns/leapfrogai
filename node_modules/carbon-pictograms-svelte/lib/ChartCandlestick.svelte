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
  <path d="M31,31.36H1c-0.199,0-0.36-0.161-0.36-0.36V1h0.72v29.64H31V31.36z M25.36,28h-0.72v-2.64H23	c-0.199,0-0.36-0.161-0.36-0.36V13c0-0.199,0.161-0.36,0.36-0.36h1.64V10h0.721v2.64H27c0.199,0,0.36,0.161,0.36,0.36v12	c0,0.199-0.161,0.36-0.36,0.36h-1.64V28z M23.36,24.64h3.279V13.36H23.36V24.64z M7.36,25H6.64v-5.64H5	c-0.199,0-0.36-0.161-0.36-0.36v-8c0-0.199,0.161-0.36,0.36-0.36h1.64V5h0.72v5.64H9c0.199,0,0.36,0.161,0.36,0.36v8	c0,0.199-0.161,0.36-0.36,0.36H7.36V25z M5.36,18.64h3.28v-7.28H5.36V18.64z M16.36,21h-0.72v-5.64H14	c-0.199,0-0.36-0.161-0.36-0.36V9c0-0.199,0.161-0.36,0.36-0.36h1.64V3h0.72v5.64H18c0.199,0,0.36,0.161,0.36,0.36v6	c0,0.199-0.161,0.36-0.36,0.36h-1.64V21z M14.36,14.64h3.28V9.36h-3.28V14.64z"></path>
</svg>